#!/usr/bin/env python3

# Author: Derick N. Alangi
# Work in Progress


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
