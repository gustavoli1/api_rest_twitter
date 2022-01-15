from flask import Flask, jsonify, abort, make_response, request
from prometheus_flask_exporter import PrometheusMetrics
import json, pymysql, os, sys, requests
app = Flask(__name__)
app.run(debug=True,port=5000,host='0.0.0.0')
metrics = PrometheusMetrics(app)

@app.route('/')
def main():
    pass

@app.route('/insert')
def getInsert():
    pass
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPUlXwEAAAAAtzrlqyjGbMw7QvrsxOm57FLVxB8%3DvtN6watQAExUQFq2SlvgHfuMMygcQgoJF1Yo2KYIPMPZvwc3Ld"
    def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=100".format(
            query, tweet_fields
        )
        response = requests.request("GET", url, headers=headers)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
    query = request.args["hashtag"]
    tweet_fields = "tweet.fields=text,author_id,created_at,lang"
    json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    con = pymysql.connect(host='db_twitter',user='twitter_user',passwd='p0o9i8u7y6',db='twitter_db')
    cursor = con.cursor()
    for json_obj in json_response['data']:
        cursor.execute("INSERT INTO twitter_db(created_at ,text , id , author_id, lang, hashtag) VALUES (%s, %s, %s, %s, %s, %s)", (json_obj['created_at'], json_obj['text'], json_obj['id'], json_obj['author_id'], json_obj['lang'], query))
    con.commit()
    con.close()
    return json.dumps(json_response, indent=4, sort_keys=True)

@app.route('/tag_by_lang')
def getLang():
    pass
    con = pymysql.connect(host = 'db_twitter',user = 'twitter_user',passwd = 'p0o9i8u7y6',db = 'twitter_db')
    cursor = con.cursor()
    cursor.execute("select hashtag, lang, count(lang) from twitter_db where hashtag='"+request.args["hashtag"]+"' group by lang, hashtag having count(lang) > 1")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return json.dumps(data, indent=4, sort_keys=True)    

@app.route('/group_by_hour')
def getGroupHour():
    pass
    con = pymysql.connect(host = 'db_twitter',user = 'twitter_user',passwd = 'p0o9i8u7y6',db = 'twitter_db')
    cursor = con.cursor()
    cursor.execute("SELECT DATE_FORMAT(MIN(created_at), '%d/%m/%Y %H:%i:00') AS group_by_hour, count(created_at) AS count_tweet FROM twitter_db GROUP BY ROUND(UNIX_TIMESTAMP(created_at) / 3600);")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return json.dumps(data, indent=4, sort_keys=True) 

@app.route('/group_by_hour_tag')
def getGroupHourTag():
    pass
    con = pymysql.connect(host = 'db_twitter',user = 'twitter_user',passwd = 'p0o9i8u7y6',db = 'twitter_db')
    cursor = con.cursor()
    cursor.execute("SELECT DATE_FORMAT(MIN(created_at), '%d/%m/%Y %H:%i:00') AS tmstamp, hashtag, COUNT(hashtag) AS cnt FROM twitter_db WHERE hashtag='"+request.args["hashtag"]+"'GROUP BY ROUND(UNIX_TIMESTAMP(created_at) / 3600), hashtag;")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return json.dumps(data, indent=4, sort_keys=True)





