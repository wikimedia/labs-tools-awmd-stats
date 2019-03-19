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


def read_contributors_from_file():

    """Read through and get all contributors."""

    file = open('contributors.json', 'r')
    json_text = file.read()
    response = json.loads(json_text)

    return response


def get_contributor_stats(username, month=None):

    """
    Fetch Gerrit API for patch contributor data.

    Keyword arguments:
    username -- the gerrit handle of the contributor
    month -- the corresponding month to get contributor statistics
    """

    if month is None:
        date = get_current_month()
    else:
        date = month
    previous_month = decrement_month(date)
    next_month = increment_month(date)

    if username != '':
        link = 'https://gerrit.wikimedia.org/r/changes/?q=owner:'
        # build the API request url
        url = link + username + '+after:' + \
            previous_month + "+before:" + next_month
        r = requests.get(url)
        json_array = r.text
        # Fix this error in headers of json tree
        json_array = json_array.replace(")]}'", '', 1)

        return json.loads(json_array)


def get_current_month(formatted='%Y-%m'):

    """
    Get current month for a particular year.

    Keyword arguments:
    format -- the current month format to be used
    """

    current_month = time.strftime(formatted)  # e.g. 2018-02

    return current_month


def get_doc_list(path):

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


def get_stats_from_db(month):

    """
    Get monthly statistics from DB.

    Keyword arguments:
    month -- the month to get monthly stats from db.json
    """

    patch = Query()
    db = get_db()
    # stats = db.search(patch.created == month)
    stats = db.search(patch.created.test(filter_month, month))

    return stats


def get_db():

    """DB object to be used independently."""

    # setting the tinydb location
    db = TinyDB('database/db.json')

    return db


def get_contributors(stats, month):

    """
    Get the list of patch contributors.

    Keyword arguments:
    stats -- nested list of all patch contributors
    month -- the month used as the filter
    """
    contributors = []
    data = sorted(stats, key=lambda x: x['username'])

    # group contributions, list should be pre-sorted using same key
    for k, g in itertools.groupby(data, key=lambda x: x['username']):

        contributor_patches = list(g)

        patch = Query()
        db = get_db()

        # count status of patches
        merged_count = len(db.search((patch.status == 'MERGED') & (
            patch.username == k) & (patch.created.test(filter_month, month))))
        abandoned_count = len(db.search((patch.status == 'ABANDONED') & (
            patch.username == k) & (patch.created.test(filter_month, month))))
        pending_count = len(db.search((patch.status == 'NEW') & (
            patch.username == k) & (patch.created.test(filter_month, month))))

        metrics = {
            "merged_count": merged_count,
            "abandoned_count": abandoned_count,
            "pending_count": pending_count,
            "patch_total": merged_count + abandoned_count + pending_count
        }

        # add metrics to the first child
        contributor_patches[0] = dict(list(metrics.items()) + list(
            contributor_patches[0].items()))
        contributors.append(contributor_patches)  # build list

    # by default sort contributors by patch count, in descending order
    contributors = sorted(contributors, key=lambda x: x[0]['patch_total'],
                          reverse=True)

    return contributors


def filter_month(string, month):

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


def patch_exists(patch):

    """
    Check whether patch(es) exists in the DB.

    Keyword arguments:
    patch -- the patch(es) to be checked if it exist in db.json
    """

    db = get_db()
    query = Query()
    rows = db.search((query.created == patch['created']) & (
        query.username == patch['username']))

    # if the patch was previously saved
    if len(rows) > 0:
        return True
    else:
        return False


def month_to_date(month):

    """
    Convert month to date format.

    Keyword arguments:
    month -- the month to convert to date format
    """

    month = datetime.strptime(month, '%Y-%m')
    date = month.strftime('%Y-%m-%d')  # eg 2018-02-01
    date = datetime.strptime(date, '%Y-%m-%d')  # return datetime object

    return date


def increment_month(month, n=1):

    """
    Increment date by 'n' months.

    Keyword arguments:
    month -- the current set month
    n -- the number of months to increment (default is 1)
    """

    date = month_to_date(month)
    next_month = date + relativedelta.relativedelta(months=n)

    return next_month.strftime('%Y-%m-%d')


def decrement_month(month, n=1):

    """
    Decrement date by 'n' months.

    Keyword arguments:
    month -- the current set month
    n -- the number of months to decrement (default is 1)
    """

    date = month_to_date(month)
    previous_month = date - relativedelta.relativedelta(months=n)

    return previous_month.strftime('%Y-%m-%d')


def db_has_month(month):

    """
    Check whether month has entries in the DB.

    Keyword arguments:
    month -- check if this month is in the db.json (DB)
    """

    stats = get_stats_from_db(month)
    # if there is at least one entry
    if len(stats) > 0:
        return True
    else:
        return False
