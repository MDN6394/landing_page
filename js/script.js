// Step 1: Get a reference to the button using its ID
// We use 'const' because the reference to the button won't change.
const button = document.getElementById('myButton');

// Step 2: Define the function that will run when the button is clicked
function handleButtonClick() {
    // This is the "something" that happens!
    console.log('Button was clicked!');
    alert('The button has been pressed!');
    
    // Example: Change the button's text
    button.textContent = 'Clicked!';
}

// Step 3: Attach an event listener to the button
// When the 'click' event occurs, the handleButtonClick function is executed.
button.addEventListener('click', handleButtonClick);