from flask import Flask, render_template, request, redirect
import requests
import threading
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

SECRET_KEY = "rajveer2025"

def send_messages(token, thread_id, delay, messages):
    url = f"https://graph.facebook.com/v18.0/{thread_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    for msg in messages:
        data = {"message": msg.strip()}
        response = requests.post(url, headers=headers, data=data)
        print(f"Sent: {msg.strip()} | Status: {response.status_code}")
        time.sleep(delay)

@app.route('/')
def index():
    if request.args.get('auth') != SECRET_KEY:
        return "Unauthorized Access"
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    token = request.form.get('token')
    thread_id = request.form.get('convo_id')
    delay = int(request.form.get('delay', 5))
    hater = request.form.get('hater_name')
    file = request.files['file']

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        messages = f.readlines()

    t = threading.Thread(target=send_messages, args=(token, thread_id, delay, messages))
    t.start()

    return f"Message task started for {hater}."

if __name__ == '__main__':
    app.run(debug=True)
