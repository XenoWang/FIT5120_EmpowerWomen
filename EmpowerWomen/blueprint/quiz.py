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
from flask import Blueprint, render_template, session, request
import io
import base64
import json

from EmpowerWomen.gemini_service import generate_quiz, grade_quiz

quiz=Blueprint('quiz',__name__)

# Home route to generate quiz questions and render quiz form
@quiz.route('/quiz')
def quiz_form():
    try:
        quiz_data = generate_quiz()  # Call the function to generate the quiz
        session['quiz_data'] = quiz_data
        session.modified = True  # Ensure Flask detects session modification

    except Exception as e:
        return f"Error generating quiz: {e}"

    # Render quiz on the page
    return render_template('Quiz.html', quiz_data=quiz_data)

# Route to handle quiz submission and return score
@quiz.route('/quizresult', methods=['POST'])
def submit_quiz():
    quiz_data = session.get('quiz_data')
    if not quiz_data:
        return "Error: No quiz data available for scoring."

    user_answers = request.form.to_dict()
    try:
        results = grade_quiz(quiz_data, user_answers)
        session['quiz_results']= results
    except Exception as e:
        return f"Error grading quiz: {e}"

    # Render the results page
    return render_template('QuizResult.html', results=results)