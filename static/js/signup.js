// Get references to the form and the button
const form = document.getElementById('loginForm');
const button = form.querySelector('.innButton');

// Check if the form fields are filled out
function checkForm() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const isFormFilled = email.value.trim() !== '' && password.value.trim() !== '';

    // Add or remove 'filled' class based on form status
    if (isFormFilled) {
        form.classList.add('filled');  // Change button hover color to green
    } else {
        form.classList.remove('filled');  // Change button hover color to red
    }
}

// Add event listeners to check form fields on input change
form.addEventListener('input', checkForm);

// Check the form when the page loads
checkForm();