#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author1__ = "Linhao Wang"
__email1__ = "lwan0191@student.monash.edu"
__author2__ = "Yuxiang Zou"
__email2__ = "yzou0027@student.monash.edu"
__author3__ = "Joshua Yu Xuan Soo"
__email3__ = "jsoo0027@student.monash.edu"

# < ------------------------------ 80 Char Limit ------------------------------ >

"""
Python Script for rendering the Resume Content Generator Page

"""

# Imports
from flask import Blueprint, render_template, request
import io
import base64
import os

from random import choice

resume = Blueprint('resume', __name__)


@resume.route('/ResumeGenerator')
def resume_page():
    return render_template("ResumePage.html")


# 读取一般描述
def load_descriptions_from_file(file_path):
    file_path = f'{os.getcwd()}\\EmpowerWomen\\documents\\{file_path}'
    descriptions_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                key, description = line.split(':', 1)  # 确保只分割一次
                descriptions_dict[key.strip()] = description.strip()
            else:
                # 跳过没有冒号的行，或者你可以记录这些行
                print(f"Skipping invalid line: {line}")
    return descriptions_dict


# 加载各类描述
hobbies_dict = load_descriptions_from_file('hobbies.txt')
personalities_dict = load_descriptions_from_file('personality.txt')
industries_dict = load_descriptions_from_file('industry.txt')
positions_dict = load_descriptions_from_file('positions.txt')
skills_dict = load_descriptions_from_file('skill.txt')
diploma_dict = load_descriptions_from_file('diplomas.txt')


def load_templates_from_file(file_path):
    """
    从文件中读取简历模板，将每个模板用 '---' 分隔，并返回模板列表。

    :param file_path: 模板文件路径
    :return: 模板列表
    """
    templates = []
    file_path = f'{os.getcwd()}\\EmpowerWomen\\documents\\{file_path}'
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取整个文件，并用 '---' 作为模板分隔符
        templates = file.read().split('---')

    # 去除每个模板前后的空白字符，并返回模板列表
    return [template.strip() for template in templates]


# 模板读取函数不变
templates = load_templates_from_file('templates.txt')


@resume.route('/resumeresult', methods=['POST'])
def generate_resume():
    # 从表单获取用户输入
    experience = request.form['experience']  # 获取用户工作年限
    hobbies_input = request.form['hobbies']  # 获取用户输入的爱好
    personality_input = request.form['personality']  # 获取性格
    industry_input = request.form['industry']  # 获取工作行业
    position_input = request.form['position']  # 获取职位
    diploma = request.form['diploma']  # 获取文凭
    skills_input = request.form['skills']  # 获取用户输入的技能

    # 处理爱好、性格、行业、职位和技能
    hobbies = [hobby.strip().capitalize() for hobby in hobbies_input.split(',')]
    personalities = [personality.strip().capitalize() for personality in personality_input.split(',')]
    industries = [industry.strip().capitalize() for industry in industry_input.split(',')]
    positions = [position.strip().capitalize() for position in position_input.split(',')]
    skills = [skill.strip().capitalize() for skill in skills_input.split(',')]

    # 获取各类描述，如果找不到对应的描述，保持为空白
    hobby_description = ', '.join([hobbies_dict.get(hobby, "") for hobby in hobbies[:1]])
    personality_description = ', '.join([personalities_dict.get(personality, "") for personality in personalities[:1]])
    industry_description = industries_dict.get(industries[0], "") if industries else ""
    position_description = positions_dict.get(positions[0], "") if positions else ""

    # 获取技能描述，最多处理5个技能
    skill_descriptions = [skills_dict.get(skill, "") for skill in skills[:5]]

    # 如果技能不足5个，用空白填充
    while len(skill_descriptions) < 5:
        skill_descriptions.append("")  # 用空字符串代替

    # 随机选择一个模板
    template = choice(templates)

    # 生成简历，替换模板中的占位符
    generated_resume = template.format(
        years=experience,
        hobbies=hobby_description,
        personality=personality_description,
        industry=industry_description,
        position=position_description,
        diploma=diploma,
        skill1=skill_descriptions[0],
        skill2=skill_descriptions[1],
        skill3=skill_descriptions[2],
        skill4=skill_descriptions[3],
        skill5=skill_descriptions[4]
    )

    return render_template('ResumeResult.html', resume=generated_resume)
