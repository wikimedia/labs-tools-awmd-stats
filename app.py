import urllib2
import json

# get user stats using Gerrit API
def getUserStats(userId):

    url = 
    if userId!="":
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        jsonArray = result.read()

        return jsonArray
