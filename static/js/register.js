document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.form');
    const modal = document.getElementById('myModal');
    const closeButton = document.querySelector('.close');
    const loginButton = document.getElementById('loginButton');
    const message = document.getElementById('message');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            message.textContent = result.error;
            modal.style.display = 'block';
        }
    });

    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    loginButton.addEventListener('click', function () {
        window.location.href = '/login';
    });
});
