from flask import Blueprint,render_template

skillset=Blueprint('skillset',__name__)

@skillset.route('/skillset')
def skill_set_page():
    return render_template("SkillSetPage.html")