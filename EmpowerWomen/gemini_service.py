import google.generativeai as genai
import json

# Configure the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})


def generate_quiz():
    prompt = '''
    Please create a competency-based quiz to assess individuals' skill levels based on the following core competencies:

Competencies:
- Digital Engagement
- Initiative and Innovation
- Learning
- Numeracy
- Oral Communication
- Planning and Organizing
- Problem Solving
- Reading
- Teamwork
- Writing

For each competency, provide 3 questions. Each question should have 4 multiple-choice options (A, B, C, D). Do not specify correct or incorrect answers, as the final score will be based on how well the answers align with the proficiency levels.

Example format:
Competency: Digital Engagement
Description: Identifying and using technology confidently and creatively.
Question 1: How do you typically interact with digital devices?
    A. Use only for basic tasks like messaging
    B. Use for work-related tasks occasionally
    C. Use confidently for a range of tasks
    D. Innovate with new technology tools

Score each competency from 1 to 10 based on the user's overall answers.


 Format the response as a JSON with the following schema:
    {
      "competency_name": "Competency Name",
      "description": "Description",
      "questions": [
        {
          "question": "Question text",
          "options": ["A", "B", "C", "D"]
        }
      ]
    }
    '''

    response = model.generate_content(prompt)
    json_strings = response.text.strip().splitlines()
    quiz_data = [json.loads(json_str) for json_str in json_strings]

    for competency_index, competency in enumerate(quiz_data):
        for question_index, question in enumerate(competency['questions']):
            question['question_index'] = f"competency_{competency_index}_question_{question_index}"

    return quiz_data


def grade_quiz(quiz_data, user_answers):
    prompt = prepare_prompt_for_gemini(quiz_data, user_answers)
    response = model.generate_content(prompt)
    return json.loads(response.text)


def prepare_prompt_for_gemini(quiz_data, user_answers):
    prompt = "Grade the following competency-based quiz based on the user's answers and provide proficiency levels:\n\n"

    for competency in quiz_data:
        prompt += f"Competency: {competency['competency_name']}\n"
        prompt += f"Description: {competency['description']}\n"
        for question in competency['questions']:
            question_key = question['question_index']  # Unique identifier for each question
            user_answer = user_answers.get(question_key)
            prompt += f"Question: {question['question']}\n"
            prompt += f"User Answer: {user_answer}\n"
        prompt += "\n"

    prompt += "\nScoring Standard:\n"
    scoring_standards = get_scoring_standards()

    for competency_name, scores in scoring_standards.items():
        prompt += f"{competency_name}:\n"
        for score_item in scores:
            prompt += f"Score: {score_item['Score']} - {score_item['Anchor Value']}\n"

    prompt += '''Please return the results in JSON format with score and proficiency.\n'''
    prompt += '''{
             "competency_name": {
                 "score": "numeric_value",
                 "proficiency": "proficiency_level"
             },
             "another_competency_name": {
                 "score": "numeric_value",
                 "proficiency": "proficiency_level"
             }
         }'''
    return prompt


def get_scoring_standards():
    file_path = 'score_standard.json'
    with open(file_path, 'r') as f:
        scoring_data = json.load(f)
    return scoring_data
