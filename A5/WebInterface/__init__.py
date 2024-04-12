import json

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect

from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from itertools import chain

from . import auth
from .database import db_session, rebuild_db, init_db
from .models import (Event, Event_Participant, Organizer, Participant, Role,
                     Student, Student_Event, Volunteer, Notification, food)
from sqlalchemy.sql.functions import current_date


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    # rebuild when the app is run for the first time
    rebuild_db()

    csrf = CSRFProtect()
    csrf.init_app(app)

    auth.mail.init_app(app)

    app.register_blueprint(auth.bp)

    admin = Admin(name='Admin Panel', template_mode='bootstrap4',
                  index_view=AdminIndexView(name='Home'))
    admin.add_view(ModelView(Event, db_session))
    admin.add_view(ModelView(Student, db_session))
    admin.add_view(ModelView(Participant, db_session))
    admin.add_view(ModelView(Organizer, db_session))
    admin.add_view(ModelView(Volunteer, db_session))
    admin.add_view(ModelView(Role, db_session))
    admin.add_view(ModelView(Student_Event, db_session))
    admin.add_view(ModelView(Event_Participant, db_session))
    admin.add_view(ModelView(Notification, db_session))
    admin.add_view(ModelView(food, db_session))

    admin.init_app(app)

    @app.route('/')
    def index():
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                return render_template('index.html', user=user, role=session['role'])
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                return render_template('index.html', user=user, role=session['role'])

        return render_template('index.html')

    @app.route('/events', methods=['GET', 'POST'])
    def events():
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                if user is not None:
                    events = Event_Participant.query.filter_by(
                        PID=user.PID).all()
                    events = [Event.query.filter_by(
                        EID=event.EID).first() for event in events]
                    other_events = Event.query.filter(
                        Event.EID.notin_([event.EID for event in events])).all()

                    return render_template('events.html', events=events,
                                           other_events=other_events, user=user, role=session['role'])
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                user_events = Student_Event.query.filter_by(Roll=user.Roll).all()
                user_volunteers = Volunteer.query.filter_by(Roll=user.Roll).all()
                if user is not None:
                    combined_events = list(chain(user_events, user_volunteers))
                    events = list(set(combined_events))
                    events = [Event.query.filter_by(
                        EID=event.EID).first() for event in events]
                    other_events = Event.query.filter(
                        Event.EID.notin_([event.EID for event in events])).all()

                    return render_template('events.html', events=events,
                                           other_events=other_events, user=user, role=session['role'])

        events = Event.query.all()
        return render_template('events.html', other_events=events)

    @app.route('/event/<int:EID>', methods=['GET', 'POST'])
    def event(EID):
        event = Event.query.filter_by(EID=EID).first()
        already_part = False
        already_vol = False
        event_already_passed = True
        # check if event has not passed if not passed then set winners to to be decided 
        if event.Date > datetime.now().date():
            event.Winner1 = "To be decided"
            event.Winner2 = "To be decided"
            event.Winner3 = "To be decided"
            db_session.commit()
            event_already_passed = False
            

        if 'role' in session:
            # set values of already_part and already_vol if the user is already registered or a volunteer
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                if Event_Participant.query.filter_by(EID=EID, PID=user.PID).first() is not None:
                    already_part = True
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                if Student_Event.query.filter_by(Roll=user.Roll, EID=EID).first() is not None:
                    already_part = True
                if Volunteer.query.filter_by(Roll=user.Roll, EID=EID).first() is not None:
                    already_vol = True
        
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                if request.method == 'POST':
                    if request.form.get('register_as') == 'participant':
                        if Event_Participant.query.filter_by(EID=EID,PID=user.PID).first() is None:
                            event_participant = Event_Participant(
                            EID=EID, PID=user.PID, Position=0)
                            db_session.add(event_participant)
                            db_session.commit()
                            already_part = True
                            return redirect(url_for('events'))

                    return redirect(url_for('events'))
                return render_template('event_specific.html',
                                       event=event, user=user, role=session['role'], already_part = already_part,event_already_passed = event_already_passed)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                if request.method == 'POST':
                    if request.form.get('register_as') == 'participant':
                        if Student_Event.query.filter_by(Roll=user.Roll, EID=EID).first() is None:
                            student_event = Student_Event(
                            Roll=user.Roll, EID=EID, Position=0)
                            db_session.add(student_event)
                            db_session.commit()
                            already_part = True
                            return redirect(url_for('events'))
                    elif request.form.get('register_as') == 'volunteer':
                        if Volunteer.query.filter_by(Roll=user.Roll, EID=EID).first() is None:
                            volunteer = Volunteer(Roll=user.Roll, EID=EID)
                            db_session.add(volunteer)
                            db_session.commit()
                            already_vol = True
                            return redirect(url_for('events'))
                    return redirect(url_for('events'))
                return render_template('event_specific.html',
                                       event=event, user=user, role = session['role'], already_part = already_part, already_vol = already_vol, event_already_passed = event_already_passed)
       
        return render_template('event_specific.html', event=event, already_part = already_part, already_vol = already_vol)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app