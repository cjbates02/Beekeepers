function isPasswordValid(e) {  
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const errorMessage = document.getElementById('errorMessage');
    
    if (password !== confirmPassword) {
        e.preventDefault();
        errorMessage.style.display = 'block'; 
    } else {
        errorMessage.style.display = 'none'; 
    }
}

document.getElementById('signupForm').addEventListener('submit', (e) => {
    isPasswordValid(e);
});