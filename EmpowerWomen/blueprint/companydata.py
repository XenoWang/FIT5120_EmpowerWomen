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
from flask import Blueprint,render_template,request,session
import io
import base64
import json


companydata=Blueprint('companydata',__name__)
searchdata = Blueprint('searchdata', __name__)

@companydata.route('/companydata')
def company_page():
    # Get the section name from the session
    section_name = session.get('selected_section', 'No section selected')
    # Print the section name to the console
    print(f"Selected section: {section_name}")
    # Render the CompanyData.html template with the section name
    return render_template("CompanyData.html", section_name=section_name)

@searchdata.route('/searchdata', methods=['POST'])
def search():
    search_query = request.form.get('search_query')

    # Log the search input in the console for debugging (optional)
    print(f"Search Query: {search_query}")

    # Return only the user input (no additional text)
    return search_query, 200

