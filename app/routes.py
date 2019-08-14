from app import app, db
from app.models import Log
from app.subreddits import SUBREDDITS
from flask import make_response
import pandas
import simplejson as json

@app.route("/health")
def health_check():
    try:
        query = Log.query.first()
        response = {"status": "success", "code": 200}
        return make_response(json.dumps(response), 200)
    except Exception as error:
        print(error)
        response = {"status": "internal_server_error", "code": 500}
        return make_response(json.dumps(response), 500)

@app.route('/crypto_data/<string:subreddit>')
def crypto_data(subreddit):
    if subreddit in SUBREDDITS:
        all_logs = Log.query.filter(Log.subreddit==subreddit)
        df = pandas.read_sql(all_logs.statement, db.get_engine())

        df.drop(['id', 'subreddit', 'currency_sentiment'], axis=1, inplace=True)

        df_dict = df.to_dict(orient="records")
        status = {"status": "success", "code": 200}

        response = {"response": status, "results": df_dict}
        return make_response(json.dumps(response), 200)
    else:
        response = {"status": "bad_request", "code": 400}
        return make_response(json.dumps(response), 400)
    
