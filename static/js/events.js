document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze_stock_btn');
    const infoBtn = document.getElementById('info_stock_btn');
    const tickerInput = document.getElementById('stock_ticker_input'); 

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default form submission if it's inside a form
            const ticker = tickerInput.value.trim().toUpperCase();
            if (ticker) {
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