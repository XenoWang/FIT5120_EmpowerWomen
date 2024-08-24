from flask import Blueprint,render_template

trends=Blueprint('trends',__name__)

@trends.route('/trends')
def trends_page():
    return render_template('TrendsPage.html')