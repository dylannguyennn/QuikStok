from flask import Flask, render_template, request
from posts import search_ticker
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/analyze', methods=['POST'])
def analyze_stock():
    ticker = request.form.get('ticker', '').strip().upper()
    
    return(search_ticker(ticker))

@app.route('/info', methods=['POST'])
def info_stock():
    ticker = request.form.get('ticker', '').strip().upper()
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return render_template('stockinfo.html', 
        name=info.get('longName', ticker),
        symbol=ticker,
        price=info.get('currentPrice', 'N/A'),
        market_cap=info.get('marketCap', 'N/A'),
        pe_ratio=info.get('trailingPE', 'N/A'),
        dividend_yield=info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
        summary=info.get('longBusinessSummary', 'No summary available')
    )
