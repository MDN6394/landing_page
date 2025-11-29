import os
import json
from flask import Flask, jsonify, request
# We'll use the official Firebase Admin SDK to interact with Firestore
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
CORS(app, origins=["https://diabeticbuddy.netlify.app"])

# --- FIRESTORE CONFIGURATION (Option B: Explicit Credential Loading) ---

# ⚠️ ACTION REQUIRED: 
# 1. Download your Firebase Service Account JSON key.
# 2. Update the path below to the actual file name/path.
#    Example: 'path/to/my-project-firebase-adminsdk-xxxxx.json'
SERVICE_ACCOUNT_PATH = './backend/keys/private_key.json'

db = None
fallback_count = 0

try:
    # 1. Look for the JSON key content in an environment variable
    service_account_json = os.environ.get('FIREBASE_SA_JSON')

    if service_account_json:
        # Load credentials from the secure environment variable
        cred_dict = json.loads(service_account_json)
        cred = credentials.Certificate(cred_dict)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Firestore client initialized successfully using Environment Variable.")
        
    else:
        # 2. Fallback for non-persistent (in-memory) counter if variable is not set
        print("FIREBASE_SA_JSON environment variable not found. Falling back to non-persistent counter.")
        
        # 3. Attempt to fall back to Application Default Credentials if running in a Google Cloud context
        if os.environ.get('FIREBASE_CONFIG'):
             firebase_config = json.loads(os.environ.get('FIREBASE_CONFIG'))
             if not firebase_admin._apps:
                 cred = credentials.ApplicationDefault()
                 firebase_admin.initialize_app(cred, {
                     'projectId': firebase_config.get('projectId', 'default-project-id')
                 })
                 db = firestore.client()
                 print("Fallback: Firestore client initialized using Application Default Credentials.")
        else:
             print("FIREBASE_CONFIG environment variable not found. Counter will not be persistent.")


except Exception as e:
    print(f"Error initializing Firebase/Firestore: {e}")
    db = None


# Define the path for the counter document in Firestore
# We'll use a simple global collection for this demonstration.
CLICK_STATS_DOC_REF = db.collection('global_stats').document('click_counter') if db else None


# --- HELPER FUNCTION TO GET AND INCREMENT COUNT ---

def get_and_increment_count():
    """
    Safely retrieves the current count, increments it, and updates Firestore.
    """
    if not CLICK_STATS_DOC_REF:
        # Fallback for non-persistent (in-memory) counter if DB failed to initialize
        global fallback_count
        fallback_count += 1
        return fallback_count

    try:
        # Use a transaction to ensure atomic increment (thread-safe)
        @firestore.transactional
        def update_in_transaction(transaction):
            doc = CLICK_STATS_DOC_REF.get(transaction=transaction)
            
            # If the document exists, get the 'count' field, otherwise start at 0
            current_count = doc.to_dict().get('count', 0) if doc.exists else 0
            new_count = current_count + 1
            
            # Write the new count back
            transaction.set(CLICK_STATS_DOC_REF, {'count': new_count})
            
            return new_count

        return update_in_transaction(db.transaction())

    except Exception as e:
        print(f"Firestore transaction failed: {e}")
        # In a real application, you'd log this error
        return -1 # Indicate failure

# --- API ENDPOINTS ---

@app.route('/api/increment-count', methods=['POST'])
def increment_count_endpoint():
    """
    Endpoint to receive a click signal and increment the persistent counter.
    Returns the new total count.
    """
    new_count = get_and_increment_count()
    
    if new_count >= 0:
        return jsonify({
            'success': True, 
            'newCount': new_count
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'Failed to update counter due to a database error.'
        }), 500

@app.route('/api/get-count', methods=['GET'])
def get_count_endpoint():
    """
    Endpoint to retrieve the current total click count.
    """
    if not CLICK_STATS_DOC_REF:
        global fallback_count
        return jsonify({'count': fallback_count})

    try:
        doc = CLICK_STATS_DOC_REF.get()
        current_count = doc.to_dict().get('count', 0) if doc.exists else 0
        return jsonify({'count': current_count})
    except Exception as e:
        print(f"Error retrieving count: {e}")
        return jsonify({'count': 0}), 500


# --- RUN BLOCK ---
if __name__ == '__main__':
    # This block is for local testing only. 
    # In a typical server environment, Flask is served using a production WSGI server.
    app.run(debug=True, port=5000)
