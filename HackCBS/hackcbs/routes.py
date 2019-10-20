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
        return redirect(url_for('profile'))
    else:
        if choice:
            if choice == 1:
                form = PatientRegistrationForm()
                if form.validate_on_submit():
                    hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
                    user = Patient(name=form.name.data,
                                   email=form.email.data, password=hashed_password,
                                   age=int(form.age.data),
                                   address=form.address.data,
                                   blood_group=form.blood_group.data,
                                   gender=form.gender.data)
                    db.session.add(user)
                    db.session.commit()
                    flash(
                        'Your account has been created! You are now able to log in', 'success')
                    return redirect(url_for('login'))
            elif choice == 2:
                form = DoctorRegistrationForm()
                if form.validate_on_submit():
                    hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
                    user = Doctor(name=form.name.data,
                                  email=form.email.data, password=hashed_password,
                                  clinic_address=form.clinic_address.data,
                                  license_number=form.license_number.data,
                                  medical_qualification=form.medical_qualification.data)
                    db.session.add(user)
                    db.session.commit()
                    flash(
                        'Your account has been created! You are now able to log in', 'success')
                    return redirect(url_for('login'))
            elif choice == 3:
                form = AgentRegistrationForm()
                if form.validate_on_submit():
                    hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
                    user = InsuranceAgent(name=form.name.data,
                                          email=form.email.data, password=hashed_password,
                                          company_name=form.company_name.data,
                                          company_id=form.company_id.data,
                                          agent_id=form.agent_id.data,
                                          agent_designation=form.agent_designation.data)
                    db.session.add(user)
                    db.session.commit()
                    flash(
                        'Your account has been created! You are now able to log in', 'success')
                    return redirect(url_for('login'))
            return render_template('register.html', choice=choice,  form=form)
        else:
            return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
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
    return render_template('patient.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/doctor')
def doctor():
    doctor = Doctor.query.filter_by(email=form.email.data).first()
    form = doctor.form()
    return render_template('doctor.html',form = 'form')


@app.route('/insurance')
def insurance():
    return render_template('insurance.html')


@app.route('/profile')
def profile():
    medical_history = MedicalHistory.query.filter_by(patient_id=current_user.id)\
        .order_by(MedicalHistory.date_of_report.desc())
    return render_template('profile.html', medical_history=medical_history)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/media', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
