#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
__init__.py
api マッピング
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '30 03 2016'

from app import api
from app.views.user import UserView

api.add_resource(
    UserView,
    '/api/v1/users',
    '/api/v1/users/<int:id>'
)
