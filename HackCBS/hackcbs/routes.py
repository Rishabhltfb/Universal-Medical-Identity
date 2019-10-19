import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from hackcbs import app, db, bcrypt
from hackcbs.models import Patient, Doctor, InsuranceAgent, MedicalHistory
from hackcbs.forms import PatientRegistrationForm, DoctorRegistrationForm, AgentRegistrationForm, LoginForm


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register/<int:choice>", methods=['GET', 'POST'])
def register(choice):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        if choice:
            if choice == 1:
                form = PatientRegistrationForm()
            elif choice == 2:
                form = DoctorRegistrationForm()
            elif choice == 3:
                form = AgentRegistrationForm()
            return render_template('register.html', choice=choice,  form=form)
        else:
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
    return render_template('patient_home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/doctor')
def doctor():
    return render_template('doctor_home.html')


@app.route('/insurance')
def insurance():
    return render_template('insurance_home.html')


@app.route('/profile')
def profile():
    medical_history = MedicalHistory.query.filter_by(patient_id=current_user.id)\
        .order_by(MedicalHistory.date_of_report.desc())
    return render_template('profile.html', medical_history=medical_history)
