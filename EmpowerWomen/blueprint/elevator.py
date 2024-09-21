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
    从文件中读取简历模板，将每个模板用 '---' 分隔，并返回模板列表。

    :param file_path: 模板文件路径
    :return: 模板列表
    """
    templates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取整个文件，并用 '---' 作为模板分隔符
        templates = file.read().split('---')

    # 去除每个模板前后的空白字符，并返回模板列表
    return [template.strip() for template in templates]
# 模板读取函数不变
templates = load_templates_from_file('EmpowerWomen/documents/templates.txt')


@elevator.route('/resumeresult', methods=['POST'])
def generate_resume():
    # 从表单获取用户输入
    years = request.form['experience']  # 获取用户工作年限
    hobbies = request.form['hobbies']  # 获取用户输入的爱好
    personality = request.form['personality']  # 获取性格
    industry = request.form['industry']  # 获取工作行业
    position = request.form['position']  # 获取职位
    diploma = request.form['diploma']  # 获取文凭
    school = request.form['school']
    skills = request.form['skills']  # 获取用户输入的技能







    # 随机选择一个模板
    template = choice(templates)

    # 生成简历，替换模板中的占位符
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

    return render_template('ResumeResult.html', resume=generated_resume)