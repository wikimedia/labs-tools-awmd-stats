import urllib2
import json
import time
from flask import Flask
from flask import render_template
from datetime import datetime



app = Flask(__name__) # instantiate Flask

# route for homepage
@app.route('/')
def index():
    # register datetime filter

    # stats = getStatsFromDb(getCurrentMonth()) # stats for the current month
    #return render_template('index.html', stats = stats)
    with open('stats/' + getCurrentMonth() + '.json', 'r') as f:
    #with open('stats/test.json', 'r') as f:
        stats = json.load(f)

    return render_template('index.html', stats = stats)
    #return render_template('test.html', stats = stats)

# REST endpoint for fetching stats by month
@app.route('/month/<month>')
def month():
    file = open("stats/" + month + ".json", "r")
    jsonText =  file.read()
    response = app.response_class(
        response=jsonText,
        status=200,
        mimetype='application/json'
    )
    return response

# loop through participants
def getParticipants():

    file = open('participants.json', "r")
    jsonText =  file.read()
    response = json.loads(jsonText)
    return response

# get user stats using Gerrit API
def getUserStats(username):
    
    if username!="":
        # concatenate url
        url = "https://gerrit.wikimedia.org/r/changes/?q=owner:" + username;
        
        request = urllib2.Request(url)
        result = urllib2.urlopen(request)
        jsonArray = result.read()

        jsonArray = jsonArray.replace(")]}'", ""); # Fix this error in headers of json tree
        return json.loads(jsonArray);

# create json file for monthly stats
def createJsonFile(jsonArray):
    filename = getCurrentMonth()
    with open('stats/' + filename + '.json', 'w') as f:
        f.write(str(jsonArray))  # convert result to string ad save it

# get current month
def getCurrentMonth():
    currentMonth = time.strftime("%Y-%m"); # eg 2018-02 
    return currentMonth 

# cron job for fetching and saving stats, for now fires in HTTP
@app.route('/cron')
def cronTask():
    # load and save participants stats
    participants = getParticipants()

    monthlyStats = []
    for participant in participants:

        username = participant['username']
        patches = getUserStats(username)

        participant_patches = [];

        for patch in patches:
            participant_patches.append(patch)   

        # append a dictionary to an array
        monthlyStats.append({'details': participant, 'stats': participant_patches })

    # convert from array to json
    output = json.dumps(monthlyStats) # converting list to json
    createJsonFile(output)

    response = app.response_class(
        response=output,
        status=200,
        mimetype='application/json'
    )
    return response 

# get monthly stats from DB (file)
def getStatsFromDb( month ):
    
    # read stats from DB (file)
    file = open("stats/" + month + ".json", "r")
    jsonText =  file.read()
    stats = json.loads(jsonText)
    
    return json

# custom Flask filter for datetimeformating
@app.template_filter()
def datetimeformat(value, format):

    return datetime.strptime(value, format)

if __name__ == '__main__':
    app.run()