from flask import Blueprint, render_template, jsonify
import io
import base64
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
