/* ... SURVEY PAGE ... */

document.getElementById('finish-survey').addEventListener('click', function() {
    const name = document.getElementById('name').value;
    const sex = document.getElementById('sex').value;
    const country = document.getElementById('country').value;

    if (name && sex && country) {
        updateUserInfo(name, sex, country);
    } else {
        alert('Please fill in all fields.');
    }
});

function updateUserInfo(name, sex, country) {
    fetch('/update_user_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `name=${encodeURIComponent(name)}&sex=${encodeURIComponent(sex)}&country=${encodeURIComponent(country)}`
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/main'; // Redirect to next page
        } else {
            alert('Failed to update user info.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred.');
    });
}