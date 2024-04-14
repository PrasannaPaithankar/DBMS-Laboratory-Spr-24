import json
import os

from flask import Flask, redirect, render_template, request, url_for
from flask_wtf import CSRFProtect
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI

from .database import initSolr


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_file("config.json", load=json.load)

    # csrf = CSRFProtect()
    # csrf.init_app(app)

    # Initialize llm here
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/hard_drive/Codes/DBMS-Laboratory-Spr-24/A5/silken-agent-420312-1464c99084fe.json"
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBAnX6q5rNF6IGtRLnF-epDIEH9_54Qq34"

    llm = GoogleGenerativeAI(model="gemini-pro")
    # llm = ChatVertexAI(model_name="chat-bison")

    print(llm.invoke("Hello, how are you?"))

    vector_store = initSolr("data")
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

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
