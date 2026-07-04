from flask import Flask, jsonify, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.1',
        description='Content-Type Verification',
        badge='SECURE',
        badge_class='secure',
        control='4.1.1'
    )

@app.route('/json')
def json_endpoint():
    payload = {
        'status': 'secure',
        'message': 'application/json with charset=UTF-8'
    }
    response = jsonify(payload)
    response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return response

@app.route('/html')
def html_endpoint():
    html = (
        '<!doctype html>'
        '<html><head><meta charset="UTF-8"></head>'
        '<body><h1>HTML response</h1><p>Correct text/html charset UTF-8.</p></body></html>'
    )
    return Response(html, content_type='text/html; charset=UTF-8')

@app.route('/xml')
def xml_endpoint():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<note>'
        '<status>secure</status>'
        '<message>application/xml with charset=UTF-8</message>'
        '</note>'
    )
    return Response(xml, content_type='application/xml; charset=UTF-8')

@app.route('/text')
def text_endpoint():
    return Response('Plain text response with charset=UTF-8\n', content_type='text/plain; charset=UTF-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
