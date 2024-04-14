import json
import os

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI

from .database import initSolr


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    csrf = CSRFProtect()
    csrf.init_app(app)

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

    @app.route('/')
    def index():
        if request.method == 'POST':
            prompt = request.form['prompt']

            # Process the prompt
            results = rag_chain.invoke(prompt)

            return render_template('index.html',
                                   results=results)
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        vector_store.close()

    return app
