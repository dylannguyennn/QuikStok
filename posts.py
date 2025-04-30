import os
import praw
import asyncpraw
import asyncio
from analysis import analyze_sentiment
from datetime import datetime, timedelta
from app import db
from models import Post
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

PRAW_CLIENT_ID = os.getenv("PRAW_CLIENT_ID")
PRAW_CLIENT_SECRET = os.getenv("PRAW_CLIENT_SECRET")
PRAW_USER_AGENT = os.getenv("PRAW_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

async def fetch_submissions(reddit, subreddit_names, submissions_list, ticker, company, last_post_date):

    # Search for submissions containing ticker or company name
    # Stop searching if post_date is older than last_post_date
    print("Beginning submission processing...")
    keywords = [ticker, company]
    subreddit = await reddit.subreddit('+'.join(subreddit_names))
    async for submission in subreddit.search(query=keywords, sort="new", time_filter="month", limit=None):
        post_date = datetime.fromtimestamp(submission.created_utc)

        if post_date <= last_post_date:
            break
        if ticker in submission.title or company in submission.title:
            submissions_list.append([submission.title, post_date, "submission_title"])
        if ticker in submission.selftext or company in submission.selftext:
            submissions_list.append([submission.selftext, post_date, "submission_selftext"])
    print("Submission processing finished.")



async def fetch_comments(reddit, subreddit_names, submissions_list, ticker, company, last_post_date):
    print("Beginning comment processing...")
    subreddit = await reddit.subreddit('+'.join(subreddit_names))
    async for comment in subreddit.comments(limit=500):
        comment_date = datetime.fromtimestamp(comment.created_utc)

        if comment_date <= last_post_date:
            break
        if ticker in comment.body or company in comment.body:
            submissions_list.append([comment.body, comment_date, "comment"])
    print("Finished comment processing...")



async def search_ticker_reddit(ticker, company, site='reddit'):
    reddit = asyncpraw.Reddit(
        client_id=PRAW_CLIENT_ID,
        client_secret=PRAW_CLIENT_SECRET,
        password=REDDIT_PASSWORD,
        user_agent=PRAW_USER_AGENT,
        username=REDDIT_USERNAME,
    )

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

    await asyncio.gather(
        fetch_submissions(reddit, subreddit_names, submissions_list, ticker, company, last_post_date),
        fetch_comments(reddit, subreddit_names, submissions_list, ticker, company, last_post_date)
    )

    # Run new submissions through pipeline
    texts, dates, types = zip(*submissions_list) if submissions_list else ([], [], [])
    sentiment_df = analyze_sentiment(list(texts))

    # Add new submissions to database
    records = sentiment_df.to_dict('records')
    submissions_db = []
    for rec, txt, dt, type in zip(records, texts, dates, types):
        submissions_db.append(
            Post(
                ticker=ticker,
                text=txt, 
                text_hash=Post.create_hash(txt),
                site=site,
                label=rec['label'],
                score=rec['score'],
                post_date=dt,
                type=type
            )
        )
    
    if submissions_db:
        statement = insert(Post).values([
            {
                'ticker': p.ticker,
                'text': p.text,
                'text_hash': p.text_hash,
                'type': p.type,
                'site': p.site,
                'label': p.label,
                'score': p.score,
                'post_date': p.post_date
            }
            for p in submissions_db
        ])
        statement = statement.on_conflict_do_nothing(index_elements=['ticker', 'text_hash'])
        db.session.execute(statement)
        db.session.commit()