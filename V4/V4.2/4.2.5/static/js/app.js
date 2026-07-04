document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('requestForm');
    if (form) {
        form.addEventListener('submit', () => {
            console.log('Form submitted');
        });
    }
});
