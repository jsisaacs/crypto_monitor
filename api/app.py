from flask import Flask
import sqlalchemy as db
import pandas as pd
import simplejson as json
import os


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])


# engine = db.create_engine(
#     "postgres://joshisaacson:hockey123@cryptodb-instance.cijcjngfdgar.us-east-1.rds.amazonaws.com:5432/cryptodb"
# )
# connection = engine.connect()
# metadata = db.MetaData()
# cryptodb = db.Table("crypto_main", metadata, autoload=True, autoload_with=engine)


@app.route("/health")
def health_check():
    return "health"
    # try:
    #     connection.execute("SELECT 1")
    #     return "200"
    # except Exception as error:
    #     print(error)
    #     return "500"


@app.route("/monitor", defaults={"datapoints_per_subreddit": "All"})
@app.route("/monitor/<datapoints_per_subreddit>")
def crypto_monitor(datapoints_per_subreddit):
    # crypo_subreddits = [
    #     "CryptoCurrency",
    #     "CryptoMarkets",
    #     "LINKTrader",
    #     "Chainlink",
    #     "Bitcoin",
    #     "Ethereum",
    # ]

    # if datapoints_per_subreddit is "All":
    #     nested_json_dict = {}
    #     for subreddit in crypo_subreddits:
    #         data = connection.execute(
    #             f"select active_users, subreddit_sentiment, timestamp from crypto_main where subreddit = '{subreddit}' order by id asc;"
    #         ).fetchall()
    #         df = pd.DataFrame(data)
    #         df.columns = data[0].keys()
    #         df_dict = df.to_dict(orient="records")
    #         nested_json_dict[subreddit] = df_dict
    #     return json.dumps(nested_json_dict)

    # elif int(datapoints_per_subreddit) > 0:
    #     nested_json_dict = {}
    #     for subreddit in crypo_subreddits:
    #         data = connection.execute(
    #             f"""SELECT * FROM (
    #                 SELECT * FROM crypto_main WHERE subreddit = '{subreddit}' ORDER BY id DESC LIMIT {datapoints_per_subreddit}
    #               ) as r ORDER BY id"""
    #         )
    #         df = pd.DataFrame(data)
    #         df.columns = data.keys()
    #         df_dict = df.to_dict(orient="records")
    #         nested_json_dict[subreddit] = df_dict
    #     return json.dumps(nested_json_dict)
    # else:
    #     return "error accessing crypto data"
    print("envir" + os.environ["APP_SETTINGS"])
    return "monitor"


def run_app():
    app.run(host="0.0.0.0", port=5000)
    print("envir" + os.environ["APP_SETTINGS"])
