from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

test_data = pandas.read_csv('/Users/joshisaacson/Desktop/crypto_monitor_backend/test_data/crypto_data_dev.csv')
test_data.to_sql(con=db.get_engine(), name="log", if_exists="replace")

from app import routes, models

