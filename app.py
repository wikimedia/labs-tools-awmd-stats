import requests
import json
import time
import itertools
import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask
from flask import render_template
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

# get submitter using Gerrit API
def getSubmitterStats(username, month):
	
	date = getCurrentMonth() 
	previous_month = decrementMonth(date)
	next_month = incrementMonth(date)

	if username!="":
		# concatenate url
		url = "https://gerrit.wikimedia.org/r/changes/?q=owner:" + username + "+after:" + previous_month + "+before:" + next_month;
		
		r = requests.get(url)

		jsonArray = r.text
		jsonArray = jsonArray.replace(")]}'", "", 1); # Fix this error in headers of json tree
		return json.loads(jsonArray);

# get current month
def getCurrentMonth(format = "%Y-%m"):
	currentMonth = time.strftime(format); # eg 2018-02 
	return currentMonth 

# REST endpoint for fetching stats by month
@app.route('/month/<month>')
def month(month=False):
	db = getDb()

	# load and save participants list
	participants = getParticipants()

	# loop through participants
	for participant in participants:

		username = participant['username']
		patches = getSubmitterStats(username)

		# loop through participant patches
		for patch in patches:

			# prepare patch dictionary
			patch['username'] = username;
			patch['name'] = participant['name'];
			patch['country'] = participant['country'];

			# make sure patch wasn't previously saved
			if not patchExists(patch):
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
# check wether patch exists in DB
def patchExists(patch):
	db = getDb()
	Patch = Query()
	rows = db.search((Patch.created == patch['created']) 
		& (Patch.username == patch['username']))

	# if the patch was previously saved
	if (0<len(rows)):
		return True
	else:
		return False
#convert month to date format
def monthToDate(month):

	month = datetime.strptime(month, ("%Y-%m"))
	date = month.strftime("%Y-%m-%d"); # eg 2018-02-01
	date = datetime.strptime(date, ("%Y-%m-%d")) # return datetime object
	
	return date 
	
# increment date by x months
def incrementMonth(month, x=1):
	date =  monthToDate(month)
	next_month = date + relativedelta(months=x)
	return next_month.strftime("%Y-%m-%d")

# decrement date by x months
def decrementMonth(month, x=1):
	date =  monthToDate(month)
	previous_month = date - relativedelta(months=x)
	return previous_month.strftime("%Y-%m-%d")

# test endpoint
@app.route('/test')
def test():
	pprint.pprint(getSubmitterStats('D3r1ck01', '2018-01'))
	return ''

if __name__ == '__main__':
	app.run()