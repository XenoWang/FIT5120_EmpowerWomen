#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"

# < ------------------------------ 80 Char Limit ------------------------------ >

# Imports
from flask import Blueprint, render_template, request
import io
import base64

from random import choice

elevator = Blueprint('elevator', __name__)


@elevator.route('/elevator')
def resume_page():
    return render_template("ElevatorPitch.html")






def load_templates_from_file(file_path):
    """
    Read the resume templates from the file, separate each template with '-- ', and return the list of templates.

    param file_path: indicates the path of the template file
    :return: list of templates
    """
    templates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire file and use '-- 'as the template separator
        templates = file.read().split('---')

    # Remove the whitespace before and after each template and return a list of templates
    return [template.strip() for template in templates]
# The template read function is unchanged
templates = load_templates_from_file('EmpowerWomen/documents/templates.txt')


@elevator.route('/resumeresult', methods=['POST'])
def generate_resume():
    # Get user input from the form
    years = request.form['experience']  # Get user years of service
    hobbies = request.form['hobbies']  # Get user input for hobbies
    personality = request.form['personality']  # Acquire character
    industry = request.form['industry']  # Get a job industry
    position = request.form['position']  # Get a job
    diploma = request.form['diploma']  # Obtain a diploma
    school = request.form['school'] #Get user input schools
    skills = request.form['skills']  # Get user input skills







    # Select a template at random
    template = choice(templates)

    # Generate a resume and replace placeholders in the template
    generated_resume = template.format(
        years=years,
        hobbies=hobbies,
        personality=personality,
        industry=industry,
        position=position,
        diploma=diploma,
        skills=skills,
        school=school
    )

    return render_template('PitchResult.html', resume=generated_resume)