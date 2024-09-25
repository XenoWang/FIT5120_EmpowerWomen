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
from flask_sqlalchemy import SQLAlchemy
from EmpowerWomen.plugins import db

class ANZSCO1(db.Model):
    """
    Class for the ANSZC01 Table
    """
    __tablename__ = 'ANZSCO1'
    ANZSCO1_CODE = db.Column(db.Integer, primary_key=True)
    SECTION = db.Column(db.String(255), nullable=False)

class ANZSCO4(db.Model):
    """
    Class for the ANSZC04 Table
    """
    __tablename__ = 'ANZSCO4'
    ANZSCO4_CODE = db.Column(db.Integer, primary_key=True)
    ANZSCO1_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO1.ANZSCO1_CODE'), nullable=False)
    TITLE = db.Column(db.String(255), nullable=False)

    # Relationship to ANZSCO1
    anzsco1 = db.relationship('ANZSCO1', backref=db.backref('anzsco4s', lazy=True))

class Specialist(db.Model):
    """
    Class for the SPECIALIST Table
    """
    __tablename__ = 'SPECIALIST'
    ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO4.ANZSCO4_CODE'), primary_key=True)
    SPECIALIST_SKILL = db.Column(db.String(255), primary_key=True)
    TIME_SPENT = db.Column(db.Numeric(5, 2), nullable=False)

    # Relationship to ANZSCO4
    anzsco4 = db.relationship('ANZSCO4', backref=db.backref('specialists', lazy=True))

class CoreCompetency(db.Model):
    """
    Class for the CORE_COMPETENCY Table
    """
    __tablename__ = 'CORE_COMPETENCY'
    CORE_COMPETENCY = db.Column(db.String(255), primary_key=True)
    CORE_COMPETENCY_DESC = db.Column(db.Text, nullable=True)
    SCORE = db.Column(db.Integer, primary_key=True)
    PROFICIENCY_LEVEL = db.Column(db.String(20), nullable=True)

class OccupationCoreCompetency(db.Model):
    """
    Class for the OCCUPATION_CORE_COMPETENCY Table
    """
    __tablename__ = 'OCCUPATION_CORE_COMPETENCY'
    ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO4.ANZSCO4_CODE'), primary_key=True)
    CORE_COMPETENCY = db.Column(db.String(255), db.ForeignKey('CORE_COMPETENCY.CORE_COMPETENCY'), primary_key=True)
    SCORE = db.Column(db.Integer, db.ForeignKey('CORE_COMPETENCY.SCORE'), primary_key=True)
    ANCHOR_VALUE = db.Column(db.Text, nullable=True)
    YEAR = db.Column(db.Integer, primary_key=True)

    # Relationships to ANZSCO4 and CoreCompetency with explicit foreign_keys
    anzsco4 = db.relationship('ANZSCO4', backref=db.backref('occupation_core_competencies', lazy=True))
    core_competency = db.relationship(
        'CoreCompetency',
        backref=db.backref('occupation_core_competencies', lazy=True),
        foreign_keys=[CORE_COMPETENCY]  # Specify explicit foreign key columns
    )

class Company(db.Model):
    __tablename__ = 'COMPANY'

    ABN = db.Column(db.String(11), primary_key=True)
    COMPANY_NAME = db.Column(db.String(255), nullable=False)
    GROUP_SIZE = db.Column(db.String(50))
    ANZSIC = db.Column(db.String(4))
    DIVISION_NAME = db.Column(db.String(255))

    # 关系定义
    employees = db.relationship('Employee', backref='company', lazy=True)
    questionnaires = db.relationship('CompanyQuestionnaire', backref='company', lazy=True)

class Questionnaire(db.Model):
    __tablename__ = 'QUESTIONNAIRE'

    QUESTION_INDEX = db.Column(db.String(50), primary_key=True)
    QUESTION_TEXT = db.Column(db.String(255), primary_key=True)
    UPPER_QUESTION_TEXT = db.Column(db.Text)
    RESPONSE_TYPE = db.Column(db.String(50))

    # 关系定义
    company_questionnaires = db.relationship('CompanyQuestionnaire', backref='questionnaire', lazy=True)

class CompanyQuestionnaire(db.Model):
    __tablename__ = 'COMPANY_QUESTIONNAIRE'

    ABN = db.Column(db.String(11), db.ForeignKey('COMPANY.ABN'), primary_key=True)
    QUESTION_INDEX = db.Column(db.String(50), db.ForeignKey('QUESTIONNAIRE.QUESTION_INDEX'), primary_key=True)
    QUESTION_TEXT = db.Column(db.String(255), db.ForeignKey('QUESTIONNAIRE.QUESTION_TEXT'), primary_key=True)
    RESPONSE = db.Column(db.String(10))

class Employee(db.Model):
    __tablename__ = 'EMPLOYEE'

    ABN = db.Column(db.String(11), db.ForeignKey('COMPANY.ABN'), primary_key=True)
    OCCUPATION = db.Column(db.String(40), primary_key=True)
    GENDER = db.Column(db.String(6), primary_key=True)
    EMPLOYMENT_STATUS = db.Column(db.String(15), primary_key=True)
    EMPLOYEE_NUMBER = db.Column(db.Integer)
