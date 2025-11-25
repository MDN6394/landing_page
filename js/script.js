// Step 1: Get a reference to the button using its ID
// We use 'const' because the reference to the button won't change.
const button = document.getElementById('myButton');

// Step 2: Define the function that will run when the button is clicked
function handleButtonClick() {
    const url = "https://forms.office.com/Pages/ResponsePage.aspx?id=xTzTd7TJZkeVx-1bUV4cziphz6xyu4lEro3MSVcU7xRUN1lSSTlYQ0hRWjNHRzRPOVdUMU5KNlFGVy4u"

    window.open(url, '_blank', 'noopener,noreferrer');
}

// Step 3: Attach an event listener to the button
// When the 'click' event occurs, the handleButtonClick function is executed.
button.addEventListener('click', handleButtonClick);