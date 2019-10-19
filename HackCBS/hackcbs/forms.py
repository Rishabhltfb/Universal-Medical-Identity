from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from hackcbs.models import Patient, Doctor, InsuranceAgent, MedicalHistory

sample_license_id = []  # include sample license numbers in this list.


class PatientRegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    age = StringField('Age', validators=[DataRequired(), Length(min=1, max=3)])
    address = TextAreaField('Address', validators=[DataRequired()])
    blood_group = StringField('Blood_group')
    # gender =
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data).first()
        if patient:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class DoctorRegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    license_number = StringField('License_number', validators=[DataRequired()])
    clinic_address = TextAreaField('Address', validators=[DataRequired()])
    medical_qualification = TextAreaField(
        'Qualification', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_license(self, license_number):
        doctor = Doctor.query.filter_by(
            license_number=license_number.data).first()
        if self.license_number in sample_license_id:
            if doctor:
                raise ValidationError(
                    'User with this license number is already registered!')
        else:
            raise ValidationError('Invalid license number!')


class AgentRegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    company_name = StringField('Company', validators=[DataRequired()])
    company_id = StringField('Company_ID', validators=[DataRequired()])
    agent_id = StringField('Agent_ID', validators=[DataRequired()])
    designation = StringField('Designation')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        agent = InsuranceAgent.query.filter_by(email=email.data).first()
        if agent:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_agent_id(self, email):
        agent = InsuranceAgent.query.filter_by(agent_id=agent_id.data).first()
        if agent:
            raise ValidationError(
                'Someone with this ID is already registered.')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg'])])
    document = FileField('Update Document', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
