#!/usr/bin/env python

# Author: Derick N. Alangi

class Config(object):
    # The config class
    SECRET_KEY = ''

class ProdConfig(Config):
    ENV = 'prod'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
