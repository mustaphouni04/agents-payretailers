const conversacionesButton = document.getElementById('conversacionesButton');
const sideMenu = document.getElementById('sideMenu');
const closeMenuButton = document.getElementById('closeMenuButton');
const nuevaConversacionButton = document.getElementById('nuevaConversacionButton');
const gestionesButton = document.getElementById('gestionesButton');
const conversationTitles = document.querySelectorAll('.conversation-title');

conversacionesButton.addEventListener('click', function() {
    sideMenu.classList.add('open');
});

closeMenuButton.addEventListener('click', function() {
    sideMenu.classList.remove('open');
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