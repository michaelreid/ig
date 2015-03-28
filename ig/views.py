# setup flask to render templates
from flask import render_template

# help flask to find the app (and it's configurations)
from ig import app

# setup instagram objects
import os
from instagram.client import InstagramAPI
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8080/callback'
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

@app.route("/")
def popular():
    popular_media = api.media_popular(count=100)
    results = []
    for media in popular_media:
        results.append(media.images['standard_resolution'].url)
    print results
    return render_template("popular.html", results=results)
    

# generate access token
# instagram setup    
from instagram import client, subscriptions
unauthenticated_api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

@app.route("/authenticate")
def home():
    connect_url = unauthenticated_api.get_authorize_url(scope=["likes", "comments"])
    return render_template("menu.html", connect_url=connect_url)


@app.route("/callback?code=<code>")
def on_callback(code):
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        api = client.InstagramAPI(access_token=access_token)
        request.session['access_token'] = access_token
        print "access token=" + access_token
    except Exception as e:
        print e
    return render_template("menu.html")