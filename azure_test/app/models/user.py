#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
user
User モデル
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '30 03 2016'

from app import mongo


class User(mongo.Document):
    name = mongo.StringField()
    email = mongo.StringField()
    password = mongo.StringField()
