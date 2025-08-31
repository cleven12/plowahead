from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from app import app, db, mail
from models import Member
from forms import MemberRegistrationForm
import logging

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
                                        Follow us on Instagram for the latest updates and community stories.
                                    </p>
                                    
                                    <p>Best regards,<br>
                                    <strong>The Plow Ahead Initiative Team</strong></p>
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
                    recipients=[app.config['MAIL_USERNAME']],
                    html=f'''
                    <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2>New Member Registration</h2>
                            <p><strong>Name:</strong> {member.name}</p>
                            <p><strong>Email:</strong> {member.email}</p>
                            <p><strong>Phone:</strong> {member.phone or 'Not provided'}</p>
                            <p><strong>Message:</strong> {member.message or 'No message'}</p>
                            <p><strong>Registration Time:</strong> {member.created_at}</p>
                        </body>
                    </html>
                    '''
                )
                mail.send(admin_msg)
                
            except Exception as e:
                logging.error(f"Email sending failed: {str(e)}")
                # Don't fail the registration if email fails
                pass
            
            return render_template('success.html', member=member)
            
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
