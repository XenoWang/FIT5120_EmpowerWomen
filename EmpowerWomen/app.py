from flask import Flask, jsonify

# import init_app from plugins
from EmpowerWomen.plugins import db
from EmpowerWomen.blueprint import home, skills, trends, tests
from EmpowerWomen.config import Config
from sqlalchemy import text
from flask_migrate import Migrate
app = Flask(__name__)

# load config
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app,db)

# initialize app and other plugins


# register all blueprints
app.register_blueprint(home)
app.register_blueprint(skills)
app.register_blueprint(trends)
app.register_blueprint(tests)


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
