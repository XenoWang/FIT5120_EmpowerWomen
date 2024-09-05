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
from flask import blueprints
from .skills import skills
from .trends import trends
from .home import home
from .tests import tests
from .privacy import privacy
from .terms import terms
from .resumerefinement import resumerefinement
from .skillmatching import skillmatching
from .skillass import skillass

def register_blueprints(app):
    app.register_blueprint(skills)
    app.register_blueprint(trends)
    app.register_blueprint(home)
    app.register_blueprint(tests)
    app.register_blueprint(privacy)
    app.register_blueprint(terms)
    app.register_blueprint(resumerefinement)
    app.register_blueprint(skillass)
    app.register_blueprint(skillmatching)