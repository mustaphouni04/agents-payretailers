const nuevaConversacionButton = document.getElementById('nuevaConversacionButton');
const gestionesButton = document.getElementById('gestionesButton');
const conversationTitles = document.querySelectorAll('.conversation-title');
const welcomeMessage = document.getElementById('welcomeMessage');

// Fetch user name and update welcome message
fetch('/get_user_name')
    .then(response => response.json())
    .then(data => {
        welcomeMessage.textContent = `Hola, ${data.name}`;
    })
    .catch(error => {
        console.error('Error fetching user name:', error);
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

const nuevaConversacionButton = document.getElementById('nuevaConversacionButton');
const gestionesButton = document.getElementById('gestionesButton');
const conversationTitles = document.querySelectorAll('.conversation-title');
const welcomeMessage = document.getElementById('welcomeMessage');
