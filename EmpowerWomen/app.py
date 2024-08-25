from flask import Flask, jsonify

from model import ANZSCO1
from plugins import init_app
#import init_app from plugins
from plugins import db
from blueprint import home, skills,trends
from config import Config
from sqlalchemy import text

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




def check_table_data(table_name):
    try:
        records = db.session.execute(text(f'SELECT * FROM {table_name} LIMIT 5')).fetchall()

        if records:
            print(f"Table {table_name} is connected successfully. Here are some records:")
            for record in records:
                print(record)
        else:
            print(f"Table {table_name} is connected successfully, but no records found.")
    except Exception as e:
        print(f"Failed to query table {table_name}: {str(e)}")


def test_db_connection():
    try:
        with app.app_context():
            print("Testing database connection and table data...")
            check_table_data('ANZSCO1')
            check_table_data('ANZSCO4')
            check_table_data('SPECIALIST')
            check_table_data('CORE_COMPETENCY')
            check_table_data('OCCUPATION_CORE_COMPETENCY')
    except Exception as e:
        print(f"Database connection failed: {str(e)}")


if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)
