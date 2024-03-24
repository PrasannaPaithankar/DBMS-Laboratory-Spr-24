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

    @app.route('/DBMS24')
    def test():
        return 'DBMS24'
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
                if part_bool == "1":
                    event_participants = Event_Participant.query.filter_by(
                        EID=organizer.EID).all()
                    participants = []
                    for event_participant in event_participants:
                        participant = Participant.query.filter_by(
                            PID=event_participant.PID).first()
                        participants.append(participant)
                    if participants:
                        msg = Message(subject,
                                    sender=app.config['MAIL_USERNAME'],
                                    recipients=[participant.email for participant in participants])
                        msg.body = message
                        auth.mail.send(msg)
                        flash('Emails sent successfully to participants')
                    else:
                        flash('No participants found')
               
                if volu_bool == "2":
                    volunteers = Volunteer.query.filter_by(EID=organizer.EID).all()
                    if volunteers:
                        msg = Message(subject,
                                    sender=app.config['MAIL_USERNAME'],
                                    recipients=[volunteer.student.email for volunteer in volunteers])
                        msg.body = message
                        auth.mail.send(msg)
                        flash('Emails sent successfully to volunteers')
                    else:
                        flash('No volunteers found')
                    
                return render_template('organizerPanel.html', user=organizer, events=[Event.query.filter_by(EID=organizer.EID).first()])
            
            elif request.form['formtype'] == 'setWinner':
                winner1 = request.form['winner1']
                winner2 = request.form['winner2']
                winner3 = request.form['winner3']
                organizer_id = session['user_id']
                organizer = Organizer.query.filter_by(Roll=organizer_id).first()
                event = Event.query.filter_by(EID=organizer.EID).first()

                # check if the date of event has passed
                print("Event date: ", event.Date)
                print("Current date: ", datetime.now().date())
                # extract date from datetime object
                current_date = datetime.now().date()
                if event.Date > datetime.now().date():
                    flash('Event has not yet passed. Cannot set winners')
                    return render_template('organizerPanel.html', user=organizer, events=[event])

                subject = f'Congratulations! You have won {event.EName}'
                message = f'Congratulations! You have won {event.EName}. Please contact the organizers for further details.'
                winners = []
                error = None

                user = Participant.query.filter_by(Name=winner1).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner1).first()
                    if user is not None:
                        winners.append(user)
                    else:
                        error = 'Winner1 not found'
                else:
                    winners.append(user)

                user = Participant.query.filter_by(Name=winner2).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner2).first()
                    if user is not None:
                        winners.append(user)
                    else:
                        error = 'Winner2 not found'
                else:
                    winners.append(user)

                user = Participant.query.filter_by(Name=winner3).first()
                if user is None:
                    user = Student.query.filter_by(Name=winner3).first()
                    if user is not None:
                        winners.append(user)
                    else:
                        error = 'Winner3 not found'
                else:
                    winners.append(user)
                
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

                return render_template('organizerPanel.html', user=organizer, events=[event])

        if 'role' in session:
            if session['role'] == 'organizer':
                user = Organizer.query.filter_by(
                    Roll=session['user_id']).first()
                events = Event.query.filter_by(EID=user.EID).all()
                return render_template('organizerPanel.html',
                                       user=user, events=events, role=session['role'])
        return render_template('index.html')
    

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        role = None
        if request.method == 'POST':
            # try:
            #     session['role']
            # except KeyError:
            #     session['role'] = 'user'
            if 'role' in session:
                role = session['role']
            query = request.form['query']
            events = Event.query.filter(Event.EName.ilike(
                f'%{query}%') | Event.Desc.ilike(f'%{query}%')).all()
            return render_template('search.html', events=events, user = role)
        return render_template('search.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'role' in session and 'user_id' in session:
            user_id = session['user_id']
            user_role = session['role']
            if user_role == 'external':
                user = Participant.query.filter_by(PID=user_id).first()
            else:  
                user = Student.query.filter_by(Roll=user_id).first()
                
            if request.method == 'POST':
                return redirect(url_for('auth.edit_profile'))

            return render_template('profile.html', user=user, role=user_role)
        return redirect(url_for('auth.login'))
    
    @app.route('/schedule', methods=['GET', 'POST'])
    def schedule():
        events = Event.query.all()
        events.sort(key=lambda x: x.Date)
        try:
            userid = session['user_id']
            role = session['role']
        except KeyError:
            userid = None
            role = None

        return render_template('schedule.html', events=events, user=userid, role=role)
    
    @app.route('/sendnotification', methods=['GET', 'POST'])
    def sendnotification():
        print(session)
        # Sending all the volunteers Roll and name to the form

        volunteers= (
            db_session.query(Volunteer.Roll, Student.Name)
            .join(Student, Volunteer.Roll == Student.Roll)
            .all()
        )

        print(volunteers)


        if request.method == 'POST':
            Vroll = request.form['volunteers']
            message = request.form['message']
            print(Vroll)
            print(message)
            # Add it to the database
            notification = Notification(receiver=Vroll, message=message , time=datetime.now() , sender=session['user_id'])
            db_session.add(notification)
            db_session.commit()
            print('Notification sent successfully')
            flash('Notification sent successfully')


        return render_template('sendnotification.html' , volunteers=volunteers, user = session['user_id'], role = session['role'])

    @app.route('/volunteerdashboard')
    def volunteerdashboard():
        messages = (
            db_session.query(Student.Name, Student.Roll, Notification.message, Notification.time)
            .join(Student, and_(Notification.sender == Student.Roll, Notification.receiver == session['user_id']))
            .order_by(Notification.time.desc())  # Sorting by time in descending order
            .all()
        )

        print(messages)
        return render_template('volunteer_dashboard.html' , messages=messages, user = session['user_id'], role = session['role'])

    @app.route('/searchvolunteers')
    def searchvolunteers():
        volunteers = (
        db_session.query(Volunteer.Roll, Student.Name, Student.email, Event.EName)
        .join(Event, Volunteer.EID == Event.EID)
        .join(Student, Volunteer.Roll == Student.Roll)
        .all()
        )

        print(volunteers)
        return render_template('searchvolunteers.html' , volunteers=volunteers, user = session['user_id'], role = session['role'])

    @app.route('/sendnotficationvolunteer/<volunteers>', methods=['GET', 'POST'])
    def sendnotficationvolunteer(volunteers):
        volunteers = eval(volunteers)
        if request.method == 'POST':
            Vroll = request.form['volunteers']
            message = request.form['message']
            # Add it to the database
            notification = Notification(receiver=Vroll, message=message, time=datetime.now(), sender=session['user_id'])
            db_session.add(notification)
            db_session.commit()
            print('Notification sent successfully')
            flash('Notification sent successfully')

        return render_template('sendnotification.html', volunteers=[{'Name':volunteers[1],'Roll':volunteers[0]}], user = session['user_id'], role = session['role'])

    @app.route('/food')
    def efood():
        if 'role' in session:
            if session['role'] == 'external':
                user = Participant.query.filter_by(
                    PID=session['user_id']).first()
                foodtype = user.vegnonveg
                print(foodtype)
                foods = db_session.query(food.Name, food.detail).filter_by(type=foodtype).all()
                print(foods)
                return render_template('food.html',foods = foods, foodtype = foodtype,user=user, role=session['role'])
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                return render_template('food.html',foodtype = None ,user=user, role=session['role'])

        return render_template('food.html',foodtype = None)

    @app.route('/modifyfood', methods=['GET', 'POST'])
    def modifyfood():
        if request.method == 'POST':
            foodtype = bool(request.form['foodtype'])
            name = request.form['name']
            detail = request.form['detail']

            db_session.add(food(Name=name, type=foodtype, detail=detail))
            db_session.commit()
            flash('Food added successfully')

        return render_template('modifyfood.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app