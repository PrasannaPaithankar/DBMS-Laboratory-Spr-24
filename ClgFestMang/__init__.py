import json

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect

from . import auth
from .database import db_session, rebuild_db
from .models import (Event, Event_Participant, Organizer, Participant, Role,
                     Student, Student_Event, Volunteer)


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

    admin.init_app(app)

    @app.route('/')
    def index():
        print(session)
        if 'user' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                return render_template('index.html', user=user)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                return render_template('index.html', user=user)

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
                                           other_events=other_events)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                if user is not None:
                    events = Student_Event.query.filter_by(
                        Roll=user.Roll).all()
                    events = [Event.query.filter_by(
                        EID=event.EID).first() for event in events]
                    other_events = Event.query.filter(
                        Event.EID.notin_([event.EID for event in events])).all()

                    return render_template('events.html', events=events,
                                           other_events=other_events)

        events = Event.query.all()
        return render_template('events.html', events=events)

    @app.route('/event/<int:EID>', methods=['GET', 'POST'])
    def event(EID):
        event = Event.query.filter_by(EID=EID).first()
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                if request.method == 'POST':
                    event_participant = Event_Participant(
                        EID=EID, PID=user.PID, Position=0)
                    # check if the participant is already registered
                    if Event_Participant.query.filter_by(EID=EID,PID=user.PID).first() is not None:
                        db_session.add(event_participant)
                        db_session.commit()
                        return redirect(url_for('events'))
                    db_session.add(event_participant)
                    db_session.commit()
                    return redirect(url_for('events'))
                return render_template('event_specific.html',
                                       event=event, user=user)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                if request.method == 'POST':
                    student_event = Student_Event(
                        Roll=user.Roll, EID=EID, Position=0)
                    # check if the student is already registered
                    if Student_Event.query.filter_by(Roll=user.Roll, EID=EID).first() is not None:
                        db_session.add(student_event)
                        db_session.commit()
                        return redirect(url_for('events'))
                    db_session.add(student_event)
                    db_session.commit()
                    return redirect(url_for('events'))
                return render_template('event_specific.html',
                                       event=event, user=user)
        return render_template('event_specific.html', event=event)

    @app.route('/organizerPanel', methods=['GET', 'POST'])
    def organizerPanel():
        if request.method == 'POST':
            if request.form['formtype'] == 'mail':
                subject = request.form['subject']
                message = request.form['message']
                part_bool = request.form.get('participants', 0)
                volu_bool = request.form.get('volunteers', 0)

                organizer_id = session['user_id']
                organizer = Organizer.query.filter_by(Roll=organizer_id).first()
                print(organizer.EID)
                if part_bool == "1":
                    event_participants = Event_Participant.query.filter_by(
                        EID=organizer.EID).all()
                    participants = []
                    for event_participant in event_participants:
                        participant = Participant.query.filter_by(
                            PID=event_participant.PID).first()
                        participants.append(participant)
                elif part_bool == "2":
                    participants = request.form.getlist('participants')
                    for participant in participants:
                        participant = Participant.query.filter_by(
                            PID=participant).first()
                if volu_bool == "1":
                    volunteers = Volunteer.query.filter_by(EID=organizer.EID).all()

                    msg = Message(subject,
                                sender=app.config['MAIL_USERNAME'],
                                recipients=[volunteers.email])
                    msg.body = message
                    auth.mail.send(msg)
                if part_bool == "1" or part_bool == "2":
                    print(participants)
                    msg = Message(subject,
                                sender=app.config['MAIL_USERNAME'],
                                recipients=[participant.email for participant in participants])
                    msg.body = message
                    auth.mail.send(msg)
                flash('Emails sent successfully')
                return render_template('organizerPanel.html', user=organizer)
            
            elif request.form['formtype'] == 'setWinner':
                winner1 = request.form['winner1']
                winner2 = request.form['winner2']
                winner3 = request.form['winner3']
                organizer_id = session['user_id']
                organizer = Organizer.query.filter_by(Roll=organizer_id).first()
                event = Event.query.filter_by(EID=organizer.EID).first()

                subject = f'Congratulations! You have won {event.EName}'
                message = f'Congratulations! You have won {event.EName}. Please contact the organizers for further details.'
                winners = []
                user = Participant.query.filter_by(Name=winner1).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner1).first()
                    if user is not None:
                        winners.append(user)
                else:
                    error = 'Winner1 not found'
                user = Participant.query.filter_by(Name=winner2).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner2).first()
                    if user is not None:
                        winners.append(user)
                else:
                    error = 'Winner2 not found'
                user = Participant.query.filter_by(Name=winner3).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner3).first()
                    if user is not None:
                        winners.append(user)
                else:
                    error = 'Winner3 not found'
                
                if len(winners) == 3:
                    event.Winner1 = winner1
                    event.Winner2 = winner2
                    event.Winner3 = winner3
                    db_session.commit()

                    for winner in winners:
                        msg = Message(subject,
                                    sender=app.config['MAIL_USERNAME'],
                                    recipients=[winner.email])
                        msg.body = message
                        auth.mail.send(msg)
                    flash('Winners notified successfully')
                
                if error is not None:
                    flash(error)

                return render_template('organizerPanel.html', user=organizer)

        if 'role' in session:
            if session['role'] == 'organizer':
                user = Organizer.query.filter_by(
                    Roll=session['user_id']).first()
                events = Event.query.filter_by(EID=user.EID).all()
                return render_template('organizerPanel.html',
                                       user=user, events=events)
        return render_template('index.html')
    

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            # if 'role' in session:
            try:
                session['role']
            except KeyError:
                session['role'] = 'user'
            if session['role'] == 'organizer':
                user = Organizer.query.filter_by(
                    Roll=session['user_id']).first()
                query = request.form['query']
                events = Event.query.filter(Event.EName.ilike(
                    f'%{query}%') | Event.Desc.ilike(f'%{query}%')).all()
                volunteers = Volunteer.query.filter(
                    Volunteer.Name.ilike(f'%{query}%')).all()
                return render_template('search.html', events=events,
                                        volunteers=volunteers, user=user, role=session['role'])
            else:
                query = request.form['query']
                events = Event.query.filter(Event.EName.ilike(
                    f'%{query}%') | Event.Desc.ilike(f'%{query}%')).all()
                return render_template('search.html', events=events, role=session['role'])
        return render_template('search.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        user_id = session['user_id']
        user_role = session['role']
        if user_role == 'external':
            user = Participant.query.filter_by(PID=user_id).first()
        elif user_role == 'organizer':
            user = Organizer.query.filter_by(Roll=user_id).first()
        else:
            user = Student.query.filter_by(Roll=user_id).first()
        if request.method == 'POST':
            return redirect(url_for('auth.edit_profile'))

        return render_template('profile.html', user=user, role=user_role)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
