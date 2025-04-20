from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(6), nullable=False)
    text = db.Column(db.Text, nullable=False)
    site = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(20), nullable=True)    # Sentiment label
    score = db.Column(db.Float, nullable=True)         # Sentiment score
    post_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
