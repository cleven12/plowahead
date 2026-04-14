from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class MemberRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(max=20, message='Phone number must be less than 20 characters')
    ])
    message = TextAreaField('Message (Optional)', validators=[
        Optional(),
        Length(max=500, message='Message must be less than 500 characters')
    ])
    submit = SubmitField('Register Now')
