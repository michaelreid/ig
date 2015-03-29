######################################
# INITAL SETUP OF FLASK & INSTAGRAMAPI
#
# setup flask to render templates
from flask import render_template
#
# help flask to find the app (and it's configurations)
from ig import app
#
# setup instagram objects
import os
from instagram.client import InstagramAPI
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8080/callback'
token = open('ig/access_token', 'r')
ACCESS_TOKEN = token.read()
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)



######################################
#
#
#


def popular_media(number):
    return api.media_popular(count=number)
    

def media_likes():
    media = popular_media(3) # get 3 most popular media
    print media
    # likes = api.media_likes()
    for item in media:
        print item.likes

media_likes()

######################################
#  DISPLAY THE MOST POPULAR MEDIA
#    
@app.route("/")
def display_media():
    media = popular_media(3)
    popular_urls = []
    for item in media:
        url = item.images['low_resolution'].url
        popular_urls.append(url)
    return render_template('popular.html', popular_urls=popular_urls)







#######################################
# HACKY MEHTOD TO GENERATE ACCESS TOKEN
#
# 1. instagram setup:
#    

from instagram import client, subscriptions
unauthenticated_api = client.InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

# 2. inital view to generate authentication:
#
@app.route("/authenticate")
def home():
    connect_url = unauthenticated_api.get_authorize_url(scope=["likes", "comments"])
    return render_template("menu.html", connect_url=connect_url)

# 3. view to receive access token:
#    
# setup flask to access the request
#
from flask import request
    
@app.route('/callback')
def on_callback():
    code = request.args.get('code')
    access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
    api = client.InstagramAPI(access_token=access_token)
    # request.session['access_token'] = access_token
    print "access token=" + access_token
    token_file = open('ig/access_token.txt', 'w')
    token_file.write(access_token)
    token_file.close()
    return render_template("menu.html")