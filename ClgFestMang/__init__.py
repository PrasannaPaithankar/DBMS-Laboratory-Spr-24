import os
from flask import Flask, render_template, request, redirect, url_for, session
from . import db
from . import auth
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET='pipi',
        # DATABASE=os.path.join(app.instance_path, 'clgfestmang.sqlite')
    )
    app.config['FLASK_ADMIN_SWATCH'] = 'lumen'
    admin = Admin(app, name='ClgFestMang', template_mode='bootstrap4')
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Post, db.session))

    db.init_app(app)
    app.register_blueprint(auth.bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

