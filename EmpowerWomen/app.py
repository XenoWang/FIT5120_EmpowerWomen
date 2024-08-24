from flask import Flask
# from plugins import init_app
#import init_app from plugins

from EmpowerWomen.blueprint import home, skills,trends

app = Flask(__name__)

#
# init_app(app)
# initialize app and other plugins

#register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)




if __name__ == '__main__':
    app.run()
