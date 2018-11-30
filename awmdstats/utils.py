#!/usr/bin/env python3

# Authors:  Derick N. Alangi,
#           Samuel Guebo

import itertools
import json
import os
import requests
import time

from dateutil import relativedelta
from datetime import datetime
from tinydb import TinyDB
from tinydb import Query

"""
Utility functions to perform specific tasks for the app.
"""


def readContributorsFromFile():

    """Read through and get all contributors."""

    file = open('contributors.json', 'r')
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

    if username != '':
        link = 'https://gerrit.wikimedia.org/r/changes/?q=owner:'
        # build the API requst url
        url = link + username + '+after:' + \
            previous_month + "+before:" + next_month
        r = requests.get(url)
        jsonArray = r.text
        # Fix this error in headers of json tree
        jsonArray = jsonArray.replace(")]}'", '', 1)

        return json.loads(jsonArray)


def getCurrentMonth(format='%Y-%m'):

    """
    Get current month for a particular year.

    Keyword arguments:
    format -- the current month format to be used
    """

    currentMonth = time.strftime(format)  # e.g. 2018-02

    return currentMonth


def getDocList(path):

    """
    Get the generated documentation files as a list

    Keyword arguments:
    directory -- the path to the directory containing generated doc files
    """

    doc_list = []

    # get all HTML files
    for doc in os.listdir(path):
        doc_list.append(doc)

    return doc_list


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


def getContributors(stats, month):

    """
    Get the list of patch contributors.

    Keyword arguments:
    stats -- nested list of all patch contributors
    month -- the month used as the filter
    """
    data = []
    contributors = []
    data = sorted(stats, key=lambda x: x['username'])

    # group contributions, list should be pre-sorted using same key
    for k, g in itertools.groupby(data, key=lambda x: x['username']):

        contributor_patches = list(g)

        # prepare metrics
        merged_count = abandoned_count = pending_count = 0

        Patch = Query()
        db = getDb()

        # count status of patches
        merged_count = len(db.search((Patch.status == 'MERGED') & (
            Patch.username == k) & (Patch.created.test(filterMonth, month))))
        abandoned_count = len(db.search((Patch.status == 'ABANDONED') & (
            Patch.username == k) & (Patch.created.test(filterMonth, month))))
        pending_count = len(db.search((Patch.status == 'NEW') & (
            Patch.username == k) & (Patch.created.test(filterMonth, month))))

        metrics = {
            "merged_count": merged_count,
            "abandoned_count": abandoned_count,
            "pending_count": pending_count,
            "patch_total": merged_count + abandoned_count + pending_count
        }

        # add metrics to the first child
        contributor_patches[0] = dict(list(metrics.items()) + list(
            contributor_patches[0].items()))
        contributors.append(contributor_patches)  # Store group iterator as a list

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
    rows = db.search((Patch.created == patch['created']) & (
        Patch.username == patch['username']))

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

    month = datetime.strptime(month, ('%Y-%m'))
    date = month.strftime('%Y-%m-%d')  # eg 2018-02-01
    date = datetime.strptime(date, ('%Y-%m-%d'))  # return datetime object

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

    return next_month.strftime('%Y-%m-%d')


def decrementMonth(month, n=1):

    """
    Decrement date by 'n' months.

    Keyword arguments:
    month -- the current set month
    n -- the number of months to decrement (default is 1)
    """

    date = monthToDate(month)
    previous_month = date - relativedelta.relativedelta(months=n)

    return previous_month.strftime('%Y-%m-%d')


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
