import json

from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect

from . import auth
from .database import Base, db_session, engine, rebuild_db
from .models import (Event, Event_Participant, Organizer, Participant, Role,
                     Student, Student_Event, Volunteer)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    # rebuild when the app is run for the first time
    rebuild_db()

    csrf = CSRFProtect()
    csrf.init_app(app)

    app.register_blueprint(auth.bp)
    
    admin = Admin(name='Admin Panel', template_mode='bootstrap4', index_view=AdminIndexView(name='Home'))
    admin.add_view(ModelView(Event, db_session))
    admin.add_view(ModelView(Student, db_session))
    admin.add_view(ModelView(Participant, db_session))
    admin.add_view(ModelView(Organizer, db_session))
    admin.add_view(ModelView(Volunteer, db_session))
    admin.add_view(ModelView(Role, db_session))
    admin.add_view(ModelView(Student_Event, db_session))
    admin.add_view(ModelView(Event_Participant, db_session))

    admin.init_app(app)

    @app.route('/')
    def index():
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(PID=session['user_id']).first()
                return render_template('index.html', user=user)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                return render_template('index.html', user=user)
            
        return render_template('index.html')
    
    @app.route('/events', methods=['GET', 'POST'])
    def events():
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(PID=session['user_id']).first()
                user_events = Event_Participant.query.filter_by(PID=user.PID).all()
                other_events = Event_Participant.query.filter(Event_Participant.PID != user.PID).all()
                user_events = [Event.query.filter_by(EID=event.EID).first() for event in user_events]
                other_events = [Event.query.filter_by(EID=event.EID).first() for event in other_events]

                return render_template('events.html', user_events=user_events, other_events=other_events)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                user_events = Student_Event.query.filter_by(Roll=user.Roll).all()
                other_events = Student_Event.query.filter(Student_Event.Roll != user.Roll).all()
                user_events = [Event.query.filter_by(EID=event.EID).first() for event in user_events]
                other_events = [Event.query.filter_by(EID=event.EID).first() for event in other_events]

                return render_template('events.html', user_events=user_events, other_events=other_events)
        
        events = Event.query.all()
        return render_template('events.html', events=events)
    
    @app.route('/event/<int:EID>', methods=['GET', 'POST'])
    def event(EID):
        event = Event.query.filter_by(EID=EID).first()
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(PID=session['user_id']).first()
                if request.method == 'POST':
                    event_participant = Event_Participant(EID=EID, PID=user.PID, Position=0)
                    db_session.add(event_participant)
                    db_session.commit()
                    return redirect(url_for('events'))
                return render_template('event_specific.html', event=event, user=user)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                if request.method == 'POST':
                    student_event = Student_Event(Roll=user.Roll, EID=EID, Position=0)
                    db_session.add(student_event)
                    db_session.commit()
                    return redirect(url_for('events'))
                return render_template('event_specific.html', event=event, user=user)
        return render_template('event_specific.html', event=event)
    
    @app.route('/organizerPanel', methods=['GET', 'POST'])
    def organizerPanel():
        if request.method == 'POST':
            subject = request.form['subject']
            message = request.form['email']
            part_bool = request.form.get('participants', 0)
            volu_bool = request.form.get('volunteers', 0)

            organizer_id = session['user_id']
            organizer = Organizer.query.filter_by(OID=organizer_id).first()
            if part_bool == 1:
                participants = Event_Participant.query.filter_by(EID=organizer.EID).all()
            elif part_bool == 2:
                participants = request.form.getlist('participants')
                for participant in participants:
                    participant = Participant.query.filter_by(PID=participant).first()
            if volu_bool == 1:
                volunteers = Volunteer.query.filter_by(EID=organizer.EID).all()

                msg = Message(subject,
                                sender=app.config['MAIL_USERNAME'],
                                recipients=[volunteers.email])
                msg.body = message
                auth.mail.send(msg)
            if part_bool > 0:
                msg = Message(subject,
                                sender=app.config['MAIL_USERNAME'],
                                recipients=[participants.email])
                msg.body = message
                auth.mail.send(msg)
            flash('Emails sent successfully')

        if 'role' in session:
            if session['role'] == 'organizer':
                user = Organizer.query.filter_by(OID=session['user_id']).first()
                events = Event.query.filter_by(OID=user.OID).all()
                return render_template('organizerPanel.html', user=user, events=events)
        return redirect(url_for('index'))

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            if 'role' in session:
                if session['role'] == 'organizer':
                    user = Organizer.query.filter_by(OID=session['user_id']).first()
                    query = request.form['query']
                    events = Event.query.filter(Event.EName.ilike(f'%{query}%') | Event.Desc.ilike(f'%{query}%')).all()
                    volunteers = Volunteer.query.filter(Volunteer.Name.ilike(f'%{query}%')).all()
                    return render_template('search.html', events=events, volunteers=volunteers, user=user)
                else:
                    query = request.form['query']
                    events = Event.query.filter(Event.EName.ilike(f'%{query}%') | Event.Desc.ilike(f'%{query}%')).all()
                    return render_template('search.html', events=events)
        return render_template('search.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        user_id = session['user_id']
        user_role = session['role']
        if user_role == 'external':
            user = Participant.query.filter_by(PID=user_id).first()
        elif user_role == 'organizer':
            user = Organizer.query.filter_by(OID=user_id).first()
        else:
            user = Student.query.filter_by(Roll=user_id).first()
        if request.method == 'POST':
            return redirect(url_for('auth.edit_profile'))
          
        return render_template('profile.html', user=user, role=user_role)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
