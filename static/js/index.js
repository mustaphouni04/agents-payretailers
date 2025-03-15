document.getElementById('registerButton').addEventListener('click', function() {
    // Redirect to the registration page
    window.location.href = '/registration'; // Replace with your actual registration page URL
});

// Create dynamic spheres
const backgroundCircles = document.querySelector('.background-circles');
const numCircles = 20; // Number of spheres

for (let i = 0; i < numCircles; i++) {
    const circle = document.createElement('div');
    circle.classList.add('circle');

    const size = Math.random() * 50 + 20; // Random size between 20 and 70 pixels
    const x = Math.random() * window.innerWidth;
    const y = Math.random() * window.innerHeight;

    circle.style.width = `${size}px`;
    circle.style.height = `${size}px`;
    circle.style.left = `${x}px`;
    circle.style.top = `${y}px`;

    // Random animation delay to stagger movement
    circle.style.animationDelay = `${Math.random() * 5}s`;

    backgroundCircles.appendChild(circle);
}







