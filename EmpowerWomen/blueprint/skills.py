#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"

#< ------------------------------ 80 Char Limit ------------------------------ >

# Imports
from flask import Blueprint,render_template
import io
import base64

skills=Blueprint('skills',__name__)

@skills.route('/skills')
def skills_page():
    return render_template("SkillsPage.html")

