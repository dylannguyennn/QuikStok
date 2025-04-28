from datetime import datetime
from app import db
from sqlalchemy import UniqueConstraint
import hashlib
import unicodedata
import re

class Post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = (
        db.UniqueConstraint('ticker', 'text_hash', name='unique_ticker_texthash'),
    )

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(6), nullable=False)
    text = db.Column(db.Text, nullable=False)
    text_hash = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(20), nullable=False) # Submission/SubmissionComment/Comment
    site = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(20), nullable=True)    # Sentiment label
    score = db.Column(db.Float, nullable=True)         # Sentiment score
    post_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Text normalization -> Hash -> Avoid duplicate posts
    @staticmethod
    def create_hash(text: str) -> str:
        norm = text.replace('\r\n', '\n')
        norm = unicodedata.normalize('NFC', norm)

        # Optional for additional normalization/cleaning
        # norm = re.sub(r'!\[.*?\]\(.*?\)', '', norm)
        # norm = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', norm)
        # norm = re.sub(r'<[^>]+>', '', norm)
        # norm = re.sub(r'[\u200B\uFEFF]', '', norm)
        # norm = re.sub(r'\s+', ' ', norm)
        # norm = norm.strip()

        return hashlib.sha256(norm.encode('utf-8')).hexdigest()
