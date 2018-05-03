#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
user.py
user api
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '30 03 2016'


from flask.ext.restful import Resource
from app.models.user import User


class UserView(Resource):

    def get(self, id=None):
        l = User.objects()
        print(l)
        return 'get'

    def post(self):
        return 'post'

    def put(self, id):
        return 'put'

    def delete(self, id):
        return 'delete'
