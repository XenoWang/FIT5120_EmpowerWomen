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
    # Query all occupation data
    occupations = ANZSCO4.query.order_by(ANZSCO4.TITLE).all()

    selected_occupation_id = None
    competency_results = None
    selected_occupation = None
    wordcloud_path = None

    # Process form submission
    if request.method == 'POST':
        selected_occupation_id = request.form.get('occupation')
        user_results = session.get('quiz_results')  # Assume that the quiz result is stored in the session

        if not user_results:
            flash('No quiz results found. Please take the quiz first.')
            return redirect(url_for('skillgap.skill_gap_page'))

        # Converts the competency of the user's quiz_results to lower case
        user_results_lower = {key.lower(): value for key, value in user_results.items()}

        # Get core competency data for selected occupations
        occupation_competencies = OccupationCoreCompetency.query.filter_by(
            ANZSCO4_CODE=selected_occupation_id, YEAR=2023).all()

        # Compare user ratings with job requirements
        competency_results = {}
        for competency in occupation_competencies:
            # Convert competency in the database to lowercase to match
            db_competency_lower = competency.CORE_COMPETENCY.lower()

            user_score = int(user_results_lower.get(db_competency_lower, {}).get('score', 0))
            required_score = competency.SCORE

            if user_score >= required_score:
                competency_results[competency.CORE_COMPETENCY] = "Meets Requirement ✅"
            else:
                competency_results[competency.CORE_COMPETENCY] = f"Requires {required_score}, you have {user_score}🚩"

        selected_occupation = ANZSCO4.query.get(selected_occupation_id).TITLE

        # Generate Word Cloud
        wordcloud_path = generate_specialist_wordcloud(selected_occupation_id)

    # Render the form and results
    return render_template('SkillGap.html',
                           occupations=occupations,
                           selected_occupation_id=selected_occupation_id,
                           competency_results=competency_results,
                           selected_occupation=selected_occupation,
                           wordcloud_path=wordcloud_path)
# Generate Word Cloud images, do not save local, directly transfer image data
def generate_specialist_wordcloud(occupation_id):
    specialists = Specialist.query.filter_by(ANZSCO4_CODE=occupation_id).all()

    if not specialists:
        return None

    # Prepare word cloud data
    word_freq = {specialist.SPECIALIST_SKILL: float(specialist.TIME_SPENT) for specialist in specialists}

    # Generating word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white", max_words=50).generate_from_frequencies(word_freq)

    # Save the image to memory and pass the path
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return img

# Dynamically generate images and display them on the front end
@skillgap.route('/wordcloud/<int:occupation_id>')
def wordcloud(occupation_id):
    wordcloud_img = generate_specialist_wordcloud(occupation_id)

    if wordcloud_img is None:
        return "No specialist tasks available for this occupation.", 404

    return Response(wordcloud_img, mimetype='image/png')