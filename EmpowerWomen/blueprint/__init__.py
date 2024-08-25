from flask import blueprints

from .skills import skills
from .trends import trends
from .home import home
from .tests import tests


def register_blueprints(app):
    app.register_blueprint(skills)
    app.register_blueprint(trends)
    app.register_blueprint(home)
    app.register_blueprint(tests)