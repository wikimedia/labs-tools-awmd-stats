import urllib2
import json
import time


# loop through participants
def getParticipants():
# read from the previously save sessions.json
    filename = getCurrentMonth()
    file = open(filename + '.json', "r")
    jsonText =  file.read()
    response = app.response_class(
        response=jsonText,
        status=200,
        mimetype='application/json'
    )
    return response

# get user stats using Gerrit API
def getUserStats(username):
    
    if username!="":
        # concatenate url
        url = "https://gerrit.wikimedia.org/r/changes/?q=owner:" + username;
        
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        jsonArray = result.read()

        return jsonArray

# create json file for monthly stats
def createJsonFile(jsonArray):
    filename = getCurrentMonth()
    with open(filename + '.json', 'w') as f:
        f.write(str(jsonArray))  # convert result to string ad save it

# get current month
def getCurrentMonth():
    currentMonth = time.strftime("%Y-%m"); # eg: 2018-02 
    return currentMonth   
