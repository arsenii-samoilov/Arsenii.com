const express = require('express');
const path = require('path');
const fs = require('fs');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'arsenii2026';
const DATA_FILE = path.join(__dirname, 'visits.json');
const SESSION_SECRET = process.env.SESSION_SECRET || 'arsenii-session-secret-change-me';

// CORS for cross-origin requests (when site is on GitHub Pages, API on Render/Railway)
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

app.use(express.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '..')));

function loadVisits() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (e) {
    return [];
  }
}

function saveVisits(visits) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(visits, null, 2));
}

function getClientIp(req) {
  return req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.socket.remoteAddress || 'unknown';
}

async function getGeo(ip) {
  if (!ip || ip === 'unknown' || ip === '::1' || ip.startsWith('127.')) return { city: 'Local', country: 'Local' };
  try {
    const res = await fetch(`http://ip-api.com/json/${ip}?fields=city,country,region`);
    const data = await res.json();
    return { city: data.city || 'Unknown', country: data.country || 'Unknown', region: data.region };
  } catch (e) {
    return { city: 'Unknown', country: 'Unknown' };
  }
}

function createToken() {
  return crypto.randomBytes(32).toString('hex');
}

const sessions = new Map();

function requireAuth(req, res, next) {
  const token = req.cookies.admin_token;
  if (token && sessions.has(token)) return next();
  res.status(401).json({ error: 'Unauthorized' });
}

app.post('/api/visit', async (req, res) => {
  try {
    const ip = getClientIp(req);
    const geo = await getGeo(ip);
    const visits = loadVisits();
    visits.push({
      page: req.body?.page || req.url,
      referrer: req.body.referrer || req.headers.referer || '',
      userAgent: req.body.userAgent || req.headers['user-agent'] || '',
      ip,
      city: geo.city,
      country: geo.country,
      region: geo.region,
      timestamp: req.body.timestamp || new Date().toISOString()
    });
    saveVisits(visits);
  } catch (e) {}
  res.status(204).end();
});

app.post('/api/login', (req, res) => {
  if (req.body.password === ADMIN_PASSWORD) {
    const token = createToken();
    sessions.set(token, { createdAt: Date.now() });
    res.cookie('admin_token', token, { httpOnly: true, maxAge: 24 * 60 * 60 * 1000 });
    res.json({ ok: true });
  } else {
    res.status(401).json({ error: 'Invalid password' });
  }
});

app.post('/api/logout', (req, res) => {
  const token = req.cookies.admin_token;
  if (token) sessions.delete(token);
  res.clearCookie('admin_token');
  res.json({ ok: true });
});

app.get('/api/visits', requireAuth, (req, res) => {
  const visits = loadVisits();
  res.json(visits.slice(-500).reverse());
});

app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`Admin: http://localhost:${PORT}/admin`);
});
