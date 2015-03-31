import os                                          # to access environment variables
import urllib2                                     # to access urls and resources
import json                                        # to work with json api response
import webbrowser                                  # to open API responses in browser
CLIENT_ID = os.environ.get('CLIENT_ID')            # get the CLIENT_ID (stored as a variable)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')    # get the CLIENT_SECRET (stored as variable)
token = open('ig/access_token', 'r')               # open the access_token (stored as a file)
ACCESS_TOKEN = token.read()                        # set ACCESS_TOKEN as variable


def popular_media():
    # the request to send to instagram api for popular media
    request_insta = urllib2.Request('https://api.instagram.com/v1/media/popular?access_token=' + ACCESS_TOKEN )

    # open the response that instagram sends
    insta_response = urllib2.urlopen(request_insta)

    # read the response and convert to dictionary
    response = json.loads(insta_response.read())
    url = response['data'][0]['images']['standard_resolution']['url']
    likes = response['data'][2]['likes']['count']
    # webbrowser.open(url)
    print {'url':url, 'likes':likes}

def list_of_popular(number):
    media = []
    for i in range(number):
        media.append(popular_media())
    return media
    
# __main__ function to enable from command line
if __name__ == "__main__":
    list_of_popular(3)