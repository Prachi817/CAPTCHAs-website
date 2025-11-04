import express from 'express';
const upload = multer();

// === Config: canaries that must match exactly ===
const CANARY_TOKEN = 'XyZ123Safe';
const FORM_VERSION = 'v1';

// === Minimal JSON-lines logger (stdout + file) ===
const LOG_DIR = 'logs';
fs.mkdirSync(LOG_DIR, { recursive: true });
const logFile = path.join(LOG_DIR, 'app.log');
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

function log(event) {
const line = JSON.stringify({ ts: new Date().toISOString(), ...event }) + '
';
try { process.stdout.write(line); } catch {}
try { logStream.write(line); } catch {}
}

// Assign request id + basic request logging
app.use((req, res, next) => {
req.id = crypto.randomUUID();
const started = process.hrtime.bigint();
res.on('finish', () => {
const ended = process.hrtime.bigint();
const durationMs = Number(ended - started) / 1e6;
log({
level: 'info',
event: 'http',
req_id: req.id,
method: req.method,
url: req.originalUrl,
status: res.statusCode,
duration_ms: Math.round(durationMs),
ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
ua: req.headers['user-agent'] || ''
});
});
next();
});

app.use(express.static('public'));

app.post('/submit', upload.none(), (req, res) => {
const { name, email, message, website, canary_token, form_version } = req.body || {};

// 1) Honeypot: if filled, it's a bot
if (website && website.trim() !== '') {
log({ level: 'warn', event: 'block', reason: 'honeypot', req_id: req.id });
return res.status(403).send('Blocked: honeypot triggered.');
}

// 2) Canaries: must match exactly
if (canary_token !== CANARY_TOKEN || form_version !== FORM_VERSION) {
log({ level: 'warn', event: 'block', reason: 'canary', req_id: req.id, got: { canary_token, form_version } });
return res.status(403).send('Blocked: canary tampering detected.');
}

// 3) Basic validation
if (!name || !email || !message) {
log({ level: 'info', event: 'validation_failed', req_id: req.id });
return res.status(400).send('Please fill out all fields.');
}

// TODO: handle the message (store, email, etc.)
log({ level: 'info', event: 'submission_ok', req_id: req.id, name, email });
return res.status(200).send('Thanks! Your message has been received.');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
log({ level: 'info', event: 'server_start', msg: `Listening on http://localhost:${PORT}` });
});