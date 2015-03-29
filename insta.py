import os                                          # to access environment variables
import urllib2                                     # to access urls and resources
import json                                        # to work with json api response
CLIENT_ID = os.environ.get('CLIENT_ID')            # get the CLIENT_ID (stored as a variable)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')    # get the CLIENT_SECRET (stored as variable)
token = open('ig/access_token', 'r')               # open the access_token (stored as a file)
ACCESS_TOKEN = token.read()                        # set ACCESS_TOKEN as variable


def request_popular():
    # the request to send to instagram api for popular media
    request_insta = urllib2.Request('https://api.instagram.com/v1/media/popular?access_token=' + ACCESS_TOKEN )

    # open the response that instagram sends
    insta_response = urllib2.urlopen(request_insta)

    # read the response and convert to dictionary
    page = json.loads(insta_response.read())
    likes = page['data'][0]
    print (likes['count'])
    
# __main__ function to enable from command line
if __name__ == "__main__":
    request_popular()