from flask import Flask, render_template, request, redirect, url_for, sessions
from .database import Base, engine, db_session, init_db, rebuild_db
from .models import Event, Participant, Role, Student, Organizer, Volunteer
from . import auth
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import argparse
import json


def create_app(rebuild=False):
    app = Flask(__name__, instance_relative_config=True)

    with open('config.json') as config_file:
        config = json.load(config_file)
    app.config.update(config)

    if rebuild: 
        rebuild_db()

    app.register_blueprint(auth.bp)

    admin = Admin(app, index_view=AdminIndexView(name='Home'))
    admin.add_view(ModelView(Event, db_session))
    admin.add_view(ModelView(Student, db_session))
    admin.add_view(ModelView(Participant, db_session))
    admin.add_view(ModelView(Organizer, db_session))
    admin.add_view(ModelView(Volunteer, db_session))
    admin.add_view(ModelView(Role, db_session))

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--rebuild', type=bool)
    args = args.parse_args()

    app = create_app(args.dblink, args.rebuild)
    app.run(debug=True)
