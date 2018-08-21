#!/usr/bin/env python

# Author: Derick N. Alangi
# Unit tests for the routes in the application
# TODO: We intend to have 100% test coverage

import pytest


@pytest.mark.usefixtures("testapp")
class TestApp:
    """Test routes in the application."""

    #  Test the / (index) route response status_code
    def test_index_route(self, testapp):
        response = testapp.get('/')
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

    #  Test the /contributor/<username>/<month>
    def test_contributor_username_month_route(self, testapp):
        response = testapp.get('/contributor/D3r1ck01/2018-07')
        assert response.status_code == 200

    #  Test the /refresh/ route response status_code
    def test_refresh_route(self, testapp):
        response = testapp.get('/refresh/')
        assert response.status_code == 200

    #  Test the /refresh/<month> route response status_code
    def test_refresh_month_route(self, testapp):
        response = testapp.get('/refresh/2018-01')
        assert response.status_code == 200
