import json
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import CSRFProtect
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


from .database import initSolr


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
    # os.environ["GOOGLE_API_KEY"] = ""

    llm = GoogleGenerativeAI(model="gemini-pro")
    print("Model initialized")

    vector_store = initSolr("data_full")
    retriever = vector_store.as_retriever()
    print("Retriever initialized")

    template = """Question: {question}

    Use the following pieces of context to answer the question at the end.
    
    Always say "thanks for asking!" at the end of the answer.

    {context}


    Detailed long answer:"""
    prompt = PromptTemplate.from_template(template)

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
        answer = request.args.get("answer")
        question = request.args.get("question")
        if answer is None:
            answer = ""
        if question is None:
            question = ""

        return render_template("index.html", answer=answer, question=question)

    @app.route('/submitmessage', methods=['POST'])
    def submitmessage():
        if request.method == "POST":
            question = request.form["questionInput"]
            answer = rag_chain.invoke(question)
        else:
            print("Error")
            answer = "Some Error with error"
        return redirect(url_for("home", answer=answer , question = question))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
