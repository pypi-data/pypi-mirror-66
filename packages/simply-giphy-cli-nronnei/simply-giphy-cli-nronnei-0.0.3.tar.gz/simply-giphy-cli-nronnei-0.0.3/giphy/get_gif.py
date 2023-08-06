import sys
import time
import json
import random
import pyperclip
import giphy_client
from giphy_client.rest import ApiException

LIMIT = 10

# create an instance of the API class
api_instance = giphy_client.DefaultApi()
API_KEY = 't13WC1JR1mBky0ABnltycI5p18v0k9Ba' # str | Giphy API Key.

def make_request(query, limit=LIMIT, randomize=True):
    try:
        # Search Endpoint
        api_response = api_instance.gifs_search_get(API_KEY, query, limit=limit)
        return api_response.data
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

def shuffle(links):
    random.shuffle(links)
    return links[0].images.downsized_large.url

def copy (query, link):
    pretty_query = "Searched: *{}*".format(query)
    return pyperclip.copy("\n".join([ pretty_query, link ]))

def hook(query):
    link = shuffle(make_request(query))
    return copy(query, link)
