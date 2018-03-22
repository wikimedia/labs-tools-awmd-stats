# Author: Samuel Guebo, Derick Alangi
# Description: Entry point of the application
# License: MIT

import requests
import json
import time
import itertools
import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask
from flask import render_template, request
from tinydb import TinyDB, Query

# instantiate Flask
app = Flask(__name__)

@app.route('/month/<month>')
@app.route('/')
def index(month=None):
	""" Default / Home page of the application / tool. """
	if month == None:
		month = getCurrentMonth() # make month format human-readable 
	monthID = month
	stats = getStatsFromDb(month)
	contributors = getContributors(stats)

	# check whether there are entries in db
	formatted = datetime.strptime(month, ("%Y-%m"))
	if dbHasMonth(month) == True:
		return render_template('index.html', stats = stats, 
			month = formatted.strftime("%B, %Y"), contributors = contributors, monthID = monthID)
	else:
		return render_template('loader.html', monthID = monthID, formatted = formatted.strftime("%B, %Y"))
 

@app.route('/contributor/<username>/<month>')
def contributorPatchesByMonth(username, month):
	""" REST endpoint for list of contributor's patche(s). """
	Submitter = Query()
	db = getDb()
	# filter by username
	patches = db.search(Submitter.username == username)
	# grab previous url from flask.request.referrer
	backUrl = request.referrer

	return render_template('contributor.html', patches = patches, monthID = month, backUrl = backUrl)


def readContributorsFromFile():
	""" Read through and get all contributors. """
	file = open('contributors.json', "r")
	jsonText =  file.read()
	response = json.loads(jsonText)

	return response


def getContributorStats(username, month=None):
	""" Fetch Gerrit API for patch contributor data. """
	if month == None:
		date = getCurrentMonth()
	else:
		date = month 
	previous_month = decrementMonth(date)
	next_month = incrementMonth(date)

	if username != "":
		link = "https://gerrit.wikimedia.org/r/changes/?q=owner:"
		# build the API requst url
		url = link + username + "+after:" + previous_month + "+before:" + next_month
		r = requests.get(url)
		jsonArray = r.text
		jsonArray = jsonArray.replace(")]}'", "", 1); # Fix this error in headers of json tree

		return json.loads(jsonArray);

@app.route('/refresh/<month>')
@app.route('/refresh/')
def refreshStatsByMonth(month=None):
	""" Force a deep refresh """
	if month == None:
		month = getCurrentMonth() # make month format human-readable 
	formatted = datetime.strptime(month, ("%Y-%m"))

	# Let loader handle the refreshing process as this is its purpose 
	return render_template('loader.html', monthID = month, formatted = formatted.strftime("%B, %Y"))

def getCurrentMonth(format="%Y-%m"):
	""" Get current month. """
	currentMonth = time.strftime(format) # e.g. 2018-02

	return currentMonth 


@app.route('/raw/')
@app.route('/raw/<month>')
def raw(month=None):
	""" Display Raw HTML stats """
	if month == None:
		month = getCurrentMonth()

	# load and save contributors list
	contributors = readContributorsFromFile()

	# loop through contributors
	for contributor in contributors:

		username = contributor['username']
		patches = getContributorStats(username, month)

		# loop through contributor patches
		db = getDb()
		for patch in patches:

			# prepare patch dictionary
			patch['username'] = username;
			patch['name'] = contributor['name'];
			patch['country'] = contributor['country']

			# make sure patch wasn't previously saved
			if not patchExists(patch):
				# persist patch to db
				db.insert(patch)

	stats = getStatsFromDb(month)
	contributors = getContributors(stats)

	formatted = datetime.strptime(month, ("%Y-%m"))

	return render_template('stats.html', stats = stats, monthID = month, 
			month = formatted.strftime("%B, %Y"), contributors = contributors)


def getStatsFromDb(month):
	""" Get monthly statistics from DB. """
	Patch = Query()
	db = getDb()
	stats = db.search(Patch.created.test(filterMonth, month))

	return stats


@app.template_filter()
def datetimeformat(value, inFormat="%Y-%m-%d %H:%M:%S.000000000", outFormat = '%Y-%m-%d, %H:%M'):
	""" Custom Flask filter for datetimeformating. """
	formattedString = datetime.strptime(value, inFormat)

	return formattedString.strftime(outFormat) # simple formatting


def getDb():
	""" DB object to be used independently. """

	# setting the tinydb location
	db = TinyDB('db/db.json')

	return db


def getContributors(patches):
	""" Get the list of patch contributors. """
	contributors = []
	# grouping by, the pythonic way
	for key, group in itertools.groupby(patches, key = lambda x: x['username']):
		contributors.append(list(group))

	return contributors


def filterMonth(string, month):
	""" Filter month. """
	if month in string: 
		return True
	else:
		return False


def patchExists(patch):
	""" Check whether patch(es) exists in the DB. """
	db = getDb()
	Patch = Query()
	rows = db.search((Patch.created == patch['created']) 
		& (Patch.username == patch['username']))

	# if the patch was previously saved
	if len(rows) > 0:
		return True
	else:
		return False


def monthToDate(month):
	""" Convert month to date format. """
	month = datetime.strptime(month, ("%Y-%m"))
	date = month.strftime("%Y-%m-%d"); # eg 2018-02-01
	date = datetime.strptime(date, ("%Y-%m-%d")) # return datetime object
	
	return date 

	
def incrementMonth(month, n=1):
	""" Increment date by 'n' months. """
	date =  monthToDate(month)
	next_month = date + relativedelta(months=n)

	return next_month.strftime("%Y-%m-%d")


def decrementMonth(month, n=1):
	""" Decrement date by 'n' months. """
	date =  monthToDate(month)
	previous_month = date - relativedelta(months=n)

	return previous_month.strftime("%Y-%m-%d")


@app.route('/test')
def sample_request():
	""" Test API endpoint with hardcoded data. """
	pprint.pprint(getContributorStats('D3r1ck01', '2018-01'))

	return ''


def dbHasMonth(month):
	""" Check whether month has entries in the DB. """
	stats = getStatsFromDb(month)
	# if there is at least one entry
	if len(stats) > 0:
		return True
	else:
		return False


# Execute the application
if __name__ == '__main__':
	app.run()