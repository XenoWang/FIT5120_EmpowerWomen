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
from flask import Blueprint,render_template,request,session, jsonify
import io
import base64
import json
from EmpowerWomen.plugins import db
from EmpowerWomen.model import CompanyCategoryFinalScores
from sqlalchemy import or_

companydata=Blueprint('companydata',__name__)
searchdata = Blueprint('searchdata', __name__)

@companydata.route('/companydata')
def company_page():
    # Get the section name from the session
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    # Print the section name to the console
    print(f"Selected Occupation: {occupation}")
    # Render the CompanyData.html template with the section name
    return render_template("CompanyData.html", Occupation=occupation)

@searchdata.route('/searchdata', methods=['POST'])
def search():
    search_query = request.form.get('search_query')

    # Log the search input in the console for debugging (optional)
    print(f"Search Query: {search_query}")

    # Perform a fuzzy search using the SQL LIKE operator for partial matches
    results = CompanyCategoryFinalScores.query.filter(
        CompanyCategoryFinalScores.COMPANY_NAME.ilike(f"%{search_query}%")
    ).all()

    # If no results found, return a 404
    if not results:
        return jsonify({"error": "No matching company found."}), 404

    response_data = {}
    for result in results:
        company_name = result.COMPANY_NAME
        category = result.CATEGORY
        final_score = result.FINAL_SCORE

        # If the company name is not already in the dictionary, add it
        if company_name not in response_data:
            response_data[company_name] = []

        # Append the category and final score to the company's list
        response_data[company_name].append({
            "category": category,
            "final_score": final_score
        })

    # Return the search results in JSON format
    return jsonify(response_data), 200
