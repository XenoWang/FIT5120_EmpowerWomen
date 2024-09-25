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
Python Script for rendering the Skill Assessment Page

"""

# Imports
from flask import Blueprint,render_template,session
import io
import base64
import json


careerpathway=Blueprint('careerpathway',__name__)

@careerpathway.route('/careerpathway')
def career_page():
    # Retrieve the occupation and section from the session
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    section_name = session.get('selected_section', 'No Section Selected')

    # Render the CareerPathway.html template, passing the occupation and section
    return render_template("CareerPathway.html", occupation=occupation, section_name=section_name)