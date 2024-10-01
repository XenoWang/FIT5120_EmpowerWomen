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
from sqlalchemy import or_, func, desc

companydata=Blueprint('companydata',__name__)
searchdata = Blueprint('searchdata', __name__)
def define_top_15_companies():
    """
    Function to fetch the top 15 companies based on the average final score
    across the four categories.
    """

    # Query to group by company and calculate the average final score
    top_companies_query = db.session.query(
        CompanyCategoryFinalScores.COMPANY_NAME,
        func.avg(CompanyCategoryFinalScores.FINAL_SCORE).label('avg_final_score')
    ).group_by(CompanyCategoryFinalScores.COMPANY_NAME).order_by(
        desc('avg_final_score')
    ).limit(15)

    # Execute the query and get results
    top_companies = top_companies_query.all()

    # Prepare the data for each company with its categories and final score
    top_data = {}
    for company_name, avg_final_score in top_companies:
        # Query to get the categories and final scores for this company
        categories = CompanyCategoryFinalScores.query.filter_by(COMPANY_NAME=company_name).all()

        # Prepare the list of categories and final scores for each company
        top_data[company_name] = []
        for category_info in categories:
            top_data[company_name].append({
                "category": category_info.CATEGORY,
                "final_score": category_info.FINAL_SCORE
            })

    return top_data
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
@searchdata.route('/searchdata/top15', methods=['GET'])
def get_top_15_companies():
    # Call the function to get the top 15 companies with the average final score
    top_data = define_top_15_companies()  # Use the get_top_15_companies function you previously created

    # Return the top 15 companies in JSON format
    return jsonify(top_data), 200
