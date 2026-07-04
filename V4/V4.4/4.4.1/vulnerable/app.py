# pyrefly: ignore [missing-import]
from flask import Flask, render_template
# pyrefly: ignore [missing-import]
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/chat')
def chat(ws):
    ws.send("Welcome to the Vulnerable Chat! Your connection is NOT encrypted.")
    while True:
        data = ws.receive()
        if data is None:
            break
        ws.send(f"Insecure Echo: {data}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
