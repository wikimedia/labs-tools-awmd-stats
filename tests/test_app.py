#!/usr/bin/env python3

# Author: Derick N. Alangi
# Unit tests for the routes in the application
# TODO: We intend to have 100% test coverage

import pytest


@pytest.mark.usefixtures('testapp')
class TestApp:
    """Test routes in the application."""

    #  Test the index( / ) route response status_code
    def test_index_route(self, testapp):
        response = testapp.get('/')
        assert response.status_code == 200

    #  Test the /docs/<doc> route response status_code
    def test_docs_doc_route(self, testapp):
        response = testapp.get('/docs/index')
        assert response.status_code == 200

    #  Test the /test route response status_code
    def test_test_route(self, testapp):
        response = testapp.get('/test')
        assert response.status_code == 200

    #  Test the /raw/ route response status_code
    def test_raw_route(self, testapp):
        response = testapp.get('/raw/')
        assert response.status_code == 200

    #  Test the /raw/<month> route response status_code
    def test_raw_month_route(self, testapp):
        response = testapp.get('/raw/2018-01')
        assert response.status_code == 200

    #  Test the /month/<month> route response status_code
    def test_month_month_route(self, testapp):
        response = testapp.get('/month/2018-01')
        assert response.status_code == 200

    #  Test the /month-rank/<month>/wiki route response status_code
    def test_rank_by_month_route_with_wiki_format(self, testapp):
        response = testapp.get('/month-rank/2018-01/wiki')
        assert response.status_code == 200

    #  Test the /month-rank/<month>/json route status_code
    def test_rank_by_month_route_with_json_format(self, testapp):
        response = testapp.get('/month-rank/2018-01/json')
        assert response.status_code == 200

    #  Test the /month-rank/<month> route response status_code
    def test_rank_by_month_route(self, testapp):
        response = testapp.get('/month-rank/2018-01')
        assert response.status_code == 200

    #  Test the /contributor/<username>/<month>
    def test_contributor_username_month_route(self, testapp):
        response = testapp.get('/contributor/D3r1ck01/2018-07')
        assert response.status_code == 200
