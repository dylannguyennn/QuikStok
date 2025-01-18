from flask import Flask, render_template, request
from posts import search_ticker
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
    
@app.route('/analyze_stock', methods=['GET', 'POST'])
def analyze_stock():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        subcount = search_ticker(ticker)
        return render_template('analysis.html',
            count = subcount,
            symbol = ticker                   
        )
    else:
        return render_template('home.html')

@app.route('/info_stock', methods=['GET', 'POST'])
def info_stock():
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        stock = yf.Ticker(ticker)
        info = stock.info
        return render_template('stockinfo.html', 
            name = info.get('longName', ticker),
            symbol = ticker,
            price = info.get('currentPrice', 'N/A'),
            market_cap = info.get('marketCap', 'N/A'),
            pe_ratio = info.get('trailingPE', 'N/A'),
            dividend_yield = info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
            summary = info.get('longBusinessSummary', 'No summary available')
        )
    else:
        return render_template('home.html')
