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
        status = {"status": "success", "code": 200}
        response = make_response(json.dumps(status), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as error:
        print(error)
        status = {"status": "internal_server_error", "code": 500}
        response = make_response(json.dumps(status), 500)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/subreddit_data/<string:subreddit>')
def crypto_data(subreddit):
    if subreddit in SUBREDDITS:
        all_logs = Log.query.filter(Log.subreddit==subreddit)
        df = pandas.read_sql(all_logs.statement, db.get_engine())

        df.drop(['id', 'subreddit', 'currency_sentiment'], axis=1, inplace=True)

        df_dict = df.to_dict(orient="records")

        status_and_results = {"subreddit": subreddit, "status": "success", "code": 200, "results": df_dict}
        response = make_response(json.dumps(status_and_results), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response      
    else:
        status_and_results = {"subreddit": subreddit, "status": "bad_request", "code": 400}
        response = make_response(json.dumps(status_and_results), 400)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    
