from flask import Flask, jsonify, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='ASVS V4.1.1',
        description='Content-Type Verification',
        badge='VULNERABLE',
        badge_class='vulnerable',
        control='4.1.1'
    )

@app.route('/json')
def json_endpoint():
    payload = {
        'status': 'vulnerable',
        'message': 'JSON returned with text/html'
    }
    response = jsonify(payload)
    response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    return response

@app.route('/html')
def html_endpoint():
    html = (
        '<!doctype html>'
        '<html><head><meta charset="UTF-8"></head>'
        '<body><h1>HTML</h1><p>HTML is returned as plain text without a correct content type.</p></body></html>'
    )
    return Response(html, content_type='text/plain')

@app.route('/xml')
def xml_endpoint():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<response>'
        '<status>vulnerable</status>'
        '<message>application/xml is served as text/plain</message>'
        '</response>'
    )
    return Response(xml, content_type='text/plain; charset=UTF-8')

@app.route('/text')
def text_endpoint():
    return Response('Plain text response missing charset\n', content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
