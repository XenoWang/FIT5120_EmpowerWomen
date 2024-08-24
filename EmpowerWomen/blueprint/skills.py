from flask import Blueprint,render_template
import io
import base64

from EmpowerWomen.model import ANZSCO1

skills=Blueprint('skills',__name__)

@skills.route('/skills')
def skills_page():
    return render_template("SkillsPage.html")

