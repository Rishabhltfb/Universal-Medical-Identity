from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_patient.jpg')
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(400), nullable=False)
    blood_group = db.Column(db.String(5), default= " ")

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_doctor.jpg')
    password = db.Column(db.String(60), nullable=False)
    clinic_address = db.Column(db.String(400), nullable=False)
    license_number = db.Column(db.String(20), nullable=False, unique=true)
    medical_qualification = db.Column(db.String(400), nullable=False)

class Insurance(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    company_name = db.Column(db.String(50), unique=True, nullable=False)
    company_id = db.Column(db.String(20), nullable=False, unique=True)
    agent_name = db.Column(db.String(100), nullable=False)
    agent_id = db.Column(db.String(20), nullable=False, unique=True)
    agent_designation = db.Column(db.String(50), nullable=False)

