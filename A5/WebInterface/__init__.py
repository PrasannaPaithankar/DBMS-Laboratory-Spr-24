import json

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
# from flask_wtf import CSRFProtect
# from langchain.embeddings import HuggingFaceEmbeddings
# from eurelis_langchain_solr_vectorstore import Solr

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_file("config.json", load=json.load)

    # csrf = CSRFProtect()
    # csrf.init_app(app)

    # Initialize llm here
    # llm = ""

    # embeddings = HuggingFaceEmbeddings()
    # vector_store = Solr(embeddings)

    # vector_store = Solr(embeddings, core_kwargs={'page_content_field': 'text_t', 'vector_field': 'vector', 'core_name': 'langchain', 'url_base': 'http://localhost:8983/solr'})
    # retriever = vector_store.as_retriever()

    @app.route("/")
    def home():
        # chats = mongo.db.chats.find({})
        # myChats = [chat for chat in chats]
        # print(myChats)
        return render_template("index.html", myChats = [])

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # vector_store.close()
        pass

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
