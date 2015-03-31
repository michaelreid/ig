######################################
# INITAL SETUP OF FLASK & INSTAGRAMAPI
#
# import python modules
import urllib2, json

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
def popular_media():
    # the request to send to instagram api for popular media
    request_insta = urllib2.Request('https://api.instagram.com/v1/media/popular?access_token=' + ACCESS_TOKEN )

    # open the response that instagram sends
    insta_response = urllib2.urlopen(request_insta)

    # read the response and convert to dictionary
    response = json.loads(insta_response.read())
    url_obj = response['data'][0]['images']['low_resolution']['url']
    url_str = str(url_obj)
    print url_str
    likes = response['data'][2]['likes']['count']
    print likes
    # webbrowser.open(url)
    return (url_str, likes)

def list_of_popular(number):
    media = []
    for i in range(number):
        media.append(popular_media())
    return media


######################################
#  DISPLAY THE MOST POPULAR MEDIA
#
@app.route("/<int:number>")
def display_media(number):
    number = int(number)
    media = list_of_popular(number)
    print media 
    return render_template('popular.html', media=media)
    


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