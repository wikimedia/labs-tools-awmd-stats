#!/usr/bin/env python

# Authors:  Derick N. Alangi,
#           Samuel Guebo

import itertools
import json
import requests
import time

from dateutil import relativedelta
from datetime import datetime
from operator import itemgetter
from tinydb import TinyDB
from tinydb import Query

"""
Utility functions to perform specific tasks for the app.
"""


def readContributorsFromFile():

    """Read through and get all contributors."""

    file = open('contributors.json', "r")
    jsonText = file.read()
    response = json.loads(jsonText)

    return response


def getContributorStats(username, month=None):

    """
    Fetch Gerrit API for patch contributor data.

    Keyword arguments:
    username -- the gerrit handle of the contributor
    month -- the corresponding month to get contributor statistics
    """

    if month is None:
        date = getCurrentMonth()
    else:
        date = month
    previous_month = decrementMonth(date)
    next_month = incrementMonth(date)

    if username != "":
        link = "https://gerrit.wikimedia.org/r/changes/?q=owner:"
        # build the API requst url
        url = link + username + "+after:" + \
            previous_month + "+before:" + next_month
        r = requests.get(url)
        jsonArray = r.text
        # Fix this error in headers of json tree
        jsonArray = jsonArray.replace(")]}'", "", 1)

        return json.loads(jsonArray)


def getCurrentMonth(format="%Y-%m"):

    """
    Get current month for a particular year.

    Keyword arguments:
    format -- the current month format to be used
    """

    currentMonth = time.strftime(format)  # e.g. 2018-02

    return currentMonth


def getStatsFromDb(month):

    """
    Get monthly statistics from DB.

    Keyword arguments:
    month -- the month to get monthly stats from db.json
    """

    Patch = Query()
    db = getDb()
    # stats = db.search(Patch.created == month)
    stats = db.search(Patch.created.test(filterMonth, month))

    return stats


def getDb():

    """DB object to be used independently."""

    # setting the tinydb location
    db = TinyDB('database/db.json')

    return db


def getContributors(patches):

    """
    Get the list of patch contributors.

    Keyword arguments:
    patches -- patches of all patch contributors
    """

    data = []
    contributors = []

    # group contributions by username
    data = sorted(patches, key=itemgetter('username'))

    for k, g in itertools.groupby(data, key=lambda x: x['username']):
        contributors.append(list(g))  # Store group iterator as a list

    return contributors


def filterMonth(string, month):

    """
    Filter month.

    Keyword arguments:
    string -- the string to perform the filtration on
    month -- the month used as the filter
    """

    if month in string:
        return True
    else:
        return False


def patchExists(patch):

    """
    Check whether patch(es) exists in the DB.

    Keyword arguments:
    patch -- the patch(es) to be checked if it exist in db.json
    """

    db = getDb()
    Patch = Query()
    rows = db.search(
        (Patch.created == patch['created']) &
        (Patch.username == patch['username'])
    )

    # if the patch was previously saved
    if len(rows) > 0:
        return True
    else:
        return False


def monthToDate(month):

    """
    Convert month to date format.

    Keyword arguments:
    month -- the month to convert to date format
    """

    month = datetime.strptime(month, ("%Y-%m"))
    date = month.strftime("%Y-%m-%d")  # eg 2018-02-01
    date = datetime.strptime(date, ("%Y-%m-%d"))  # return datetime object

    return date


def incrementMonth(month, n=1):

    """
    Increment date by 'n' months.

    Keyword arguments:
    month -- the current set month
    n -- the number of months to increment (default is 1)
    """

    date = monthToDate(month)
    next_month = date + relativedelta.relativedelta(months=n)

    return next_month.strftime("%Y-%m-%d")


def decrementMonth(month, n=1):

    """
    Decrement date by 'n' months.

    Keyword arguments:
    month -- the current set month
    n -- the number of months to decrement (default is 1)
    """

    date = monthToDate(month)
    previous_month = date - relativedelta.relativedelta(months=n)

    return previous_month.strftime("%Y-%m-%d")


def dbHasMonth(month):

    """
    Check whether month has entries in the DB.

    Keyword arguments:
    month -- check if this month is in the db.json (DB)
    """

    stats = getStatsFromDb(month)
    # if there is at least one entry
    if len(stats) > 0:
        return True
    else:
        return False
