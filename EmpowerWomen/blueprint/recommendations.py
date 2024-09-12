from flask import Blueprint, render_template, session
from EmpowerWomen.plugins import db
from EmpowerWomen.model import OccupationCoreCompetency, ANZSCO4, ANZSCO1
recommendations = Blueprint('recommendations', __name__)

def match_industry_occupations(user_results):
    section_scores = {}

    # 存储每个 section 下的 occupations
    section_occupations = {}

    sections = db.session.query(ANZSCO1).all()

    for section in sections:
        anzsco4s = db.session.query(ANZSCO4).filter_by(ANZSCO1_CODE=section.ANZSCO1_CODE).all()

        section_total_scores = {}
        competency_count = 0

        for anzsco4 in anzsco4s:
            competencies = db.session.query(OccupationCoreCompetency).filter_by(
                ANZSCO4_CODE=anzsco4.ANZSCO4_CODE, YEAR=2023
            ).all()

            for competency in competencies:
                if competency.CORE_COMPETENCY not in section_total_scores:
                    section_total_scores[competency.CORE_COMPETENCY] = 0

                section_total_scores[competency.CORE_COMPETENCY] += competency.SCORE
                competency_count += 1

        if competency_count > 0:
            section_average_scores = {key: val / len(anzsco4s) for key, val in section_total_scores.items()}

            section_score_diff = 0
            matched_competencies = 0

            for competency_name, user_score in user_results.items():
                if competency_name in section_average_scores:
                    section_score_diff += abs(section_average_scores[competency_name] - float(user_score['score']))
                    matched_competencies += 1

            if matched_competencies > 0:
                section_scores[section.SECTION] = section_score_diff / matched_competencies

    sorted_sections = sorted(section_scores.items(), key=lambda x: x[1])
    top_sections = [section_name for section_name, _ in sorted_sections[:3]]

    # 保存每个 section 下的 top occupations
    for section_name in top_sections:
        section = db.session.query(ANZSCO1).filter_by(SECTION=section_name).first()
        anzsco4s = db.session.query(ANZSCO4).filter_by(ANZSCO1_CODE=section.ANZSCO1_CODE).all()

        occupation_scores = []

        for anzsco4 in anzsco4s:
            total_score_diff = 0
            competency_count = 0

            competencies = db.session.query(OccupationCoreCompetency).filter_by(
                ANZSCO4_CODE=anzsco4.ANZSCO4_CODE, YEAR=2023
            ).all()

            for competency in competencies:
                competency_name = competency.CORE_COMPETENCY
                user_score = user_results.get(competency_name, {}).get('score')
                if user_score is not None:
                    total_score_diff += abs(competency.SCORE - float(user_score))
                    competency_count += 1

            if competency_count > 0:
                avg_score_diff = total_score_diff / competency_count
                occupation_scores.append({
                    'occupation_title': anzsco4.TITLE,
                    'score_difference': avg_score_diff
                })

        top_occupations_for_section = sorted(occupation_scores, key=lambda x: x['score_difference'])[:5]

        # 将 occupation 列表存储在字典中，按 section 分组
        section_occupations[section_name] = [occ['occupation_title'] for occ in top_occupations_for_section]

    return {
        'top_sections': top_sections,
        'section_occupations': section_occupations
    }


@recommendations.route('/recommendations', methods=['POST'])
def view_recommendations():
    # Retrieve the quiz results from the session
    quiz_results = session.get('quiz_results')

    if not quiz_results:
        return "Error: No quiz results available for recommendations."

    # Match user scores with industries and occupations
    industry_recommendations = match_industry_occupations(quiz_results)
    #print(industry_recommendations)

    # Render the recommendations page
    return render_template('recommendations.html', industry_recommendations=industry_recommendations)