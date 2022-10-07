
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flask_wtf import FlaskForm  
from zetta_app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                        validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired()])
    designation = StringField('Designation',
                        validators=[DataRequired()])
    # location = StringField('Location',
    #                        validators=[DataRequired(), Length(min=2, max=30)])
    contact = StringField('Contact',
                        validators=[DataRequired()])
    gmail = StringField('Gmail',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Login')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')

class zetta_form(FlaskForm):

    patient_name = StringField('Patient Name',
                        validators=[DataRequired()])
    age = StringField('Age',
                           validators=[DataRequired()])
    weight = StringField('weight',
                        validators=[DataRequired()])
    bmi = StringField('bmi',
                        validators=[DataRequired()])
    blood_pressure = StringField('Blood Pressure',
                        validators=[DataRequired()])
    insulin = StringField('Insulin',
                           validators=[DataRequired()])
    cardio_stress_level = StringField('Cardio',
                        validators=[DataRequired()])
    liver_stress_level = StringField('Liver',
                        validators=[DataRequired()])
    smoking_history_in_years = StringField('Smoking History',
                        validators=[DataRequired()])
   
    
    
    submit = SubmitField('Submit For Predictions')




class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')