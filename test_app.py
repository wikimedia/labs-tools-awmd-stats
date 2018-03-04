# Author: Derick N. Alangi
# Unit tests for the application
# TODO: We intend to have 100% test coverage

import unittest
from flask import Flask
from app import *

class AppTestCase(unittest.TestCase):
	""" Tests for the application. """

	def setUp(self):
		self.app = app.test_client()

	# Test the / (index) route response status_code
	def test_index(self):
		response = self.app.get('/')
		self.assertEquals(response.status_code, 200)

	# Test the /test route response status_code
	def test_test(self):
		response = self.app.get('/test')
		self.assertEquals(response.status_code, 200)

	# Test the /raw/ route response status_code
	def test_raw_route(self):
		response = self.app.get('/raw/')
		self.assertEquals(response.status_code, 200)

	# Test the /raw/<month> route response status_code
	def test_raw_month_route(self):
		response = self.app.get('/raw/2018-01')
		self.assertEquals(response.status_code, 200)

	# Test the /month/<month> route response status_code
	def test_month_route(self):
		response = self.app.get('/month/2018-01')
		self.assertEquals(response.status_code, 200)

	# Test the /contributor/<username>/<month>
	def test_contributor_username_month_route(self):
		response = self.app.get('/contributor/d3r1ck01/2018-01')
		self.assertEquals(response.status_code, 200)


# Execute the unit tests
if __name__ == '__main__':
	unittest.main()