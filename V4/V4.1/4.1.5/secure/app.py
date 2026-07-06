from flask import Flask, jsonify, make_response, render_template, request
import hmac
import hashlib

# Secure implementation for ASVS 4.1.5
# Uses HMAC-SHA256 to verify per-message integrity and authenticity.
# Rejects missing, invalid, or tampered signatures.
app = Flask(__name__, template_folder='../templates', static_folder='../static')
SECRET_KEY = b'supersecretsharedkey'

TRANSFER_HISTORY = []


def calculate_signature(body: bytes) -> str:
    # Calculate HMAC-SHA256 over the raw request body.
    return hmac.new(SECRET_KEY, body, hashlib.sha256).hexdigest()


def verify_signature(signature: str, body: bytes) -> bool:
    expected = calculate_signature(body)
    # Use constant-time comparison to prevent timing attacks.
    return hmac.compare_digest(expected, signature)


@app.route('/', methods=['GET'], provide_automatic_options=False)
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.5',
        description='Secure message signing using HMAC-SHA256',
        badge='SECURE',
        badge_class='secure',
        control='4.1.5'
    )


@app.route('/transfer', methods=['POST'], provide_automatic_options=False)
def transfer():
    signature = request.headers.get('X-Signature', '')
    body = request.get_data() or b''

    if not signature:
        return make_response(jsonify({'error': 'Missing X-Signature header'}), 401)

    if not verify_signature(signature, body):
        return make_response(jsonify({'error': 'Invalid or tampered signature'}), 403)

    payload = request.get_json(silent=True)
    if not payload:
        return make_response(jsonify({'error': 'Invalid JSON payload'}), 400)

    amount = payload.get('amount')
    recipient = payload.get('recipient')
    message = payload.get('message')

    transfer = {
        'amount': amount,
        'recipient': recipient,
        'message': message,
        'status': 'completed'
    }
    TRANSFER_HISTORY.append(transfer)

    return jsonify({
        'status': 'success',
        'transfer': transfer,
        'signature': signature,
        'verification': 'passed'
    })


@app.route('/payment', methods=['POST'], provide_automatic_options=False)
def payment():
    signature = request.headers.get('X-Signature', '')
    body = request.get_data() or b''

    if not signature:
        return make_response(jsonify({'error': 'Missing X-Signature header'}), 401)

    if not verify_signature(signature, body):
        return make_response(jsonify({'error': 'Invalid or tampered signature'}), 403)

    payload = request.get_json(silent=True)
    if not payload:
        return make_response(jsonify({'error': 'Invalid JSON payload'}), 400)

    amount = payload.get('amount')
    recipient = payload.get('recipient')
    message = payload.get('message')

    payment = {
        'amount': amount,
        'recipient': recipient,
        'message': message,
        'status': 'processed'
    }
    TRANSFER_HISTORY.append(payment)

    return jsonify({
        'status': 'success',
        'payment': payment,
        'signature': signature,
        'verification': 'passed'
    })


@app.route('/admin/action', methods=['POST'], provide_automatic_options=False)
def admin_action():
    signature = request.headers.get('X-Signature', '')
    body = request.get_data() or b''

    if not signature:
        return make_response(jsonify({'error': 'Missing X-Signature header'}), 401)

    if not verify_signature(signature, body):
        return make_response(jsonify({'error': 'Invalid or tampered signature'}), 403)

    payload = request.get_json(silent=True)
    if not payload:
        return make_response(jsonify({'error': 'Invalid JSON payload'}), 400)

    action = payload.get('action')
    amount = payload.get('amount')
    recipient = payload.get('recipient')

    record = {
        'action': action,
        'amount': amount,
        'recipient': recipient,
        'status': 'approved'
    }
    TRANSFER_HISTORY.append(record)

    return jsonify({
        'status': 'success',
        'admin_action': record,
        'signature': signature,
        'verification': 'passed'
    })


@app.route('/history', methods=['GET'], provide_automatic_options=False)
def history():
    return jsonify({
        'status': 'success',
        'history': TRANSFER_HISTORY
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
