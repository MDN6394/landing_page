// Get the form and message elements
const emailForm = document.getElementById('emailForm');
const emailInput = document.getElementById('emailInput');
const messageDisplay = document.getElementById('THISmessage');
// const emailButton = document.getElementById('submitButton'); // This element is no longer the primary listener

/**
 * Handles the email submission process.
 * @param {Event} event The event object passed by the event listener.
 */
function email(event) {
    // 1. ***CRITICAL FIX: PREVENT DEFAULT SUBMISSION***
    // This stops the browser from submitting the form and reloading the page.
    event.preventDefault(); 
    
    // Get the value of the email input (optional, but useful for real submission)
    const userEmail = emailInput.value; 

    // 2. Reset the text in the box
    emailInput.value = '';

    // 3. Display the thank you message
    messageDisplay.textContent = `Thanks for registration, ${userEmail}`; 
    // Note: I added the userEmail to the message for a more personal touch.
    
    // Optional: Hide the message after a few seconds
    setTimeout(() => {
        messageDisplay.textContent = '';
    }, 5000); // Clears the message after 5 seconds

}

function email2(event) {
    event.preventDefault(); 
    const userEmail = emailInput.value; 

    // --- NEW: Send a request to the server ---
    fetch('/api/increment-count', { // The URL path to your counter endpoint
        method: 'POST', // Use POST to signal data change (increment)
        headers: {
            'Content-Type': 'application/json'
        },
        // Optional: Send the email if your backend needs it for logging,
        // but the server should ignore it for the simple count.
        body: JSON.stringify({ email: userEmail }) 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // The server returns the new count
    })
    .then(data => {
        // You can display the new total count here if needed
        console.log('Total clicks:', data.newCount); 
    })
    .catch(error => {
        console.error('Error incrementing counter:', error);
        // Fallback message
    });
    // ------------------------------------------

    // Existing successful front-end actions:
    emailInput.value = '';
    messageDisplay.textContent = 'Thanks for registration!';
    setTimeout(() => {
        messageDisplay.textContent = '';
    }, 5000); 
}

// ***CRITICAL FIX: LISTEN FOR 'submit' ON THE FORM, NOT 'click' ON THE BUTTON***
// This correctly handles submission, regardless of how it's triggered (button click or pressing Enter).
emailForm.addEventListener('submit', email2);