from flask import Flask, jsonify

from EmpowerWomen.model import ANZSCO1
from plugins import init_app
#import init_app from plugins
from plugins import db
from blueprint import home, skills,trends
from config import Config

app = Flask(__name__)

#load config
app.config.from_object(Config)

init_app(app)
# initialize app and other plugins

#database connect url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://TP01Master:Pass!TP01@13.236.153.22:3306/TP01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)


@app.route('/anzsco1', methods=['GET'])
def get_anzsco1_data():
    try:
        records = ANZSCO1.query.all()
        result = []
        for record in records:
            result.append({
                'ANZSCO1_CODE': record.ANZSCO1_CODE,
                'SECTION': record.SECTION
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
