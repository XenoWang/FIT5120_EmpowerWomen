from flask import blueprints

from .skillset import skillset
from .skilltrend import skilltrend
from .home import home


def register_blueprints(app):
    app.register_blueprint(skillset)
    app.register_blueprint(skilltrend)
    app.register_blueprint(home)