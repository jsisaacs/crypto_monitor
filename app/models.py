from datetime import datetime
from app import db

class Log(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True)
    subreddit = db.Column(db.String(40), nullable=False)
    active_users = db.Column(db.Integer, nullable=False)
    subreddit_sentiment = db.Column(db.Numeric(1,2), nullable=False)
    currency_sentiment = db.Column(db.Numeric(1,2), nullable=False)
    timestamp = db.Column(db.Numeric(15, 0), nullable=False, index=True, default=datetime.now, primary_key=True)

    def __repr__(self):
        return '<Log {}>'.format(self.subreddit) 