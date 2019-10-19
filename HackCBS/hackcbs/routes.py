import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from hackcbs import app, db, bcrypt
from hackcbs.models import Patient, Doctor, InsuranceAgent, MedicalHistory
from hackcbs.forms import PatientRegistrationForm, DoctorRegistrationForm, AgentRegistrationForm, LoginForm

@app.route("/")
def cover():
    return render_template('cover.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    #modify functions accroding to needs
    return render_template('register.html')   

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data).first()
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        agent = InsuranceAgent.query.filter_by(email=form.email.data).first()
        if patient and bcrypt.check_password_hash(patient.password, form.password.data):
            login_user(patient, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('patient'))
        elif doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('doctor'))
        elif agent and bcrypt.check_password_hash(agent.password, form.password.data):
            login_user(agent, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('insurance'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/patient')
def patient():
    render_template('patient_home.html')

@app.route('/doctor')
def doctor():
    render_template('doctor_home.html')    

@app.route('/insurance')
def insurance():
    render_template('insurance_home.html')