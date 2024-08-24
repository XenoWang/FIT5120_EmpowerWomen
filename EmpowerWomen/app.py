from flask import Flask
# from plugins import init_app
#import init_app from plugins

from EmpowerWomen.blueprint import home, skills,trends

app = Flask(__name__)

#
# init_app(app)
# initialize app and other plugins

#database connect url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://TP01Master:Pass!TP01@13.236.153.22:3306/TP01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)




if __name__ == '__main__':
    app.run()
