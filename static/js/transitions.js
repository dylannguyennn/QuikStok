function startTransition(event) {
    event.preventDefault();
    const container = document.getElementById('main-container');
    container.classList.add('fade-out');
    
    setTimeout(() => {
        event.target.submit();
    }, 500);
}

function animatePageElements() {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('animated', `delay-${index % 3}`);
        }, 100);
    });
}

// Run animations when page loads
document.addEventListener('DOMContentLoaded', animatePageElements);
