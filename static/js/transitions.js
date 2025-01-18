function startTransition(event) {
    event.preventDefault();
    const container = document.getElementById('main-container');
    container.classList.add('fade-out');
    
    // Get the clicked button's formaction
    const clickedButton = event.submitter;
    const form = event.target;
    if (clickedButton && clickedButton.formAction) {
        form.action = clickedButton.formAction;
    }
    
    setTimeout(() => {
        form.submit();
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
