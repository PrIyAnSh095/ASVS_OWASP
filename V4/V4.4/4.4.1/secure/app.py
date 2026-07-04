# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request
# pyrefly: ignore [missing-import]
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/chat')
def chat(ws):
    if not request.is_secure:
        ws.send("ERROR: Connection rejected. WSS is required.")
        ws.close()
        return

    ws.send("Welcome to the Secure Chat! Your connection is encrypted (WSS).")
    while True:
        data = ws.receive()
        if data is None:
            break
        ws.send(f"Secure Echo: {data}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
