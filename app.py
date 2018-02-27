import requests
import json
import time
import itertools
from flask import Flask
from flask import render_template
from datetime import datetime
from tinydb import TinyDB, Query


app = Flask(__name__) # instantiate Flask

# route for homepage
@app.route('/')
def index():
	stats = getStatsFromDb(getCurrentMonth())
	submitters = getSubmitters(stats)
	month = getCurrentMonth("%B, %Y") # make month format human-readable 

	return render_template('index.html', stats = stats, 
		month = month, submitters = submitters)


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

# REST endpoint for list of submitter patches
@app.route('/submitter/<username>')
def submitter(username):
	Submitter = Query()
	db = getDb()

	patches = db.search(Submitter.username == username) # filter by username
	return render_template('submitter.html', patches = patches)

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
		
		r = requests.get(url)

		jsonArray = r.text
		jsonArray = jsonArray.replace(")]}'", "", 1); # Fix this error in headers of json tree
		return json.loads(jsonArray);

# get current month
def getCurrentMonth(format = "%Y-%m"):
	currentMonth = time.strftime(format); # eg 2018-02 
	return currentMonth 

# cron job for fetching and saving stats, for now fires in HTTP
@app.route('/cron')
def cronTask():
	db = getDb()

	# load and save participants list
	participants = getParticipants()

	# loop through participants
	for participant in participants:

		username = participant['username']
		patches = getUserStats(username)

		# loop through participant patches
		for patch in patches:

			# prepare patch dictionary
			patch['username'] = username;
			patch['name'] = participant['name'];
			patch['country'] = participant['country'];

			# persist patch to db
			db.insert(patch)

	# output the db as json
	output = db.all();

	response = app.response_class(
		response=json.dumps(output),
		status=200,
		mimetype='application/json'
	)

	return response 

# get monthly stats from db
def getStatsFromDb( month ):
	Patch = Query()
	db = getDb()

	stats = db.search(Patch.created.test(filterMonth, month))
	return stats

# custom Flask filter for datetimeformating
@app.template_filter()
def datetimeformat(value, inFormat="%Y-%m-%d %H:%M:%S.000000000", outFormat = '%Y-%m-%d, %H:%M'):
	formattedString = datetime.strptime(value, inFormat)
	return formattedString.strftime(outFormat) # simple formatting

# db object to be used indepently
def getDb():
	# setting the tinydb location
	db = TinyDB('db/db.json')
	return db

# get the list of patch submitters
def getSubmitters(patches):
	submitters = []
	# grouping by, the pythonic way
	for key, group in itertools.groupby(patches, key=lambda x:x['username']):
		submitters.append(list(group))

	return submitters

# filter month
def filterMonth(string, month):
	if month in string: 
		return True
	else:
		return False 

if __name__ == '__main__':
	app.run()