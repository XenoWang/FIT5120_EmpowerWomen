from flask import Blueprint, render_template, request, send_file
import io
import base64
import os
from random import choice
from PIL import Image, ImageDraw, ImageFont
import platform

resume = Blueprint('resume', __name__)

if platform.system() == 'Windows':
    font_path = 'arial.ttf'
else:
    font_path = 'DejaVuSans.ttf'

@resume.route('/ResumeGenerator')
def resume_page():
    return render_template("ResumeRefinement.html")
base_dir = os.getcwd()
#print(base_dir)
# Define a dictionary to store template-specific information
template_configs = {
    'Grey Modern Company Resume.jpg': {
        'image_path': os.path.join(os.getcwd(), 'EmpowerWomen', 'static', 'Image', 'GreyModernCompanyResume.jpg'),
        'text_position': (80, 750),
        'skill_position': (80, 1350),
        'hobby_position': (80, 1730),
        'font_path': font_path,
        'font_size': 23,
        'text_color': 'white',
        'max_width': 500,
        'skill_spacing': 50,
        'hobby_spacing': 50,
        'education_position': (750, 680),
        'edu_color': 'black'
    },
    'Pink White Clean Teacher Resume.jpg': {
        'image_path': os.path.join(os.getcwd(), 'EmpowerWomen', 'static', 'Image', 'PinkWhiteCleanTeacherResume.jpg'),
        'text_position': (620, 680),
        'skill_position': (90, 1700),
        'hobby_position': (90, 1050),
        'font_path': font_path,
        'font_size': 25,
        'text_color': 'black',
        'max_width': 600,
        'skill_spacing': 50,
        'hobby_spacing': 50,
        'education_position': (85, 1400),
        'edu_color': 'black'
    },
    'Pink Professional Business Administration Resume.jpg': {
        'image_path': os.path.join(os.getcwd(), 'EmpowerWomen', 'static', 'Image', 'PinkProfessionalBusinessAdministrationResume.jpg'),
        'text_position': (200, 800),
        'skill_position': (800, 1700),
        'hobby_position': (200, 1470),
        'font_path': font_path,
        'font_size': 21,
        'text_color': 'black',
        'max_width': 450,
        'skill_spacing': 50,
        'hobby_spacing': 35,
        'education_position': (190, 1700),
        'edu_color': 'black'
    }
    # Add more templates here
}

def load_descriptions_from_file(file_path):
    file_path = os.path.join(os.getcwd(), 'EmpowerWomen', 'documents', file_path)
    descriptions_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                key, description = line.split(':', 1)
                descriptions_dict[key.strip()] = description.strip()
            else:
                print(f"Skipping invalid line: {line}")
    return descriptions_dict


# 加载各类描述
hobbies_dict = load_descriptions_from_file('hobbies.txt')
personalities_dict = load_descriptions_from_file('personality.txt')
industries_dict = load_descriptions_from_file('industry.txt')
positions_dict = load_descriptions_from_file('positions.txt')
skills_dict = load_descriptions_from_file('skill.txt')
diploma_dict = load_descriptions_from_file('diplomas.txt')


def load_templates_from_file(file_path):
    templates = []
    if platform.system() == 'Windows':
        file_path = f'{os.getcwd()}\\EmpowerWomen\\documents\\{file_path}'
    else:
        file_path = f'{os.getcwd()}/EmpowerWomen/documents/{file_path}'
    with open(file_path, 'r', encoding='utf-8') as file:
        templates = file.read().split('---')
    return [template.strip() for template in templates]
def wrap_text(text, font, max_width):
    """
    Wraps text into multiple lines based on a maximum width.

    :param text: The text to wrap.
    :param font: The font used to measure the text width.
    :param max_width: The maximum width (in pixels) of a line of text.
    :return: The wrapped text with new lines inserted.
    """
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        # Measure the width of the current line using textbbox()
        text_width = font.getbbox(test_line)[2]  # getbbox returns a bounding box, [2] gives width
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())  # Save the current line
            current_line = word + " "  # Start a new line with the current word

    # Add the last line
    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)

# 模板读取函数不变
templates = load_templates_from_file('templates.txt')
@resume.route('/resumeresult', methods=['POST'])
def generate_resume():
    # Collect form data
    experience = request.form['experience']
    hobbies_input = request.form['hobbies']
    personality_input = request.form['personality']
    industry_input = request.form['industry']
    position_input = request.form['position']
    diploma = request.form['diploma']
    skills_input = request.form['skills']
    education_start = request.form['education_start']
    education_end = request.form['education_end']
    school = request.form['school']
    # Process input data
    hobbies = [hobby.strip().capitalize() for hobby in hobbies_input.split(',')]
    personalities = [personality.strip().capitalize() for personality in personality_input.split(',')]
    industries = [industry.strip().capitalize() for industry in industry_input.split(',')]
    positions = [position.strip().capitalize() for position in position_input.split(',')]
    skills = [skill.strip().capitalize() for skill in skills_input.split(',')]

    # Fetch descriptions
    hobby_description = ', '.join([hobbies_dict.get(hobby, "") for hobby in hobbies[:1]])
    personality_description = ', '.join([personalities_dict.get(personality, "") for personality in personalities[:1]])
    industry_description = industries_dict.get(industries[0], "") if industries else ""
    position_description = positions_dict.get(positions[0], "") if positions else ""

    skill_descriptions = [skills_dict.get(skill, "") for skill in skills[:5]]
    while len(skill_descriptions) < 5:
        skill_descriptions.append("")
    education_description = f"From {education_start} to {education_end}\n{diploma} at {school} "

    # Select a template and its configuration
    selected_template_name = choice(list(template_configs.keys()))
    config = template_configs[selected_template_name]

    # Randomly choose a resume text template
    template = choice(templates)

    # Generate the resume text
    generated_resume = template.format(
        years=experience,
        hobbies=hobby_description,
        personality=personality_description,
        industry=industry_description,
        position=position_description,
        diploma=diploma,
        skill1=skill_descriptions[0],
        skill2=skill_descriptions[1],
        skill3=skill_descriptions[2],
        skill4=skill_descriptions[3],
        skill5=skill_descriptions[4]
    )

    # Load the template image
    image_path = config['image_path']
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    education_position=config['education_position']
    # Define the font
    font = ImageFont.truetype(config['font_path'], size=config['font_size'])

    # Wrap the main text
    max_width = config['max_width']
    wrapped_text = wrap_text(generated_resume, font, max_width)

    # Draw the main text
    draw.text(config['text_position'], wrapped_text, font=font, fill=config['text_color'])
    draw.text(education_position, education_description, font=font, fill=config['edu_color'])

    # Draw the skills
    skill_position = config['skill_position']
    skill_spacing = config['skill_spacing']
    for skill in skills:
        draw.text(skill_position, skill, font=font, fill=config['text_color'])
        skill_position = (skill_position[0], skill_position[1] + skill_spacing)

    # Draw the hobbies
    hobby_position = config['hobby_position']
    hobby_spacing = config['hobby_spacing']
    for hobby in hobbies:
        draw.text(hobby_position, hobby, font=font, fill=config['text_color'])
        hobby_position = (hobby_position[0], hobby_position[1] + hobby_spacing)

    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='resume_image.jpg')

