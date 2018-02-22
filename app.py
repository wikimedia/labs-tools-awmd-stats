import urllib2
import json
import time
from flask import Flask
from flask import render_template


app = Flask(__name__) # instantiate Flask


# route for homepage
@app.route('/')
def index():
    stats = getStatsFromDb(getCurrentMonth()) # stats for the current month
    #return render_template('index.html', stats = stats)
    return stats

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

        # create array with [{ username: [details: [userdetails], stats: [patches] ] }]
        monthlyStats.append([username, [ ['details', participant], ['stats', participant_patches] ]])

    # convert from array to json
    createJsonFile(json.dumps(monthlyStats))

    response = app.response_class(
        response=json.dumps(monthlyStats),
        status=200,
        mimetype='application/json'
    )
    return response

# get monthly stats from DB (file)
def getStatsFromDb( month ):
    
    # read stats from DB (file)
    file = open("stats/" + month + ".json", "r")
    jsonText =  file.read()
    jsonText =  file.read()
    stats = jsonText
    
    return stats


if __name__ == '__main__':
    app.run()