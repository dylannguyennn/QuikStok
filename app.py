from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta 
import yfinance as yf
import os
import asyncio

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# To avoid circular imports
from posts import search_ticker_reddit 
from models import Post

def score_label(label: str, score: float) -> float:
    if label == "POSITIVE":
        return score
    elif label == "NEGATIVE":
        return -score
    else:
        return 0.0
    
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
    
@app.route('/analyze_stock/<ticker>', methods=['GET'])
def analyze_stock(ticker):
    # Search for new submissions containing ticker/company name 
    # and add them to the database if they are newer than most recent record
    ticker = ticker.strip().upper() 
    # search_ticker_reddit(ticker)
    asyncio.run(search_ticker_reddit(ticker))

    # Retrieve all posts from DB within timeframe
    timeframe = datetime.now() - timedelta(days=30)
    recent = (Post.query
            .filter(Post.ticker == ticker,
                    Post.post_date >= timeframe)
            .all())
    
    sentiment_data = []
    for post in recent:
        sentiment_data.append({
            'title': post.text,
            'post_date': post.post_date,
            'label': post.label,
            'score': post.score
        })

    scores = [score_label(r["label"], r["score"]) for r in sentiment_data]
    if scores:
        mean_sentiment = sum(scores) / len(scores)
    else:
        mean_sentiment = 0.0
    index_0_100 = round((mean_sentiment + 1) * 50)

    # Buckets
    if index_0_100 < 20:
        bucket = "Very Bearish"
    elif index_0_100 < 40:
        bucket = "Bearish"
    elif index_0_100 < 60:
        bucket = "Neutral"
    elif index_0_100 < 80:
        bucket = "Bullish"
    else:
        bucket = "Very Bullish"

    print(mean_sentiment)
    print(bucket)

    return render_template('analysis.html',
        symbol = ticker ,
        sentiment_rows = sentiment_data,
        sentiment_index = index_0_100,
        sentiment_label = bucket               
    )


@app.route('/info_stock/<ticker>', methods=['GET'])
def info_stock(ticker):
    ticker = ticker.strip().upper() 
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
