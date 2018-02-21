import urllib2
import json
import datetime

# get user stats using Gerrit API
def getUserStats(userId):

    url = 
    if userId!="":
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        jsonArray = result.read()

        return jsonArray

# create json file for monthly stats
def createJsonFile(jsonTree):
    month = 
    with open('sessions.json', 'w') as f:
        f.write(str(jsonTree))  # convert result to string ad save it