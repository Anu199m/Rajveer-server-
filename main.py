from flask import Flask, request, render_template_string
import requests
import time
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>Rajveer FB Message Server</title></head>
<body style="text-align:center; margin-top: 50px;">
  <h2>🚀 Facebook Message Automation</h2>
  <form method="POST" enctype="multipart/form-data">
    <input type="text" name="token" placeholder="Access Token" required><br><br>
    <input type="text" name="convo_id" placeholder="Conversation ID" required><br><br>
    <input type="text" name="sender" placeholder="Sender Name" required><br><br>
    <input type="number" name="timer" placeholder="Time (seconds)" value="2" required><br><br>
    <input type="file" name="file" accept=".txt" required><br><br>
    <button type="submit">🚀 Start Sending</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form["token"]
        convo_id = request.form["convo_id"]
        sender = request.form["sender"]
        timer = int(request.form["timer"])
        file = request.files["file"]

        messages = file.read().decode("utf-8").splitlines()
        sent = 0

        for msg in messages:
            full_msg = f"{sender}: {msg}"
            url = f"https://graph.facebook.com/v19.0/{convo_id}/messages"
            headers = {"Content-Type": "application/json"}
            try:
                requests.post(url, json={"message": {"text": full_msg}}, params={"access_token": token}, headers=headers)
                sent += 1
                time.sleep(timer)
            except Exception as e:
                print(f"Error: {e}")
                break

        return f"<h3>✅ {sent} messages sent!</h3>"

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
