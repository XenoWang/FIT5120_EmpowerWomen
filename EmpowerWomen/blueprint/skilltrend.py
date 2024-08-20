from flask import Blueprint,render_template

skilltrend=Blueprint('skilltrend',__name__)

@skilltrend.route('/skilltrend')
def skill_trend_page():
    return render_template('SkillTrendPage.html')