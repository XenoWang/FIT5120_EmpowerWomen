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
import os


careerpathway=Blueprint('careerpathway',__name__)

# Dictionary of sector names (all in lowercase) and corresponding image file names
sector_images = {
    'managers': 'managers.jpg',
    'professionals': 'professionals.jpg',
    'technicians and trades workers': 'technicians_trades.jpg',
    'community and personal service workers': 'community_service.jpg',
    'clerical and administrative workers': 'clerical_administrative.jpg',
    'sales workers': 'sales_workers.jpg',
    'machinery operators and drivers': 'machinery_operators.jpg',
    'labourers': 'labourers.jpg'
}

# Function to get the correct image path based on the OS and sector
def get_image_path(sector):
    # Base directory for the images
    base_dir = os.path.join('static', 'Image')

    # Retrieve the image filename from the dictionary
    image_filename = sector_images.get(sector)

    # If the sector is valid and has an associated image
    if image_filename:
        # Join the base directory with the image filename
        image_path = os.path.join(base_dir, image_filename)
        return image_path
    else:
        # Return None or a default image path if the sector is invalid
        return None

@careerpathway.route('/careerpathway')
def career_page():
    # Retrieve the occupation and section from the session
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    section_name = session.get('selected_section', 'No Section Selected')
    section_image_path = get_image_path(section_name.lower())
    session['sector_name'] = section_name

    # Call your function to get the career pathway JSON
    career_pathway_data = get_session_occupation()  # Assuming this function works correctly and returns JSON

    # Convert the career pathway data to a JSON string to send to the front-end
    career_pathway_json = json.dumps(career_pathway_data)

    # Render the template and pass the occupation, section, and career pathway JSON
    return render_template("CareerPathway.html",
                           occupation=occupation,
                           section_name=section_name,
                           career_pathway_json=career_pathway_json,
                           section_image_path=section_image_path)
