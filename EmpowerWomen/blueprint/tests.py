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
Page used for Developer Testing -- Unused Functionality

"""

# Imports
from flask import Blueprint, render_template, jsonify
from EmpowerWomen.model import ANZSCO1 ,db
import io
import base64

tests=Blueprint('tests',__name__)

@tests.route('/tests')
def tests_page():
    return render_template("Tests.html")


@tests.route('/api/anzsco1', methods=['GET'])
def get_anzsco1():
    # 查询所有 ANZSCO1 表的数据
    anzsco1_data = ANZSCO1.query.all()

    # 将查询结果转换为字典形式
    result = []
    for item in anzsco1_data:
        result.append({
            'ANZSCO1_CODE': item.ANZSCO1_CODE,
            'SECTION': item.SECTION
        })

    return jsonify(result)
