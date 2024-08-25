from flask import Blueprint, render_template, jsonify
import io
import base64
import os
import sys

# Add the directory containing EmpowerWomen to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)


from EmpowerWomen.model import ANZSCO1 ,db


tests=Blueprint('tests',__name__)

@tests.route('/tests')
def tests_page():
    return render_template("TestsPage.html")


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
