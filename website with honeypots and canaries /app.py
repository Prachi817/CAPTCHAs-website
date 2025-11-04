from flask import Flask, request, send_from_directory, g
import os, time, json, uuid, logging
from logging.handlers import RotatingFileHandler

# Serve static files from project root
app = Flask(__name__, static_folder='.', static_url_path='')

CANARY_TOKEN = 'XyZ123Safe'
FORM_VERSION = 'v1'

# === JSON-lines logger with rotation ===
os.makedirs('logs', exist_ok=True)
handler = RotatingFileHandler('logs/app.log', maxBytes=1_000_000, backupCount=3)
handler.setLevel(logging.INFO)
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = True  # also goes to stdout if configured by server

def jlog(**event):
    event = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), **event}
    line = json.dumps(event)
    logger.info(line)
    try:
        print(line)
    except Exception:
        pass

@app.before_request
def add_request_context():
    g.req_id = str(uuid.uuid4())
    g.started = time.perf_counter()

@app.after_request
def log_request(response):
    duration_ms = int((time.perf_counter() - g.started) * 1000)
    jlog(level='info', event='http', req_id=g.req_id, method=request.method,
         url=request.full_path, status=response.status_code, duration_ms=duration_ms,
         ip=request.headers.get('X-Forwarded-For', request.remote_addr),
         ua=request.headers.get('User-Agent', ''))
    return response

@app.route('/')
def index():
    # Serve index.html from project root
    return send_from_directory('.', 'index.html')

@app.post('/submit')
def submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    website = request.form.get('website', '').strip()  # honeypot
    canary_token = request.form.get('canary_token')
    form_version = request.form.get('form_version')

    # 1) Honeypot check
    if website:
        jlog(level='warn', event='block', reason='honeypot', req_id=g.req_id)
        return ('Blocked: honeypot triggered.', 403)

    # 2) Canary checks
    if canary_token != CANARY_TOKEN or form_version != FORM_VERSION:
        jlog(level='warn', event='block', reason='canary', req_id=g.req_id,
             got={'canary_token': canary_token, 'form_version': form_version})
        return ('Blocked: canary tampering detected.', 403)

    # 3) Basic validation
    if not (name and email and message):
        jlog(level='info', event='validation_failed', req_id=g.req_id)
        return ('Please fill out all fields.', 400)

    # TODO: handle the message (store, email, etc.)
    jlog(level='info', event='submission_ok', req_id=g.req_id, name=name, email=email)
    return ('Thanks! Your message has been received.', 200)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    jlog(level='info', event='server_start', msg=f'Listening on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)
