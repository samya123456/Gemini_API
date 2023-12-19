import os
import json
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
socketio = SocketIO(app)


def generate_continuous_data(user_question):
    model = genai.GenerativeModel('gemini-pro')
    print('inside generate_continuous_data')
    response = model.generate_content(
        user_question, stream=True)
    for chunk in response:
        yield chunk.text.encode('utf-8')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('request_data')
def handle_request_data(data):
    print('Received request for data')
    user_question = data.get('question', '')
    print(f'Received request for data with question: {user_question}')
    for chunk in generate_continuous_data(user_question):
        socketio.emit('continuous_data', {'data': chunk.decode('utf-8')})


if __name__ == '__main__':
    socketio.run(app)
