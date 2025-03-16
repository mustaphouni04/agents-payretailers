/* ... REGISTRATION PAGE ... */

document.getElementById('authForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
    })
    .then(response => {
        if (response.ok) {
            return response.text(); // Or response.json() if you return JSON
        } else {
            throw new Error('Authentication failed.');
        }
    })
    .then(data => {
        if (data.includes("survey page")){
            window.location.href = '/survey'; // Redirect to questionnaire
        }
        else if (data.includes("Incorrect password")){
            alert("Contraseña incorrecta.");
        }
        else if (data.includes("Database error")){
            alert("Error en la base de datos, por favor, inténtelo más tarde.");
        }
        else {
            window.location.href = '/survey'; // Redirect to questionnaire
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Un error ocurrió durante autenticación.');
    });
});
