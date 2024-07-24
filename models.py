from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Herb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    diseases = db.relationship('Disease', secondary='herb_disease_association', back_populates='herbs')
    herb_associations = db.relationship('HerbDiseaseAssociation', back_populates='herb')

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    herbs = db.relationship('Herb', secondary='herb_disease_association', back_populates='diseases')
    disease_associations = db.relationship('HerbDiseaseAssociation', back_populates='disease')

class HerbDiseaseAssociation(db.Model):
    __tablename__ = 'herb_disease_association'
    id = db.Column(db.Integer, primary_key=True)
    herb_id = db.Column(db.Integer, db.ForeignKey('herb.id'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    herb = db.relationship('Herb', back_populates='herb_associations')
    disease = db.relationship('Disease', back_populates='disease_associations')

class DiagnosisLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prescription = db.Column(db.String(500), nullable=False)
    diagnosis_result = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)