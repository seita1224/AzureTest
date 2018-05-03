#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
__init__.py
flask app
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '30 03 2016'

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api
from redis import Redis

sample = Flask(__name__)
redis = Redis()
mongo = MongoEngine(sample)
api = Api(sample)

import app.views
