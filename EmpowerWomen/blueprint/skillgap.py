import io
from flask import Response


from flask import Blueprint, render_template, request, redirect, url_for, flash, session,send_file
from wordcloud import WordCloud

from EmpowerWomen.model import ANZSCO4, OccupationCoreCompetency, Specialist

# Create Blueprint
skillgap = Blueprint('skillgap', __name__)

# Career match route to display the form and calculate the result
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from EmpowerWomen.model import ANZSCO4, OccupationCoreCompetency
from flask_sqlalchemy import SQLAlchemy

# Create Blueprint
skillgap = Blueprint('skillgap', __name__)

@skillgap.route('/SkillGap', methods=['GET', 'POST'])
def skill_gap_page():
    # 查询所有职业数据
    occupations = ANZSCO4.query.order_by(ANZSCO4.TITLE).all()

    selected_occupation_id = None
    competency_results = None
    selected_occupation = None
    wordcloud_path = None

    # 处理表单提交
    if request.method == 'POST':
        selected_occupation_id = request.form.get('occupation')
        user_results = session.get('quiz_results')  # 假设 quiz 结果存储在 session 中

        if not user_results:
            flash('No quiz results found. Please take the quiz first.')
            return redirect(url_for('skillgap.skill_gap_page'))

        # 将用户的 quiz_results 的 competency 转为小写
        user_results_lower = {key.lower(): value for key, value in user_results.items()}

        # 获取选定职业的 core competency 数据
        occupation_competencies = OccupationCoreCompetency.query.filter_by(
            ANZSCO4_CODE=selected_occupation_id, YEAR=2023).all()

        # 比较用户评分与职业要求
        competency_results = {}
        for competency in occupation_competencies:
            # 将数据库中的 competency 转为小写以匹配
            db_competency_lower = competency.CORE_COMPETENCY.lower()

            user_score = int(user_results_lower.get(db_competency_lower, {}).get('score', 0))
            required_score = competency.SCORE

            if user_score >= required_score:
                competency_results[competency.CORE_COMPETENCY] = "Meets Requirement"
            else:
                competency_results[competency.CORE_COMPETENCY] = f"Requires {required_score}, you have {user_score}"

        selected_occupation = ANZSCO4.query.get(selected_occupation_id).TITLE

        # 生成 Word Cloud
        wordcloud_path = generate_specialist_wordcloud(selected_occupation_id)

    # 渲染表单和结果
    return render_template('SkillGap.html',
                           occupations=occupations,
                           selected_occupation_id=selected_occupation_id,
                           competency_results=competency_results,
                           selected_occupation=selected_occupation,
                           wordcloud_path=wordcloud_path)
# 生成Word Cloud图像，不保存本地，直接传递图片数据
def generate_specialist_wordcloud(occupation_id):
    specialists = Specialist.query.filter_by(ANZSCO4_CODE=occupation_id).all()

    if not specialists:
        return None

    # 准备词云数据
    word_freq = {specialist.SPECIALIST_SKILL: float(specialist.TIME_SPENT) for specialist in specialists}

    # 生成词云
    wordcloud = WordCloud(width=800, height=400, background_color="white", max_words=50).generate_from_frequencies(word_freq)

    # 保存图片到内存并传递路径
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return img

# 动态生成图片并显示在前端
@skillgap.route('/wordcloud/<int:occupation_id>')
def wordcloud(occupation_id):
    wordcloud_img = generate_specialist_wordcloud(occupation_id)

    if wordcloud_img is None:
        return "No specialist tasks available for this occupation.", 404

    return Response(wordcloud_img, mimetype='image/png')