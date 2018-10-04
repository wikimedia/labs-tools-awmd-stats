#!/usr/bin/env python

# Author: Samuel Guebo, Derick Alangi
# Description: The main application layer
# License: MIT

from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from pprint import pprint

from awmdstats import utils


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    """

    app = Flask(__name__)

    @app.route('/month/<month>')
    @app.route('/')
    def index(month=None):
        """
        Default/Home page of the application/tool.

        Keyword arguments:
        month -- the default is the current month but can view previous months
        """
        if month is None:
            month = utils.getCurrentMonth()  # make month format human-readable
        monthID = month
        stats = utils.getStatsFromDb(month)
        contributors = utils.getContributors(stats)

        # check whether there are entries in db
        formatted = datetime.strptime(month, ('%Y-%m'))
        if utils.dbHasMonth(month) is True:
            return render_template(
                'index.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, monthID=monthID
            )
        else:
            return render_template(
                'loader.html', monthID=monthID,
                formatted=formatted.strftime('%B, %Y')
            )

    @app.route('/contributor/<username>/<month>')
    def contributorPatchesByMonth(username, month):
        """
        REST endpoint for list of contributor's patche(s).

        Keyword arguments:
        username -- the gerrit handle of the contributor
        month -- the month to fetch corresponding contributions
        """
        Submitter = utils.Query()
        db = utils.getDb()
        # filter by username
        patches = db.search(Submitter.username == username)
        # grab previous url from flask.request.referrer
        backUrl = request.referrer

        return render_template(
            'contributor.html', patches=patches,
            monthID=month, backUrl=backUrl
        )

    @app.route('/refresh/<month>')
    @app.route('/refresh/')
    def refreshStatsByMonth(month=None):
        """
        Force a deep refresh.

        Keyword arguments:
        month -- the month to perform a hard refresh (regenerate the data)
        """
        if month is None:
            month = utils.getCurrentMonth()  # make month format human-readable
        formatted = datetime.strptime(month, ('%Y-%m'))

        # Let loader handle the refreshing process as this is its purpose
        return render_template(
            'loader.html', monthID=month,
            formatted=formatted.strftime('%B, %Y')
        )

    @app.route('/raw/')
    @app.route('/raw/<month>')
    @app.before_first_request
    def raw(month=None):
        """
        Display Raw HTML stats.

        Keyword arguments:
        month -- the month to generate raw data, mainly JSON data
        """
        if month is None:
            month = utils.getCurrentMonth()

        # load and save contributors list
        contributors = utils.readContributorsFromFile()

        # loop through contributors
        for contributor in contributors:

            username = contributor['username']
            patches = utils.getContributorStats(username, month)

            # loop through contributor patches
            db = utils.getDb()
            for patch in patches:

                # prepare patch dictionary
                patch['username'] = username
                patch['name'] = contributor['name']
                patch['country'] = contributor['country']

                # make sure patch wasn't previously saved
                if not utils.patchExists(patch):
                    # persist patch to db
                    db.insert(patch)
                # update patch status
                else:
                    Patch = utils.Query()
                    db.update(
                        {'status': patch['status']},
                        (Patch.username == patch['username']) &
                        (Patch.created == patch['created'])
                    )

        stats = utils.getStatsFromDb(month)
        contributors = utils.getContributors(stats)
        formatted = datetime.strptime(month, ('%Y-%m'))

        return render_template(
            'stats.html', stats=stats, monthID=month,
            month=formatted.strftime('%B, %Y'), contributors=contributors
        )

    @app.template_filter()
    def datetimeformat(
        value,
        inFormat='%Y-%m-%d %H:%M:%S.000000000',
        outFormat='%Y-%m-%d, %H:%M'
    ):
        """
        Custom Flask filter for datetimeformating.

        Keyword arguments:
        value -- the actual date value gotten from the data
        inFormat -- input format of the value (date)
        outFormat -- output format of the value (date)
        """
        formattedString = datetime.strptime(value, inFormat)

        return formattedString.strftime(outFormat)  # simple formatting

    @app.route('/test')
    def sample_request():
        """Test API endpoint with hardcoded data."""
        pprint(utils.getContributorStats('D3r1ck01', '2018-02'))

        return ''

    @app.route('/docs/sitemap')
    def show_doc_sitemap():
        """Show documentation sitemap."""
        return render_template("docs/index.html")

    @app.route('/docs/<doc>')
    def show_doc(doc="sitemap"):
        """Show documentation for a particular module."""
        doc_list = [
            '__init__.html',
            'app.html',
            'conftest.html',
            'index.html',
            'manage.html',
            'settings.html',
            'test_app.html',
            'test_utils.html',
            'utils.html'
        ]

        if doc in doc_list:
            if doc == 'sitemap.html':
                return render_template('docs/' + doc)
            return render_template('docs/' + doc)
        else:
            return '[404] Doc Not Found'

    return app
