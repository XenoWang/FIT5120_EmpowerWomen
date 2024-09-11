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

# Imports
from flask import Blueprint,render_template

privacy=Blueprint('privacy',__name__)

@privacy.route('/privacy')
def privacy_page():
    return render_template("PrivacyStatement.html")

