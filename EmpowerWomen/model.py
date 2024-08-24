from flask_sqlalchemy import SQLAlchemy
#
# from plugins import db
#
# class ANZSCO1(db.Model):
#     __tablename__ = 'anzsco1'
#     ANZSCO1_CODE = db.Column(db.Integer, primary_key=True)
#     SECTION = db.Column(db.String(255), nullable=False)
#
#     anzsco4 = db.relationship('ANZSCO4', backref='anzsco1', lazy=True)
#
# class ANZSCO4(db.Model):
#     __tablename__ = 'anzsco4'
#     ANZSCO4_CODE = db.Column(db.Integer, primary_key=True)
#     ANZSCO1_CODE = db.Column(db.Integer, db.ForeignKey('anzsco1.ANZSCO1_CODE'), nullable=False)
#     TITLE = db.Column(db.String(255), nullable=False)
#
#     specialists = db.relationship('Specialist', backref='anzsco4', lazy=True)
#     occupation_core_competencies = db.relationship('OccupationCoreCompetency', backref='anzsco4', lazy=True)
#
# class Specialist(db.Model):
#     __tablename__ = 'specialist'
#     ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('anzsco4.ANZSCO4_CODE'), primary_key=True, nullable=False)
#     SPECIALIST_SKILL = db.Column(db.String(255), primary_key=True, nullable=False)
#     TIME_SPENT = db.Column(db.Numeric(5, 2), nullable=False)
#
# class CoreCompetency(db.Model):
#     __tablename__ = 'core_competency'
#     CORE_COMPETENCY = db.Column(db.String(255), primary_key=True, nullable=False)
#     CORE_COMPETENCY_DESC = db.Column(db.Text, nullable=True)
#     SCORE = db.Column(db.Integer, primary_key=True, nullable=False)
#     PROFICIENCY_LEVEL = db.Column(db.String(20), nullable=False)
#
#     occupation_core_competencies = db.relationship('OccupationCoreCompetency', backref='core_competency', lazy=True)
#
# class OccupationCoreCompetency(db.Model):
#     __tablename__ = 'occupation_core_competency'
#     ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('anzsco4.ANZSCO4_CODE'), primary_key=True, nullable=False)
#     CORE_COMPETENCY = db.Column(db.String(255), db.ForeignKey('core_competency.CORE_COMPETENCY'), primary_key=True, nullable=False)
#     SCORE = db.Column(db.Integer, db.ForeignKey('core_competency.SCORE'), primary_key=True, nullable=False)
#     ANCHOR_VALUE = db.Column(db.Text, nullable=True)
#     YEAR = db.Column(db.Integer, primary_key=True, nullable=False)
