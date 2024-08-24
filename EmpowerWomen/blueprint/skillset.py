from flask import Blueprint,render_template

skills=Blueprint('skills',__name__)

@skills.route('/skills')
def skills_page():
    return render_template("SkillsPage.html")