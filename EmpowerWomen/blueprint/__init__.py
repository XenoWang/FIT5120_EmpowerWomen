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
Python Script for initializing the libraries needed

"""

# Imports
from flask import blueprints
from .skills import skills
from .trends import trends
from .home import home
from .tests import tests
from .privacy import privacy
from .terms import terms
from .resume import resume
from .skillmatching import skillmatching
from .skillass import skillass
from .quiz import quiz
from .recommendations import recommendations
from .skillgap import skillgap
from .loading import loading
# Initializing Variables
imports = [skills, trends, home, tests, privacy, terms, resume, skillass,
           skillmatching, quiz, recommendations,skillgap,loading]

def register_blueprints(app):
    # Register all Blueprints
    for element in imports:
        app.register_blueprint(element)
