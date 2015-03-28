# setup flask to render templates
from flask import render_template

# help flask to find the app (and it's configurations)
from ig import app

# setup instagram objects
import os
from instagram.client import InstagramAPI
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

@app.route("/")
def popular():
    popular_media = api.media_popular(count=100)
    results = []
    for media in popular_media:
        results.append(media.images['standard_resolution'].url)
    print results
    return render_template("popular.html", results=results)
    

