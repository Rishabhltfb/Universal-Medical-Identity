import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from hackcbs import app, db, bcrypt
from hackcbs.models import Patient, Doctor, InsuranceAgent, MedicalHistory
from hackcbs.forms import PatientRegistrationForm, DoctorRegistrationForm, AgentRegistrationForm


@app.route("/")
def cover():
    return render_template('cover.html')


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
    # modify function according to needs
    return render_template('login.html')


@app.route('/patient')
def patient():
    render_template('patient_home.html')


@app.route('/about')
def about():
    render_template('patient_home.html')


@app.route('/contact')
def contact():
    render_template('patient_home.html')


@app.route('/doctor')
def doctor():
    render_template('doctor_home.html')


@app.route('/insurance')
def insurance():
    render_template('insurance_home.html')
