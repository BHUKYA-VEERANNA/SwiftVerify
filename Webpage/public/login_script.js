// Get the login form element
const loginForm = document.querySelector('.sign-in-form');

// Add an event listener for form submission
loginForm.addEventListener('submit', function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the values of username and password
    const username = this.querySelector('input[type="text"]').value.trim();
    const password = this.querySelector('input[type="password"]').value.trim();

    // Check if the username and password match the predefined credentials
    if (username === 'Admin' && password === 'Admin@123') {
        // Redirect to the dashboard.html page
        window.location.href = 'dashboard.html';
    } else {
        // Display an error message (optional)
        alert('Invalid username or password. Please try again.');
    }
});

const container = document.querySelector('.container');
const signinForm = document.querySelector('.sign-in-form');
const signupForm = document.querySelector('.sign-up-form');
const signinBtn = document.querySelector('#sign-in-btn');
const signupBtn = document.querySelector('#sign-up-btn');

signinBtn.addEventListener('click', () => {
    container.classList.remove('sign-up-mode');
});

signupBtn.addEventListener('click', () => {
    container.classList.add('sign-up-mode');
});

signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.querySelector('.sign-up-form input[type="text"]').value;
    const email = document.querySelector('.sign-up-form input[type="email"]').value;
    const password = document.querySelector('.sign-up-form input[type="password"]').value;
    // Perform signup logic here
    // For demonstration, let's just log the username, email, and password
    console.log('Signing up with username:', username, 'email:', email, 'and password:', password);
});
