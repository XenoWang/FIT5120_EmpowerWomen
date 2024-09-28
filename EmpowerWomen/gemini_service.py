import google.generativeai as genai
import json
import os
import random
from flask import session
import re


def shuffle_and_relabel_options(question_data):
    # This function will handle shuffling the options and reassigning A, B, C, D labels
    for competency in question_data:
        for question in competency['questions']:
            # Extract only the text of the options (ignoring the A, B, C, D labels)
            options = [option.split('. ', 1)[1] for option in question['options']]

            # Shuffle the options randomly
            random.shuffle(options)

            # Relabel the shuffled options with new A, B, C, D labels
            relabeled_options = [f"{label}. {option}" for label, option in zip(['A', 'B', 'C', 'D'], options)]

            # Replace the question options with the shuffled and relabeled options
            question['options'] = relabeled_options


# Configure the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})


def generate_quiz():
    prompt = '''
    Write the response in British English. Use vocabulary, spelling, and grammatical structures that are common in British English (e.g., ‘colour’ instead of ‘color’, ‘organise’ instead of ‘organize’, ‘flat’ instead of ‘apartment’, etc.). Ensure that the entire response adheres to the conventions of British English.
    Please create a competency-based quiz to assess individuals' skill levels based on the following core competencies:

Competencies:
- Digital Engagement
- Initiative and Innovation
- Learning
- Numeracy
- Oral Communication
- Planning and Organising
- Problem Solving
- Reading
- Teamwork
- Writing

For each competency, provide 3 questions. Each question should have 4 multiple-choice options (A, B, C, D). Do not specify correct or incorrect answers, as the final score will be based on how well the answers align with the proficiency levels. Ensure that the answer options for each question are randomly shuffled.

Example format:
Competency: Digital Engagement
Description: Identifying and using technology confidently and creatively.
Question 1: How do you typically interact with digital devices?
    A. Use only for basic tasks like messaging
    B. Innovate with new technology tools
    C. Use confidently for a range of tasks
    D. Use for work-related tasks occasionally

Score each competency from 1 to 10 based on the user's overall answers.


 Format the response as a JSON with the following schema:
    {
      "competency_name": "Competency Name",
      "questions": [
        {
          "question": "Question text",
          "options": ["A", "B", "C", "D"]
        }
      ]
    }
    '''

    # Call to the AI model to generate the quiz content
    response = model.generate_content(prompt)
    json_strings = response.text.strip().splitlines()

    # Load the quiz data from the generated response
    quiz_data = [json.loads(json_str) for json_str in json_strings]

    # Shuffle and relabel options for each question
    shuffle_and_relabel_options(quiz_data)

    # Add unique question index to each question
    for competency_index, competency in enumerate(quiz_data):
        for question_index, question in enumerate(competency['questions']):
            question['question_index'] = f"competency_{competency_index}_question_{question_index}"

    return quiz_data


def grade_quiz(quiz_data, user_answers):
    prompt = prepare_prompt_for_gemini(quiz_data, user_answers)
    response = model.generate_content(prompt)
    return json.loads(response.text)


def prepare_prompt_for_gemini(quiz_data, user_answers):
    prompt = "Write the response in British English. Use vocabulary, spelling, and grammatical structures that are common in British English (e.g., ‘colour’ instead of ‘color’, ‘organise’ instead of ‘organize’, ‘flat’ instead of ‘apartment’, etc.). Ensure that the entire response adheres to the conventions of British English. Grade the following competency-based quiz based on the user's answers and provide proficiency levels:\n\n"

    for competency in quiz_data:
        prompt += f"Competency: {competency['competency_name']}\n"
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
    file_path = os.path.join(os.getcwd(), 'EmpowerWomen', 'score_standard.json')
    with open(file_path, 'r') as f:
        scoring_data = json.load(f)
    return scoring_data

def get_session_occupation():
    occupation = session.get('selected_occupation', 'No Occupation Selected')
    section_name = session.get('selected_section', 'No Section Selected')
    occupation_safe = json.dumps(occupation)
    section_name_safe = json.dumps(section_name)

    # Construct the query to ask Gemini
    question = f'''
    Gemini, can you provide a detailed future career pathway for a {occupation_safe} in the {section_name_safe} section?
    Make sure the JSON format is correct and remove spare line breaks and spaces. Please structure the response in a tree diagram format, with stages of the career, necessary skills, potential job titles, and possible transitions to other related roles. Return the results in JSON format: {{

      "response": {{
        "occupation": "{occupation}",
        "section": "{section_name}",
        "career_tree": {{
          "entry_level": {{
            "job_title": "Junior {occupation}",
            "skills": ["Basic programming knowledge (Java, Python, C++)", "Understanding of algorithms and data structures", "Basic debugging and testing skills", "Version control knowledge (e.g., Git)"],
            "next_steps": {{
              "mid_level": {{
                "job_title": "{occupation}",
                "skills": ["Proficiency in multiple programming languages", "Experience with software design patterns", "Collaborative development skills", "Ability to work on full-stack development"],
                "next_steps": {{
                  "senior_level": {{
                    "job_title": "Senior {occupation}",
                    "skills": ["Leadership and mentoring skills", "Advanced system architecture and design", "Project management and team collaboration", "Expertise in cloud services and infrastructure"],
                    "next_steps": {{
                      "management_path": {{
                        "job_title": "Engineering Manager",
                        "skills": ["Team management and leadership", "Budgeting and resource allocation", "Cross-departmental communication", "Strategic decision-making"],
                        "next_steps": {{
                          "executive": {{
                            "job_title": "CTO (Chief Technology Officer)",
                            "skills": ["Strategic vision for technology", "Executive-level communication", "Long-term technology planning", "Stakeholder management"]
                          }},
                          "director": {{
                            "job_title": "Director of Engineering",
                            "skills": ["Managing multiple teams", "Resource allocation and budgeting", "Defining long-term technical strategies", "Mentorship at a large scale"]
                          }}
                        }}
                      }},
                      "technical_path": {{
                        "job_title": "Principal Engineer",
                        "skills": ["Deep technical expertise in specific fields", "Leading innovation and R&D", "Mentoring other engineers", "Industry-level impact and recognition"],
                        "next_steps": {{
                          "architect": {{
                            "job_title": "Software Architect",
                            "skills": ["Architecting large-scale software systems", "Deep knowledge of design patterns and frameworks", "Cross-functional collaboration", "Long-term system planning"]
                          }},
                          "fellow": {{
                            "job_title": "Engineering Fellow",
                            "skills": ["Industry leadership in technology", "Driving long-term innovation", "Mentoring at a global scale", "Influence on company-wide architecture"]
                          }}
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''

    # Send the question to Gemini
    response = model.generate_content(question)

    # Attempt to parse the response
    try:
        json_response = json.loads(response.text)
        print("Parsed JSON Response:", json_response)
        return json_response
    except json.JSONDecodeError as e:
        print(f"Initial JSON parse failed: {e}. Attempting to clean the response...")

        # Clean the JSON string and try again
        cleaned_response = clean_json_string(response.text)
        print(f"Cleaned response text:\n{cleaned_response}")
        try:
            json_response = json.loads(cleaned_response)
            print("Parsed cleaned JSON Response:", json_response)
            return json_response
        except json.JSONDecodeError as e:
            print(f"Failed to parse cleaned JSON: {e}")
            return {"error": "Failed to parse response"}

def clean_json_string(json_string):
    # Remove any stray newlines or tabs that may have corrupted the JSON format
    json_string = json_string.replace('\n', '').replace('\t', '')

    # Attempt to fix any missing commas between JSON objects/arrays
    # Example: "}{" -> "},{"
    json_string = re.sub(r'}\s*{', '},{', json_string)

    # Fix any unbalanced brackets or quotes by checking if they are closed
    open_brackets = json_string.count('{') - json_string.count('}')
    if open_brackets > 0:
        # Add missing closing brackets
        json_string += '}' * open_brackets

    open_square_brackets = json_string.count('[') - json_string.count(']')
    if open_square_brackets > 0:
        # Add missing closing square brackets
        json_string += ']' * open_square_brackets

    # Return the cleaned string
    return json_string
