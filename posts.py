import os
import praw
from dotenv import load_dotenv

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

# List of subreddits to search for submissions in
subreddits_names = ["Investing", "Stocks", "StockMarket", "WallStreetBets"]

with open("posts.txt", "w", encoding="utf-8") as txtfile:
    for subreddit in subreddits_names:
        s = reddit.subreddit(subreddit)
        for submission in s.new(limit=100):
            txtfile.write(submission.title + "\n")
