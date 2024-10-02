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
from flask import Blueprint, render_template, request, session, jsonify
from EmpowerWomen.plugins import db
from EmpowerWomen.model import CompanyCategoryFinalScores, Company, Employee
from sqlalchemy import or_, func, desc

companydata = Blueprint('companydata', __name__)
searchdata = Blueprint('searchdata', __name__)

from decimal import Decimal

def define_top_15_companies():
    """
    Function to fetch the top 15 companies based on the average final score
    across the four categories and include additional employee details.
    """

    top_companies_query = db.session.query(
        CompanyCategoryFinalScores.COMPANY_NAME,
        Company.ABN,
        Company.GROUP_SIZE,
        func.avg(CompanyCategoryFinalScores.FINAL_SCORE).label('avg_final_score')
    ).join(Company).group_by(CompanyCategoryFinalScores.COMPANY_NAME, Company.ABN, Company.GROUP_SIZE).order_by(
        desc('avg_final_score')
    ).limit(15)

    top_companies = top_companies_query.all()

    top_data = {}
    for company_name, abn, group_size, avg_final_score in top_companies:
        categories = CompanyCategoryFinalScores.query.filter_by(COMPANY_NAME=company_name).all()

        employees = Employee.query.filter_by(ABN=abn).all()

        occupations = {}
        gender_count = {'Men': 0, 'Women': 0}
        employment_status_count = {'Full-time': 0, 'Part-time': 0, 'Casual': 0}

        for employee in employees:
            if employee.OCCUPATION not in occupations:
                occupations[employee.OCCUPATION] = 0
            occupations[employee.OCCUPATION] += employee.EMPLOYEE_NUMBER

            if employee.GENDER in gender_count:
                gender_count[employee.GENDER] += employee.EMPLOYEE_NUMBER

            if employee.EMPLOYMENT_STATUS in employment_status_count:
                employment_status_count[employee.EMPLOYMENT_STATUS] += employee.EMPLOYEE_NUMBER

        # Convert Decimal to float or str
        top_data[company_name] = {
            "group_size": group_size,
            "average_final_score": float(avg_final_score) if isinstance(avg_final_score, Decimal) else avg_final_score,
            "categories": [
                {
                    "category": category_info.CATEGORY,
                    "final_score": category_info.FINAL_SCORE
                }
                for category_info in categories
            ],
            "occupations": occupations,
            "gender_count": gender_count,
            "employment_status_count": employment_status_count
        }

    print(top_data)
    return top_data

@companydata.route('/companydata')
def company_page():
    # Get the occupation name from the session
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    # Print the occupation to the console for debugging
    print(f"Selected Occupation: {occupation}")
    # Render the CompanyData.html template with the occupation name
    return render_template("CompanyData.html", Occupation=occupation)

@searchdata.route('/searchdata', methods=['POST'])
def search():
    search_query = request.form.get('search_query')

    # Log the search input in the console for debugging (optional)
    print(f"Search Query: {search_query}")

    # Perform a fuzzy search using the SQL LIKE operator for partial matches
    search_results = db.session.query(
        CompanyCategoryFinalScores.COMPANY_NAME,
        Company.ABN,
        Company.GROUP_SIZE,
        func.avg(CompanyCategoryFinalScores.FINAL_SCORE).label('avg_final_score')
    ).join(Company).filter(
        CompanyCategoryFinalScores.COMPANY_NAME.ilike(f"%{search_query}%")
    ).group_by(CompanyCategoryFinalScores.COMPANY_NAME, Company.ABN, Company.GROUP_SIZE).all()

    # If no results found, return a 404
    if not search_results:
        return jsonify({"error": "No matching company found."}), 404

    response_data = {}
    for company_name, abn, group_size, avg_final_score in search_results:
        # Query to get the categories and final scores for this company
        categories = CompanyCategoryFinalScores.query.filter_by(COMPANY_NAME=company_name).all()

        # Query to get employee data for the current company
        employees = Employee.query.filter_by(ABN=abn).all()

        # Aggregating employee data by occupation, gender, and employment status
        occupations = {}
        gender_count = {'Men': 0, 'Women': 0}
        employment_status_count = {'Full-time': 0, 'Part-time': 0, 'Casual': 0}

        for employee in employees:
            if employee.OCCUPATION not in occupations:
                occupations[employee.OCCUPATION] = 0
            occupations[employee.OCCUPATION] += employee.EMPLOYEE_NUMBER

            if employee.GENDER in gender_count:
                gender_count[employee.GENDER] += employee.EMPLOYEE_NUMBER

            if employee.EMPLOYMENT_STATUS in employment_status_count:
                employment_status_count[employee.EMPLOYMENT_STATUS] += employee.EMPLOYEE_NUMBER

        # Convert Decimal to float or str
        response_data[company_name] = {
            "group_size": group_size,
            "average_final_score": float(avg_final_score) if isinstance(avg_final_score, Decimal) else avg_final_score,
            "categories": [
                {
                    "category": category_info.CATEGORY,
                    "final_score": category_info.FINAL_SCORE
                }
                for category_info in categories
            ],
            "occupations": occupations,
            "gender_count": gender_count,
            "employment_status_count": employment_status_count
        }

    # Return the search results in JSON format
    print(response_data)
    return jsonify(response_data), 200


@searchdata.route('/searchdata/top15', methods=['GET'])
def get_top_15_companies():
    # Call the function to get the top 15 companies with the average final score and additional data
    top_data = define_top_15_companies()

    # Return the top 15 companies in JSON format
    return jsonify(top_data), 200

