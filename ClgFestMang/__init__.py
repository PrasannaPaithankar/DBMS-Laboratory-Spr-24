from flask import Flask, render_template, request, redirect, url_for, session
from .database import Base, engine, db_session, rebuild_db
from .models import Event, Participant, Role, Student, Organizer, Volunteer, Student_Event, Event_Participant
from . import auth
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import json
from flask_wtf.csrf import CSRFProtect


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_file("config.json", load=json.load)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prasanna:prasanna@localhost/clgfestmang'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp'
    app.config['SECRET_KEY'] = 'pipi'


    # rebuild when the app is run for the first time
    # rebuild_db()

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
                events = Event_Participant.query.filter_by(PID=user.PID).all()
                other_events = Event_Participant.query.filter(Event_Participant.PID != user.PID).all()
                events = [Event.query.filter_by(EID=event.EID).first() for event in events]
                other_events = [Event.query.filter_by(EID=event.EID).first() for event in other_events]

                return render_template('events.html', events=events, other_events=other_events)
            else:
                user = Student.query.filter_by(Roll=session['user_id']).first()
                events = Student_Event.query.filter_by(Roll=user.Roll).all()
                other_events = Student_Event.query.filter(Student_Event.Roll != user.Roll).all()
                events = [Event.query.filter_by(EID=event.EID).first() for event in events]
                other_events = [Event.query.filter_by(EID=event.EID).first() for event in other_events]

                return render_template('events.html', events=events, other_events=other_events)
        
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




    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
