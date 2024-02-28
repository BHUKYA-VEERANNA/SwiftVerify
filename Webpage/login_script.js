// Get the login form element
const loginForm = document.getElementById('loginForm');

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

const container = document.getElementById('container');
const loginBtn = document.getElementById('login');
const signupBtn = document.getElementById('register');
const signinForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
    signinForm.style.display = 'block';
    signupForm.style.display = 'none';
});

signupBtn.addEventListener('click', () => {
    container.classList.add("active");
    signinForm.style.display = 'none';
    signupForm.style.display = 'block';
});

signinForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    // Perform login logic here
    // For demonstration, let's just log the username and password
    console.log('Logging in with username:', username, 'and password:', password);
});

signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    // Perform signup logic here
    // For demonstration, let's just log the username, email, and password
    console.log('Signing up with username:', username, 'email:', email, 'and password:', password);
});
