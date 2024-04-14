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
        answer = request.args.get("answer")

        if answer is None:
            answer = ""

        print(f"Answer: {answer}")
        # myChats = [{"question":"hello","answer":"hi"},{"question":"how are you","answer":"I am fine"}]
        # print(myChats)

        # answers = []

        # answers.append(answer)
        # print(answers)
        return render_template("index.html", answer=answer)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    
    @app.route('/submitmessage', methods=['POST'])
    def submitmessage():
        # Accept the form data
        # print("Hello submit message")
        if request.method == "POST":
            question = request.form["questionInput"]
            # print(question)
            # print("IF")
            answer = "LLM will answer" + question
        else:
            print("Error")
            answer = "Some Error with error"

        # print(question)

        # return  home(answer)
        return redirect(url_for("home", answer=answer))

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
