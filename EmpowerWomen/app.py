#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"


#< ------------------------------ 80 Char Limit ------------------------------ >

# Import init_app from plugins
from flask import Flask, jsonify
from flask_session import Session

from EmpowerWomen.plugins import db
from EmpowerWomen.blueprint import home, skills, trends, tests, privacy,terms,resume,skillass,skillmatching,quiz,recommendations
from EmpowerWomen.config import Config
from sqlalchemy import text
from flask_migrate import Migrate
import google.generativeai as genai
# Load Flask App
app = Flask(__name__)

# Load Config
app.config.from_object(Config)


# Configure the session to use filesystem (or Redis for production)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = './flask_session/'  # Where session files are stored
app.config['SESSION_FILE_THRESHOLD'] = 5

# Initialize session management
Session(app)
# Configure Gemini API key
genai.configure(api_key='AIzaSyAjlxhkIHcK1BcDhyFied9EDMz9iuaKrFY')

db.init_app(app)
migrate = Migrate(app,db)

# Initialize app and other plugins
# Register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)
app.register_blueprint(tests)
app.register_blueprint(terms)
app.register_blueprint(skillass)
app.register_blueprint(privacy)
app.register_blueprint(resume)
app.register_blueprint(skillmatching)

app.register_blueprint(recommendations)
app.register_blueprint(quiz)

# Declare variables
valid_tables = ['ANZSCO1', 'ANZSCO4', 'SPECIALIST', 'CORE_COMPETENCY', 'OCCUPATION_CORE_COMPETENCY']

def check_table_data(table_name):
    if table_name in valid_tables:
        try:
            records = db.session.execute(text(f'SELECT * FROM {table_name} LIMIT 5')).fetchall()

            if records:
                print(f"Table {table_name} is connected successfully. Here are some records:")
                for record in records:
                    print(record)
            else:
                print(f"Table {table_name} is connected successfully, but no records found.")
        except Exception as e:
            print(f"Failed to query table {table_name}: {str(e)}")
    else:
        print(f"{table_name} is not Allowed")

def test_db_connection():
    try:
        with app.app_context():
            print("Testing database connection and table data...")
            check_table_data('ANZSCO1')
            check_table_data('ANZSCO4')
            check_table_data('SPECIALIST')
            check_table_data('CORE_COMPETENCY')
            check_table_data('OCCUPATION_CORE_COMPETENCY')
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

# Main Function
if __name__ == '__main__':
    #test_db_connection()
    app.run(host='0.0.0.0') # Do not set Debug to True in Production
