from flask import Flask
import sqlalchemy as db
import pandas as pd
import simplejson as json
import os
from .util import setup_dev_database


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])

db_info = {}
environment = app.config["ENV"]

if environment is "production":
    pass
elif environment is "development":
    setup_dev_database(app.config)
elif environment is "test":
    pass

# engine = db.create_engine(app.config["DATABASE_URI"])
# connection = engine.connect()
# metadata = db.MetaData()
# cryptodb = db.Table(
#     "crypto_data",
#     metadata,
#     autoload=True,
#     autoload_with=engine
# )


# def setup_database(environment, config):
#     engine = db.create_engine(app.config["DATABASE_URI"])

#     if not database_exists(engine.url):
#         create_database(engine.url)

#     print(engine.url)

# if environment is "production":
#     if engine.has_table(cryptodb):

# if environment is "development":
#     pass
# if environment is "test":
#     pass
# else:
#     raise Exception(
#         "error"
#     )


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
    #             f"select active_users,
    # subreddit_sentiment,
    # timestamp from crypto_main
    # where subreddit = '{subreddit}'
    # order by id asc;"
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
    #                 SELECT * FROM
    # crypto_main
    # WHERE subreddit = '{subreddit}'
    # ORDER BY id
    # DESC LIMIT {datapoints_per_subreddit}
    #               ) as r ORDER BY id"""
    #         )
    #         df = pd.DataFrame(data)
    #         df.columns = data.keys()
    #         df_dict = df.to_dict(orient="records")
    #         nested_json_dict[subreddit] = df_dict
    #     return json.dumps(nested_json_dict)
    # else:
    #     return "error accessing crypto data"
    print(app.config["DATABASE_URI"])
    return "monitor"


def run_app():
    app.run(host="0.0.0.0", port=5000)
