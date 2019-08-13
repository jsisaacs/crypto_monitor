import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import os


def get_test_data_path(filename):
    current_dir = os.path.dirname(__file__)
    to_test_data_dir = "../db/test_data"

    joined_desired_dir = os.path.join(current_dir, to_test_data_dir)
    abs_path_test_data = os.path.abspath(joined_desired_dir)

    pregenerated_data_path = abs_path_test_data + f"/{filename}"

    return pregenerated_data_path


def setup_dev_database(config):
    try:
        if config["ENV"] is "development":
            engine = db.create_engine(config["DATABASE_URI"])
            connection = engine.connect()
            metadata = db.MetaData()

            connection.execute("""drop table if exists crypto_data;""")
            connection.execute(
                """create table crypto_data (
                    id serial primary key,
                    subreddit varchar(20) not null,
                    active_users integer not null,
                    subreddit_sentiment numeric not null,
                    currency_sentiment numeric not null,
                    timestamp numeric not null
              );"""
            )

            data_path = get_test_data_path("crypto_data_dev.csv")

            connection.execute(
                f"""copy crypto_data (
                    active_users,
                    currency_sentiment, 
                    subreddit, 
                    subreddit_sentiment, 
                    timestamp,
                    id
                  )
                  from '{data_path}'
                  delimiter ',' csv header;"""
            )

            connection.invalidate()
            engine.dispose()
        else:
            print(f"ENV: {app.config['ENV']} needs to be 'development'")
            raise Exception("Incorrect environment")
    except Exception as error:
        print(error)
