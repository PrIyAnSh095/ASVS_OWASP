from flask import Flask, jsonify, make_response, render_template, request

# Vulnerable implementation for ASVS 4.1.5
# Accepts requests even when the X-Signature header is missing or invalid.
app = Flask(__name__, template_folder='../templates', static_folder='../static')
TRANSFER_HISTORY = []


@app.route('/', methods=['GET'], provide_automatic_options=False)
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.5',
        description='Vulnerable message processing without signature verification',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control='4.1.5'
    )


@app.route('/transfer', methods=['POST'], provide_automatic_options=False)
def transfer():
    payload = request.get_json(silent=True)
    amount = payload.get('amount') if payload else None
    recipient = payload.get('recipient') if payload else None
    message = payload.get('message') if payload else None

    TRANSFER_HISTORY.append({
        'amount': amount,
        'recipient': recipient,
        'message': message,
        'status': 'completed'
    })

    return jsonify({
        'status': 'success',
        'transfer': {
            'amount': amount,
            'recipient': recipient,
            'message': message,
            'status': 'completed'
        },
        'signature': request.headers.get('X-Signature', ''),
        'verification': 'skipped'
    })


@app.route('/payment', methods=['POST'], provide_automatic_options=False)
def payment():
    payload = request.get_json(silent=True)
    amount = payload.get('amount') if payload else None
    recipient = payload.get('recipient') if payload else None
    message = payload.get('message') if payload else None

    TRANSFER_HISTORY.append({
        'amount': amount,
        'recipient': recipient,
        'message': message,
        'status': 'processed'
    })

    return jsonify({
        'status': 'success',
        'payment': {
            'amount': amount,
            'recipient': recipient,
            'message': message,
            'status': 'processed'
        },
        'signature': request.headers.get('X-Signature', ''),
        'verification': 'skipped'
    })


@app.route('/approve', methods=['POST'], provide_automatic_options=False)
def approve():
    payload = request.get_json(silent=True)
    action = payload.get('action') if payload else None
    amount = payload.get('amount') if payload else None
    recipient = payload.get('recipient') if payload else None

    TRANSFER_HISTORY.append({
        'action': action,
        'amount': amount,
        'recipient': recipient,
        'status': 'approved'
    })

    return jsonify({
        'status': 'success',
        'approved': {
            'action': action,
            'amount': amount,
            'recipient': recipient,
            'status': 'approved'
        },
        'signature': request.headers.get('X-Signature', ''),
        'verification': 'skipped'
    })


@app.route('/admin/action', methods=['POST'], provide_automatic_options=False)
def admin_action():
    payload = request.get_json(silent=True)
    action = payload.get('action') if payload else None
    amount = payload.get('amount') if payload else None
    recipient = payload.get('recipient') if payload else None

    TRANSFER_HISTORY.append({
        'action': action,
        'amount': amount,
        'recipient': recipient,
        'status': 'executed'
    })

    return jsonify({
        'status': 'success',
        'admin_action': {
            'action': action,
            'amount': amount,
            'recipient': recipient,
            'status': 'executed'
        },
        'signature': request.headers.get('X-Signature', ''),
        'verification': 'skipped'
    })


@app.route('/history', methods=['GET'], provide_automatic_options=False)
def history():
    return jsonify({
        'status': 'success',
        'history': TRANSFER_HISTORY
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
