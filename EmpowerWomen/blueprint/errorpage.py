#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"

#< ------------------------------ 80 Char Limit ------------------------------ >

"""
Python Script for rendering the Privacy Policy

"""

from flask import Blueprint, render_template

# Define a Blueprint
errorpage = Blueprint('errorpage', __name__)

# Error handler, note that you need to receive the error parameter e
@errorpage.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@errorpage.app_errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 400

