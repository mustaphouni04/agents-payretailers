
const nuevaConversacionButton = document.getElementById('nuevaConversacionButton');
const gestionesButton = document.getElementById('gestionesButton');
const conversationTitles = document.querySelectorAll('.conversation-title');
const welcomeMessage = document.getElementById('welcomeMessage');

// Fetch user name and update welcome message
fetch('/get_user_name')
    .then(response => response.json())
    .then(data => {
        if (data && data.name) {
            welcomeMessage.textContent = `Hola, ${data.name}`;
        } else {
            console.error('User name not found in response:', data);
            welcomeMessage.textContent = 'Hola, Usuario'; // Default message
        }
    })
    .catch(error => {
        console.error('Error fetching user name:', error);
        welcomeMessage.textContent = 'Hola, Usuario'; // Default message
    });

nuevaConversacionButton.addEventListener('click', function() {
    window.location.href = '/conversation'; // Redirect to conversation page
});

gestionesButton.addEventListener('click', function() {
    window.location.href = '/management'; // Redirect to management page
});

conversationTitles.forEach(title => {
    title.addEventListener('click', function() {
        window.location.href = '/conversation'; // Redirect to conversation page
    });
});