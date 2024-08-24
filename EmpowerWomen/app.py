from flask import Flask

from EmpowerWomen.blueprint import home, skills,trends

app = Flask(__name__)


#register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)

if __name__ == '__main__':
    app.run()
