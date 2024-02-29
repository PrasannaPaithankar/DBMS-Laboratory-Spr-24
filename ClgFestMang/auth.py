import json
import random
from datetime import datetime, timedelta

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from . import database, models
from flask_mail import Mail, Message

with open('./instance/config.json') as config_file:
    config = json.load(config_file)

mail = Mail()
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        college = request.form['college']
        accomodation = request.form['accommodation']
        vegnonveg = request.form['vegnonveg']
        dept = request.form['dept']
        if vegnonveg == "Veg":
            vegnonveg = False
        else:
            vegnonveg = True
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'

        if error is None:
            try:
                if role == 'Student':
                    user = models.Student(Name=username, email=email, password=generate_password_hash(
                        password), Dept=dept, RID=1, gender=gender)
                elif role == 'ExternalParticipant':
                    accomodation = random.choice(
                        ['Azad', 'Nehru', 'Patel', 'MS', 'HJB'])
                    if accomodation == "No":
                        accomodation = None
                    user = models.Participant(Name=username, email=email, password=generate_password_hash(
                        password), CName=college, accomodation=accomodation, vegnonveg=vegnonveg, gender=gender)

                database.db_session.add(user)
                database.db_session.commit()

                subject = 'Registration Successful for DBMSFest 2024'
                body = f'Hello {username},\n\nYou have successfully registered for DBMSFest 2024.\n\nRegards,\nDBMSFest 2024 Team.'
                msg = Message(subject,
                                sender=config['MAIL_USERNAME'],
                                recipients=[email])
                msg.body = body
                mail.send(msg)
                flash('Successfully registered', 'success')
                return redirect(url_for('auth.login'))
            except:
                error = 'User {} is already registered.'.format(username)

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = models.Student.query.filter_by(Name=username).first()
        user2 = models.Participant.query.filter_by(Name=username).first()

        who = None
        if user is not None:
            who = 'student'
            if not check_password_hash(user.password, password):
                error = 'Incorrect password.'
        elif user2 is not None:
            who = 'participant'
            if not check_password_hash(user2.password, password):
                error = 'Incorrect password.'
        else:
            error = 'Incorrect username.'

        if error is None:
            session.clear()
            if who == 'student':
                session['user_id'] = user.Roll
                session['role'] = user.role.Rname
            elif who == 'participant':
                session['user_id'] = user2.PID
                session['role'] = 'external'
            flash('Successfully logged in', 'success')
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/edit_profile', methods=('GET', 'POST'))
def edit_profile():
    if request.method == 'POST':
        user_id = g.user
        user_role = g.role
        username = None
        if user_role == 'external':
            user = models.Participant.query.filter_by(PID=user_id).first()
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            accomodation = request.form['accommodation']
            vegnonveg = request.form['vegnonveg']
            if vegnonveg == "Veg":
                vegnonveg = False
            else:
                vegnonveg = True

            try:
                if email:
                    user.email = email
                if password:
                    if password == confirm_password:
                        user.password = generate_password_hash(password)
                if accomodation == "No":
                    user.accomodation = None
                if vegnonveg:
                    user.vegnonveg = vegnonveg
                database.db_session.commit()
                flash('Profile updated successfully.')
                username = user.Name
            except:
                error = 'Failed to update profile.'
                flash(error)
        else:
            user = models.Student.query.filter_by(Roll=user_id).first()
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            try:
                if email:
                    user.email = email
                if password:
                    if password == confirm_password:
                        user.password = generate_password_hash(password)
                database.db_session.commit()
                flash('Profile updated successfully.')
                username = user.Name
            except:
                error = 'Failed to update profile.'
                flash(error)
            
        if error is None:
            subject = 'Profile Updated for DBMSFest 2024'
            body = f'Hello {username},\n\nYour profile has been successfully updated for DBMSFest 2024.\n\nRegards,\nDBMSFest 2024 Team.'
            msg = Message(subject,
                            sender=config['MAIL_USERNAME'],
                            recipients=[email])
            msg.body = body
            mail.send(msg)

        return render_template('auth/edit_profile.html', user=user, role=user_role)

    return render_template('auth/edit_profile.html', role=g.role)


@bp.before_app_request
def load_logged_in_user():
    session.modified = True

    # if 'last_accessed' in session:
    #     last_accessed = session.get('last_accessed')
    #     if last_accessed + timedelta(seconds=config['PERMANENT_SESSION_LIFETIME']) < datetime.now():
    #         return redirect(url_for('logout'))
    # session['last_accessed'] = datetime.now()

    user_id = session.get('user_id')
    user_role = session.get('role')

    if user_role is None:
        g.user = None
        g.role = None
    elif user_role == 'external':
        user = models.Participant.query.filter_by(PID=user_id).first()
        g.user = user.PID
        g.role = 'external'
    else:
        user = models.Student.query.filter_by(Roll=user_id).first()
        g.user = user.Roll
        g.role = user.role.Rname

    end = request.endpoint
    if end is not None:
        if end.startswith('admin') and g.role != 'admin':
            return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
