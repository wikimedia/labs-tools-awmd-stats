#!/usr/bin/env python3

# Author: Samuel Guebo, Derick Alangi
# Description: The main application layer
# License: MIT

from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from pprint import pprint

from awmdstats import utils


def create_app():
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
            month = utils.get_current_month()  # month format human-readable

        stats = utils.get_stats_from_db(month)
        contributors = utils.get_contributors(stats, month)

        chart_data = []
        patch_total = 0
        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        for contributor in contributors:
            patch_total += len(contributor)
            entry = {"name": contributor[0]['username'],
                     "patches": str(len(contributor))}
            chart_data.append(entry)

        # URL scheme that the home button should use
        prot_scheme = "https" if not app.debug else "http"

        # check whether there are entries in db
        formatted = datetime.strptime(month, '%Y-%m')
        if utils.db_has_month(month) is True:
            return render_template(
                'index.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, month_id=month, data=chart_data,
                patchsum=patch_total, refresh_month=month_refresh,
                scheme=prot_scheme
            )
        else:
            return render_template(
                'no-contributions.html', month_id=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh, scheme=prot_scheme
            )

    @app.context_processor
    def utility_processor():
        def attach_badge(patch_count):
            if patch_count >= 100:
                badge = '🥇'
            elif patch_count >= 50:
                badge = '🥈'
            elif patch_count >= 10:
                badge = '🥉'
            else:
                badge = ''
            return badge
        return dict(attach_badge=attach_badge)

    @app.route('/contributor/<username>/<month>')
    def contributor_patches_by_month(username, month):
        """
        REST endpoint for list of contributor's patch(es).

        Keyword arguments:
        username -- the Gerrit handle of the contributor
        month -- the month to fetch corresponding contributions
        """
        submitter = utils.Query()
        db = utils.get_db()
        # filter by username
        patches = db.search(submitter.username == username)
        # grab previous url from flask.request.referrer
        back_url = request.referrer

        return render_template(
            'contributor.html', patches=patches,
            month_id=month, back_url=back_url
        )

    @app.template_filter()
    def datetimeformat(
        value,
        in_format='%Y-%m-%d %H:%M:%S.000000000',
        out_format='%Y-%m-%d, %H:%M'
    ):
        """
        Custom Flask filter for date-time formatting.

        Keyword arguments:
        value -- the actual date value gotten from the data
        inFormat -- input format of the value (date)
        outFormat -- output format of the value (date)
        """
        formatted_string = datetime.strptime(value, in_format)

        return formatted_string.strftime(out_format)  # simple formatting

    @app.route('/docs/<doc>')
    def show_doc(doc="index.html"):
        """Show documentation for a particular module."""

        # grab all generated from directory
        doc_dir_path = "awmdstats/templates/docs"
        doc_list = utils.get_doc_list(doc_dir_path)

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

    @app.route('/month-rank/<month>/<format>')
    @app.route('/month-rank/<month>')
    def rank_by_month(month=None, format=None):
        """
        REST endpoint for a list of contributors sorted by patche(s).

        Keyword arguments:
        month -- the month to fetch corresponding contributors to be sorted
        format -- the formats that the sorted data can be displayed in
        """
        if month is None:
            # get current month in format human-readable
            month = utils.get_current_month()

        stats = utils.get_stats_from_db(month)
        contributors = utils.get_contributors(stats, month)

        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        # check whether there are entries in db
        formatted = datetime.strptime(month, '%Y-%m')

        # grab previous url from flask.request.referrer
        back_url = request.referrer

        formats = ['wiki']
        if format is not None and format in formats:

            # build formatted list
            wikicode = ""
            for contributor in contributors:
                data = contributor[0]
                url_parts = request.url_root.split("/")
                base_url = "/".join(url_parts[0:len(url_parts) - 1])
                line = (['# @', data['username'], ' - [[',
                        base_url,
                        url_for('contributor_patches_by_month',
                                username=data['username'],
                                month=month),
                         '|(' + str(data['patch_total']),
                         ' patches submitted - ',
                         str(data['merged_count']),
                         ' merged, ' + str(data['pending_count']),
                         ' under review and ',
                         str(data['abandoned_count']),
                         ' abandoned)]]'
                         ]
                        )

                if format == 'wiki':
                    wikicode += "".join(line) + '\n'

            #  render raw text
            return wikicode, 200, {'Content-Type': 'text/css;'}

        if utils.db_has_month(month) is True:
            return render_template(
                'month.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, month_id=month, back_url=back_url,
                refresh_month=month_refresh
            )
        else:
            return render_template(
                'no-contributions.html', month_id=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh
            )

    @app.route('/raw/')
    @app.route('/raw/<month>')
    def raw(month=None):
        """
        Display Raw HTML stats.

        Keyword arguments:
        month -- the month to generate raw data, mainly JSON data
        """
        if month is None:
            month = utils.get_current_month()

        # load and save contributors list
        contributors = utils.read_contributors_from_file()

        # loop through contributors
        for contributor in contributors:

            username = contributor['username']
            patches = utils.get_contributor_stats(username, month)

            # loop through contributor patches
            db = utils.get_db()
            for patch in patches:

                # prepare patch dictionary
                patch['username'] = username
                patch['name'] = contributor['name']
                patch['country'] = contributor['country']

                # make sure patch wasn't previously saved
                if not utils.patch_exists(patch):
                    # persist patch to db
                    db.insert(patch)
                # update patch status
                else:
                    query = utils.Query()
                    db.update({'status': patch['status']},
                              (query.username == patch['username']) & (
                        query.created == patch['created']))

        stats = utils.get_stats_from_db(month)
        contributors = utils.get_contributors(stats, month)
        formatted = datetime.strptime(month, '%Y-%m')

        chart_data = []
        patch_total = 0
        if month in request.path:
            month_refresh = request.path.split('/')[-1]
        else:
            month_refresh = ''

        for contributor in contributors:
            patch_total += len(contributor)
            entry = {"name": contributor[0]['username'],
                     "patches": str(len(contributor))}
            chart_data.append(entry)

        if utils.db_has_month(month) is True:
            return render_template(
                'index.html', stats=stats, month=formatted.strftime('%B, %Y'),
                contributors=contributors, month_id=month, data=chart_data,
                patchsum=patch_total, refresh_month=month_refresh
            )
        else:
            return render_template(
                'no-contributions.html', month_id=month,
                formatted=formatted.strftime('%B, %Y'),
                refresh_month=month_refresh
            )

    @app.route('/test')
    def sample_request():
        """Test API endpoint with hardcoded data."""
        pprint(utils.get_contributor_stats('D3r1ck01', '2018-02'))

        return ''

    @app.context_processor
    def inject_current_year():
        return {'cYear': datetime.utcnow()}

    return app
