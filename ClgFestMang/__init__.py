import os
from flask import Flask, render_template, request, redirect, url_for, session
import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET='pipi',
        # DATABASE=os.path.join(app.instance_path, 'clgfestmang.sqlite')
    )
    db.init_app(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
    

