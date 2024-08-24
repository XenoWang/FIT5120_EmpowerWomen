from flask import Blueprint,render_template
from wordcloud import WordCloud
import io
import base64
skills=Blueprint('skills',__name__)

@skills.route('/skills')
def skills_page():
    return render_template("SkillsPage.html")

