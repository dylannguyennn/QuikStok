import os
import praw
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from analysis import analyze_sentiment

load_dotenv()

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

def search_ticker(ticker):
    # List of subreddits to search for submissions in
    subreddits_names = ["Investing", "Stocks", "StockMarket", "WallStreetBets"]
    submission_list = []

    for subreddit_name in subreddits_names:
        for submission in reddit.subreddit(subreddit_name).search(ticker, sort="new"):
            company = yf.Ticker(ticker).info["shortName"]
            if ticker in submission.title or company in submission.title:
                submission_list.append(submission.title)

    submission_dict = pd.DataFrame(submission_list, columns=["title"]).to_dict()

    return analyze_sentiment(submission_dict)


