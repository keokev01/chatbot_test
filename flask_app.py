from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import sqlite3
from chatbot.chatbot import Chatbot
import uuid

PYTHONANYWHERE_USERNAME = "chatbottest"
PYTHONANYWHERE_WEBAPPNAME = "chatbot_test"

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Fügen Sie einen geheimen Schlüssel für die Sitzung hinzu

# Setze den Pfad zur Datenbankdatei
database = f"/home/{PYTHONANYWHERE_USERNAME}/mysite/{PYTHONANYWHERE_WEBAPPNAME}/database/chatbot.db"
if not os.path.exists(database):
    raise RuntimeError(f"Database file not found at {database}")

@app.before_request
def ensure_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Erstellen Sie eine neue Benutzer-ID

@app.route("/")
def index():
    return "Ok. Your chatbot app is running. But the URL you used is missing the type_id path variable."

@app.route("/<type_id>/chat")
def chatbot(type_id: str):
    return render_template("index.html")

@app.route("/<type_id>/info")
def info_retrieve(type_id: str):
    user_id = session['user_id']
    bot = Chatbot(
        database_file=database,
        type_id=type_id,
        user_id=user_id,
        type_name=Chatbot.default_type_name,
        type_role=Chatbot.default_type_role,
        instance_context=Chatbot.default_instance_context,
        instance_starter=Chatbot.default_instance_starter
    )
    response = bot.info_retrieve()
    return jsonify(response)

@app.route("/<type_id>/conversation")
def conversation_retrieve(type_id: str):
    user_id = session['user_id']
    bot = Chatbot(
        database_file=database,
        type_id=type_id,
        user_id=user_id,
        type_name=Chatbot.default_type_name,
        type_role=Chatbot.default_type_role,
        instance_context=Chatbot.default_instance_context,
        instance_starter=Chatbot.default_instance_starter
    )
    response = bot.conversation_retrieve()
    return jsonify(response)

@app.route("/<type_id>/response_for", methods=["POST"])
def response_for(type_id: str):
    user_id = session['user_id']
    user_says = request.json
    bot = Chatbot(
        database_file=database,
        type_id=type_id,
        user_id=user_id,
        type_name=Chatbot.default_type_name,
        type_role=Chatbot.default_type_role,
        instance_context=Chatbot.default_instance_context,
        instance_starter=Chatbot.default_instance_starter
    )
    assistant_says_list = bot.respond(user_says)
    response = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)

@app.route("/<type_id>/reset", methods=["DELETE"])
def reset(type_id: str):
    user_id = session['user_id']
    bot = Chatbot(
        database_file=database,
        type_id=type_id,
        user_id=user_id,
        type_name=Chatbot.default_type_name,
        type_role=Chatbot.default_type_role,
        instance_context=Chatbot.default_instance_context,
        instance_starter=Chatbot.default_instance_starter
    )
    bot.reset()
    assistant_says_list = bot.start()
    response = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run()
