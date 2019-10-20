from datetime import datetime
from hackcbs import db, login_manager
from flask_login import UserMixin

# add __repr__ fuction in the below classes according to needs


@login_manager.user_loader
def load_patient(user_id):
    return Patient.query.get(int(user_id))


@login_manager.user_loader
def load_doctor(user_id):
    return Doctor.query.get(int(user_id))


@login_manager.user_loader
def load_agent(user_id):
    return InsuranceAgent.query.get(int(user_id))


class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_patient.jpg')
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(400), nullable=False)
    blood_group = db.Column(db.String(5), default=" ")
    gender = db.Column(db.String(5), nullable=False)


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_doctor.jpg')
    password = db.Column(db.String(60), nullable=False)
    clinic_address = db.Column(db.String(400), nullable=False)
    license_number = db.Column(db.String(20), nullable=False, unique=True)
    medical_qualification = db.Column(db.String(400), nullable=False)


class InsuranceAgent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    company_name = db.Column(db.String(50), unique=True, nullable=False)
    company_id = db.Column(db.String(20), nullable=False, unique=True)
    agent_id = db.Column(db.String(20), nullable=False, unique=True)
    agent_designation = db.Column(db.String(50), nullable=False)


class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False, unique=True)
    doctor_id = db.Column(db.Integer, nullable=False, unique=True)
    heading = db.Column(db.String(200), nullable=False)
    uploaded_file = db.Column(db.String(200), nullable=False)
    patient_notes = db.Column(db.String(1000), default=" ")
    doctor_remarks = db.Column(db.String(1000), default=" ")
    date_of_report = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    doctor_name = db.Column(db.String(30), nullable=False)
