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

// Loading Overlay
document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze_stock_btn');
    const infoBtn = document.getElementById('info_stock_btn');
    const tickerInput = document.getElementById('stock_ticker_input');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission if it's inside a form
            const ticker = tickerInput.value.trim().toUpperCase();
            if (ticker) {
                // Show loading overlay when analyze button is clicked
                loadingOverlay.classList.add('active');
                // Navigate to the analyze page
                window.location.href = `/analyze_stock/${ticker}`;
            } else {
                console.log("Please enter a stock ticker.");
            }
        });
    }

    if (infoBtn) {
        infoBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission if it's inside a form
            const ticker = tickerInput.value.trim().toUpperCase();
            if (ticker) {
                window.location.href = `/info_stock/${ticker}`;
            } else {
                console.log("Please enter a stock ticker.");
            }
        });
    }
});