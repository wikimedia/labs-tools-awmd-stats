#!/usr/bin/env python3

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

        stats = utils.getStatsFromDb(month)
        contributors = utils.getContributors(stats, month)

        ChartData = []
        patchTotal = 0
        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        for contributor in contributors:
            patchTotal += len(contributor)
            entry = {"name": contributor[0]['username'],
                     "patches": str(len(contributor))}
            ChartData.append(entry)

        # URL scheme that the home button should use
        prot_scheme = "https" if not app.debug else "http"

        # check whether there are entries in db
        formatted = datetime.strptime(month, ('%Y-%m'))
        if utils.dbHasMonth(month) is True:
            return render_template(
                'index.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, monthID=month, data=ChartData,
                patchsum=patchTotal, refresh_month=month_refresh,
                scheme=prot_scheme
            )
        else:
            return render_template(
                'no-contributions.html', monthID=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh, scheme=prot_scheme
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

    @app.route('/docs/<doc>')
    def show_doc(doc="index.html"):
        """Show documentation for a particular module."""

        # grab all generated from directory
        doc_dir_path = "awmdstats/templates/docs"
        doc_list = utils.getDocList(doc_dir_path)

        doc_list = sorted(doc_list)  # sort alphabetically for sitemap output

        if doc in doc_list:
            return render_template('doc.html', template='docs/' + doc,
                                   doc_list=doc_list)
        else:
            notice_title = "No documentation"
            notice_desc = "Oops! no file " + doc + " found."

            return render_template('doc.html', template='404.html',
                                   notice_title=notice_title,
                                   notice_desc=notice_desc)

    @app.route('/month-rank/<month>')
    def rank_by_month(month=None):
        """
        REST endpoint for a list of contributors sorted by patche(s).

        Keyword arguments:
        month -- the month to fetch corresponding contributors to be sorted
        """
        if month is None:
            # get current month in format human-readable
            month = utils.getCurrentMonth()

        stats = utils.getStatsFromDb(month)
        contributors = utils.getContributors(stats, month)

        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        # check whether there are entries in db
        formatted = datetime.strptime(month, ('%Y-%m'))

        # grab previous url from flask.request.referrer
        backUrl = request.referrer

        if utils.dbHasMonth(month) is True:
            return render_template(
                'month.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, monthID=month, backUrl=backUrl,
                refresh_month=month_refresh
            )
        else:
            return render_template(
                'no-contributions.html', monthID=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh
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
                    db.update({'status': patch['status']},
                              (Patch.username == patch['username']) & (
                        Patch.created == patch['created']))

        stats = utils.getStatsFromDb(month)
        contributors = utils.getContributors(stats, month)
        formatted = datetime.strptime(month, ('%Y-%m'))

        ChartData = []
        patchTotal = 0
        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        for contributor in contributors:
            patchTotal += len(contributor)
            entry = {"name": contributor[0]['username'],
                     "patches": str(len(contributor))}
            ChartData.append(entry)

        if utils.dbHasMonth(month) is True:
            return render_template(
                'index.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, monthID=month, data=ChartData,
                patchsum=patchTotal, refresh_month=month_refresh
            )
        else:
            return render_template(
                'no-contributions.html', monthID=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh
            )

    @app.route('/test')
    def sample_request():
        """Test API endpoint with hardcoded data."""
        pprint(utils.getContributorStats('D3r1ck01', '2018-02'))

        return ''

    @app.context_processor
    def inject_current_year():
        return {'cYear': datetime.utcnow()}

    return app
