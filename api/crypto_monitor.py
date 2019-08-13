#!/usr/bin/env python3

import praw
from pprint import pprint
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlalchemy as db
import statistics
import datetime


reddit = praw.Reddit(
    client_id="_KDU2aJRg-99Vg",
    client_secret="eLXrEKwH946QrsItQ5OZuNcqAuU",
    user_agent="script:crypo-monitor:v0.0.1 (by /u/puddlypanda12321)",
)

crypo_subreddits = [
    "CryptoCurrency",
    "CryptoMarkets",
    "LINKTrader",
    "Chainlink",
    "AskReddit",
]

chainlink_terms = [
    "json",
    "jason",
    "parser",
    "chad",
    "o'fork",
    "ofork",
    "link",
    "chainlink",
    "chain",
    "nulink",
    "nolink",
    "sergey",
    "700k",
    "singularity",
]


def create_mod_dict(subreddit_collection):
    mods = {}
    for subreddit in subreddit_collection:
        subreddit_mods = reddit.subreddit(subreddit).moderator()
        mods[subreddit] = subreddit_mods
    return mods


# filter_type: either hot or controversial
def get_posts(subreddit, filter_type, post_limit, mods):
    posts = []
    subreddit_mods = mods[subreddit]
    if filter_type is "hot":
        for submission in reddit.subreddit(subreddit).hot(limit=post_limit):
            user = submission.author
            if user not in subreddit_mods:
                posts.append(submission)
    if filter_type is "controversial":
        for submission in reddit.subreddit(subreddit).controversial(limit=post_limit):
            user = submission.author
            if user not in subreddit_mods:
                posts.append(submission)
    return posts


def get_comments_from_post(post, comment_limit):
    post.comment_sort = "top"
    post.comment_limit = comment_limit
    post.comments.replace_more(limit=0)
    comments = post.comments.list()
    return comments


def get_post_sentiment(post, comment_limit):
    comments_compound_sentiment = []
    analyzer = SentimentIntensityAnalyzer()
    comments = get_comments_from_post(post, comment_limit)
    for comment in comments:
        lowercase_comments = comment.body.lower()
        scores = analyzer.polarity_scores(lowercase_comments)
        comments_compound_sentiment.append(scores["compound"])
    return comments_compound_sentiment


def get_subreddit_sentiment(subreddit, filter_type, post_limit, comment_limit, mods):
    posts_compound_sentiment = []
    subreddit_posts = get_posts(subreddit, filter_type, post_limit, mods)
    for post in subreddit_posts:
        post_sentiment = get_post_sentiment(post, comment_limit)
        if len(post_sentiment) is not 0:
            posts_compound_sentiment.append(post_sentiment)
    post_averages = []
    for post_sentiment_scores in posts_compound_sentiment:
        if len(post_sentiment_scores) is not 0:
            average_post_compound_sentiment = statistics.mean(post_sentiment_scores)
            post_averages.append(average_post_compound_sentiment)
    average_subreddit_compound_sentiment = round(statistics.mean(post_averages), 2)
    return average_subreddit_compound_sentiment


def get_active_users(subreddit):
    sub_name = reddit.subreddit(subreddit)
    active_users = sub_name.active_user_count
    return active_users


def run_crypto_monitor(filter_type, post_limit, comment_limit):
    # try:
    nltk.download("vader_lexicon")

    engine = db.create_engine(
        "postgres://joshisaacson:hockey123@cryptodb-instance.cijcjngfdgar.us-east-1.rds.amazonaws.com:5432/cryptodb"
    )
    connection = engine.connect()

    metadata = db.MetaData()
    cryptodb = db.Table("crypto_main", metadata, autoload=True, autoload_with=engine)

    mods = create_mod_dict(crypo_subreddits)
    for subreddit in crypo_subreddits:
        subreddit_sentiment = get_subreddit_sentiment(
            subreddit, filter_type, post_limit, comment_limit, mods
        )
        subreddit_activity = get_active_users(subreddit)
        timestamp = datetime.datetime.now().timestamp()

        query = db.insert(cryptodb).values(
            subreddit=subreddit,
            active_users=subreddit_activity,
            subreddit_sentiment=subreddit_sentiment,
            currency_sentiment=0,
            timestamp=timestamp,
        )
        connection.execute(query)

        print("{} | {} | {}".format(subreddit, subreddit_sentiment, subreddit_activity))

    # except Exception as k:
    #     print("Error connnecting to database")
    #     print(k)


if __name__ == "__main__":
    run_crypto_monitor("hot", 20, 5)
    # print(get_active_users("CryptoNews"))
