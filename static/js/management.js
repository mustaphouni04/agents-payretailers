document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_paperwork_data')
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('paperwork-grid');
            data.forEach(paperwork => {
                const box = document.createElement('div');
                box.classList.add('paperwork-box');
                box.innerHTML = `
                    <h3>${paperwork.title}</h3>
                    <p>Summary: ${paperwork.summary}</p>
                    <p>Date: ${paperwork.date}</p>
                `;
                box.addEventListener('click', () => {
                    window.location.href = `/paperwork_details/${paperwork.id}`;
                });
                grid.appendChild(box);
            });
        })
        .catch(error => console.error('Error:', error));
});