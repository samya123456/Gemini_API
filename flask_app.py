import os
import json
import time
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
    response = model.generate_content(
        user_question, stream=True)
    for chunk in response:
        words = chunk.text.split(' ')
        for word in words:
            time.sleep(0.05)
            yield word

        # print(chunk.text)


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

    user_question = data.get('question', '')

    for word in generate_continuous_data(user_question):
        socketio.emit('continuous_data', {'data': " " + word})


if __name__ == '__main__':
    socketio.run(app)
