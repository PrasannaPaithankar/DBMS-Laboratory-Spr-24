import os
from flask import Flask, render_template, request, redirect, url_for, session
from . import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY']='dev'
    db.init_app(app)

    from .auth import bp
    app.register_blueprint(bp) 
    return app
    # @app.route('/')
    # def index():
    #     return render_template('index.html')
    

