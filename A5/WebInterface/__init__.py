import json

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_wtf import CSRFProtect
from langchain.embeddings import HuggingFaceEmbeddings
from eurelis_langchain_solr_vectorstore import Solr

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # Initialize llm here
    llm = ""

    embeddings = HuggingFaceEmbeddings()
    vector_store = Solr(embeddings)

    vector_store = Solr(embeddings, core_kwargs={'page_content_field': 'text_t', 'vector_field': 'vector', 'core_name': 'langchain', 'url_base': 'http://localhost:8983/solr'})
    retriever = vector_store.as_retriever()

    @app.route('/')
    def index():
        if request.method == 'POST':
            prompt = request.form['prompt']

            # Process the prompt

            
            return render_template('index.html', results=results)
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        vector_store.close()

    return app
