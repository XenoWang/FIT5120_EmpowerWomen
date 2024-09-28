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
from EmpowerWomen.gemini_service import get_session_occupation


careerpathway=Blueprint('careerpathway',__name__)

@careerpathway.route('/careerpathway')
def career_page():
    # Retrieve the occupation and section from the session
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    section_name = session.get('selected_section', 'No Section Selected')

    # Call your function to get the career pathway JSON
    career_pathway_data = get_session_occupation()  # Assuming this function works correctly and returns JSON

    # Convert the career pathway data to a JSON string to send to the front-end
    career_pathway_json = json.dumps(career_pathway_data)

    # Render the template and pass the occupation, section, and career pathway JSON
    return render_template("CareerPathway.html",
                           occupation=occupation,
                           section_name=section_name,
                           career_pathway_json=career_pathway_json)
