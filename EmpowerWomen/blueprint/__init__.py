from flask import blueprints

from .skills import skills
from .trends import trends
from .home import home


def register_blueprints(app):
    app.register_blueprint(skills)
    app.register_blueprint(trends)
    app.register_blueprint(home)