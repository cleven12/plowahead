import os
# Import routes
# from . import routes
# import models
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime



#from  Route.py
# from flask import render_template, request, redirect, url_for, flash
# from flask_mail import Message
# from app import app, db, mail
# from models import Member
# from forms import MemberRegistrationForm
# import logging

# from forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
mail = Mail()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "cGxvd19haGVhZF8yMDI1X2hha3VuYV9tYXRhdGEK")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///plow_ahead.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Database Models
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Member {self.name}>'

# v[0]
# Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'clevengodsontech@gmail.com'
# app.config['MAIL_PASSWORD'] = 'ipx ihef eocq bceb'
# app.config['MAIL_DEFAULT_SENDER'] = 'clevengodsontech@gmail.com'

# v[1]
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'       # Or your email provider
# app.config['MAIL_PORT'] = 587                     # 465 for SSL
# app.config['MAIL_USE_TLS'] = True                 # True if using TLS
# app.config['MAIL_USE_SSL'] = False                # True if using SSL
# app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
# app.config['MAIL_PASSWORD'] = 'your_email_password'
# app.config['MAIL_DEFAULT_SENDER'] = ('Plow Ahead', 'your_email@gmail.com')

# v[2]
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cleven2024@gmail.com'
app.config['MAIL_PASSWORD'] = 'fcyk lfvk ujkc uihc'
app.config['MAIL_DEFAULT_SENDER'] = ('Plow Ahead', 'happykombet@gmail.com')

# Initialize extensions
db.init_app(app)
mail.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    db.create_all()



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


@app.route('/')
def index():
    form = MemberRegistrationForm()
    return render_template('index.html', form=form)

@app.route('/register', methods=['POST'])
def register():
    form = MemberRegistrationForm()

    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_member = Member.query.filter_by(email=form.email.data).first()
            if existing_member:
                flash('This email is already registered. Thank you for your interest!', 'info')
                return redirect(url_for('index') + '#registration')

            # Create new member
            member = Member(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                message=form.message.data
            )

            db.session.add(member)
            db.session.commit()

            # Send confirmation email
            try:
                msg = Message(
                    subject='Welcome to Plow Ahead Initiative!',
                    recipients=[member.email],
                    html=f'''
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                                <div style="text-align: center; background: linear-gradient(135deg, #214487, #3a5da8); color: white; padding: 30px; border-radius: 10px 10px 0 0;">
                                    <h1 style="margin: 0; font-size: 2rem;">Welcome to Plow Ahead Initiative!</h1>
                                </div>
                                <div style="background: #f5f7fa; padding: 30px; border-radius: 0 0 10px 10px;">
                                    <h2 style="color: #214487;">Hello {member.name},</h2>
                                    <p>Thank you for joining the Plow Ahead Initiative! We're excited to have you as part of our community dedicated to unlocking human potential through education, innovation, and purposeful development.</p>

                                    <p>Your registration details:</p>
                                    <ul style="background: white; padding: 20px; border-radius: 5px; list-style: none;">
                                        <li><strong>Name:</strong> {member.name}</li>
                                        <li><strong>Email:</strong> {member.email}</li>
                                        {'<li><strong>Phone:</strong> ' + member.phone + '</li>' if member.phone else ''}
                                    </ul>

                                    <p>We'll keep you updated on our programs, campaigns, and stories of impact. Together, let's build a world where human potential is unlocked and innovation drives purposeful change.</p>

                                    <p style="margin-top: 30px;">
                                        <strong>Stay connected with us:</strong><br>
                                        Follow us on <a href="https://instagram.com/plowahead_initiative">Instagram</a> for the latest updates and community stories.
                                    </p>

                                    <p>Best regards,<br>
                                    <strong>The Plow Ahead Initiative Team</strong>
                                    </p>

                                    <p style="margin-top: 10px; font-size: 0.8rem; color: #888; font-style: italic;">
                                        Developed with ❤️ by <a href="mailto:clevengodsontech@gmail.com">Cleven</a>
                                    </p>
                                </div>
                            </div>
                        </body>
                    </html>
                    '''
                )
                mail.send(msg)

                # Send notification to admin
                admin_msg = Message(
                subject='New Member Registration - Plow Ahead Initiative',
                recipients=[app.config['MAIL_DEFAULT_SENDER']],  # staff emails
                html=f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                            <div style="text-align: center; background: linear-gradient(135deg, #214487, #3a5da8); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                                <h2 style="margin: 0;">New Member Registration</h2>
                            </div>

                            <div style="background: #f5f7fa; padding: 20px; border-radius: 0 0 10px 10px;">
                                <p><strong>Name:</strong> {member.name}</p>
                                <p><strong>Email:</strong> {member.email}</p>
                                <p><strong>Phone:</strong> {member.phone or 'Not provided'}</p>
                                <p><strong>Message:</strong> {member.message or 'No message'}</p>
                                <p><strong>Registration Time:</strong> {member.created_at}</p>

                                <hr style="margin: 20px 0; border: none; border-top: 1px solid #ccc;">

                                <!-- Dev footer -->
                                <p style="margin-top: 10px; font-size: 0.8rem; color: #888; font-style: italic;">
                                    Developed with ❤️ by <a href="mailto:clevengodsontech@gmail.com">Cleven</a>
                                </p>
                            </div>
                        </div>
                    </body>
                </html>
                """)
                mail.send(admin_msg)
            except Exception as e:
                logging.error(f"Email sending failed: {str(e)}")
                # Don't fail the registration if email fails
                pass

            return render_template('success.html', member=member)    
# V[0]
                # admin_msg = Message(
                #     subject='New Member Registration - Plow Ahead Initiative',
                #     recipients=[app.config['MAIL_DEFAULT_SENDER']],
                #     html=f'''
                #     <html>
                #         <body style="font-family: Arial, sans-serif;">
                #             <h2>New Member Registration</h2>
                #             <p><strong>Name:</strong> {member.name}</p>
                #             <p><strong>Email:</strong> {member.email}</p>
                #             <p><strong>Phone:</strong> {member.phone or 'Not provided'}</p>
                #             <p><strong>Message:</strong> {member.message or 'No message'}</p>
                #             <p><strong>Registration Time:</strong> {member.created_at}</p>
                #         </body>
                #     </html>
                #     '''
                # )
                # mail.send(admin_msg)
            # except Exception as e:
            #     logging.error(f"Email sending failed: {str(e)}")
            #     # Don't fail the registration if email fails
            #     pass

            # return render_template('success.html', member=member)

        except Exception as e:
            logging.error(f"Registration failed: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('index') + '#registration')

    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'error')
        return redirect(url_for('index') + '#registration')

@app.route('/success')
def success():
    # Redirect to home if accessed directly
    return redirect(url_for('index'))


# from main.py
# from app import app
if __name__ == '__main__':
    app.run(debug=True)
