import os
import re
import praw
import yfinance as yf
import pandas as pd
from analysis import analyze_sentiment
from datetime import datetime, timedelta
from app import db
from models import Post
from sqlalchemy import func

PRAW_CLIENT_ID = os.getenv("PRAW_CLIENT_ID")
PRAW_CLIENT_SECRET = os.getenv("PRAW_CLIENT_SECRET")
PRAW_USER_AGENT = os.getenv("PRAW_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=PRAW_CLIENT_ID,
    client_secret=PRAW_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent=PRAW_USER_AGENT,
    username=REDDIT_USERNAME,
)

def process_ticker(ticker):
    to_shorten = ["Corporation", "Inc.", "Inc", "Corp", "Co", "Co.", "Corp.", "International", "Incorporated", "Company"]
    company = yf.Ticker(ticker).info["shortName"]
    company = company.replace(".", "").replace(",", "").split(" ")
    company = " ".join([i for i in company if i not in to_shorten])
    return company

def search_ticker_reddit(ticker, site='reddit'):
    # Retrieve most recent post/record's date from DB
    last_post_date: datetime = (db.session
                                .query(func.max(Post.post_date))
                                .filter(Post.ticker == ticker)
                                .scalar())
    
    if not last_post_date:
        last_post_date = datetime.now() - timedelta(days=30)

    # List of subreddits to search for submissions in
    subreddit_names = ["Investing", "Stocks", "StockMarket", "WallStreetBets", "ThetaGang", "Dividends", "Options"]
    submissions_list = []
    company = process_ticker(ticker)
    keywords = [company, ticker]

    # Search for submissions containing ticker or company name
    # Stop searching if post_date is older than last_post_date
    for submission in reddit.subreddit('+'.join(subreddit_names)).search(keywords, sort="new", time_filter="month"):
        post_date = datetime.fromtimestamp(submission.created_utc)

        if post_date <= last_post_date:
            break
        if ticker in submission.title or company in submission.title:
            submissions_list.append([submission.title, post_date])

    # Run new submissions through pipeline
    texts, dates = zip(*submissions_list) if submissions_list else ([], [])
    sentiment_df = analyze_sentiment(list(texts))

    # Add new submussions to database
    records = sentiment_df.to_dict('records')
    submissions_db = []
    for rec, txt, dt in zip(records, texts, dates):
        submissions_db.append(
            Post(
                ticker=ticker,
                text=txt, 
                site=site,
                label=rec['label'],
                score=rec['score'],
                post_date=dt
            )
        )

    if submissions_db:
        db.session.bulk_save_objects(submissions_db)
        db.session.commit()    

# ADD SEARCHING FOR TICKER/COMPANY WITHIN SUBMISSION DESCRIPTION
