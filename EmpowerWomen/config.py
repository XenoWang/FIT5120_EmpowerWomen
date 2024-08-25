#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"

#< ------------------------------ 80 Char Limit ------------------------------ >

class Config:
    # Database Credentials
    DB_USER = 'TP01Master'
    DB_PASSWORD = 'Pass!TP01'
    DB_HOST = 'fit5120harmonyseekers.cz2s4m6aa5w7.ap-southeast-2.rds.amazonaws.com'
    DB_PORT = '3306'
    DB_NAME = 'TP01'

    # Construct the SQLAlchemy database URL
    DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = DB_URI

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
