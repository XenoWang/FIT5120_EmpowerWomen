from flask_sqlalchemy import SQLAlchemy

from EmpowerWomen.plugins import db

class ANZSCO1(db.Model):
    __tablename__ = 'ANZSCO1'
    ANZSCO1_CODE = db.Column(db.Integer, primary_key=True)
    SECTION = db.Column(db.String(255), nullable=False)

class ANZSCO4(db.Model):
    __tablename__ = 'ANZSCO4'
    ANZSCO4_CODE = db.Column(db.Integer, primary_key=True)
    ANZSCO1_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO1.ANZSCO1_CODE'), nullable=False)
    TITLE = db.Column(db.String(255), nullable=False)

    # Relationship to ANZSCO1
    anzsco1 = db.relationship('ANZSCO1', backref=db.backref('anzsco4s', lazy=True))

class Specialist(db.Model):
    __tablename__ = 'SPECIALIST'
    ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO4.ANZSCO4_CODE'), primary_key=True)
    SPECIALIST_SKILL = db.Column(db.String(255), primary_key=True)
    TIME_SPENT = db.Column(db.Numeric(5, 2), nullable=False)

    # Relationship to ANZSCO4
    anzsco4 = db.relationship('ANZSCO4', backref=db.backref('specialists', lazy=True))

class CoreCompetency(db.Model):
    __tablename__ = 'CORE_COMPETENCY'
    CORE_COMPETENCY = db.Column(db.String(255), primary_key=True)
    CORE_COMPETENCY_DESC = db.Column(db.Text, nullable=True)
    SCORE = db.Column(db.Integer, primary_key=True)
    PROFICIENCY_LEVEL = db.Column(db.String(20), nullable=True)

class OccupationCoreCompetency(db.Model):
    __tablename__ = 'OCCUPATION_CORE_COMPETENCY'
    ANZSCO4_CODE = db.Column(db.Integer, db.ForeignKey('ANZSCO4.ANZSCO4_CODE'), primary_key=True)
    CORE_COMPETENCY = db.Column(db.String(255), db.ForeignKey('CORE_COMPETENCY.CORE_COMPETENCY'), primary_key=True)
    SCORE = db.Column(db.Integer, db.ForeignKey('CORE_COMPETENCY.SCORE'), primary_key=True)
    ANCHOR_VALUE = db.Column(db.Text, nullable=True)
    YEAR = db.Column(db.Integer, primary_key=True)

    # Relationships to ANZSCO4 and CoreCompetency with explicit foreign_keys
    anzsco4 = db.relationship('ANZSCO4', backref=db.backref('occupation_core_competencies', lazy=True))
    core_competency = db.relationship(
        'CoreCompetency',
        backref=db.backref('occupation_core_competencies', lazy=True),
        foreign_keys=[CORE_COMPETENCY]  # 指定明确的外键列
    )
