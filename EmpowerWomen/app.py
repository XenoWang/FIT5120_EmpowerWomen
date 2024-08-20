from flask import Flask

from EmpowerWomen.blueprint import home, skillset,skilltrend

app = Flask(__name__)


#register all blueprints
app.register_blueprint(home)
app.register_blueprint(skillset)
app.register_blueprint(skilltrend)

if __name__ == '__main__':
    app.run()
