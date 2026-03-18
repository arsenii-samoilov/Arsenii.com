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
const GA4_MEASUREMENT_ID = process.env.GA4_MEASUREMENT_ID || 'G-LJE40VWDPW';
const GA4_API_SECRET = process.env.GA4_API_SECRET || '';

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

async function sendToGA4(page, pageTitle, referrer, userAgent, ip) {
  if (!GA4_API_SECRET) return;
  try {
    const clientId = crypto.createHash('sha256').update((ip || '') + (userAgent || '')).digest('hex').slice(0, 32);
    const pageLocation = page.startsWith('http') ? page : `https://arsenii.com${page.startsWith('/') ? '' : '/'}${page}`;
    const payload = {
      client_id: clientId,
      events: [{
        name: 'page_view',
        params: {
          page_location: pageLocation,
          page_title: pageTitle || 'Arsenii Samoilov',
          page_referrer: referrer || '',
          engagement_time_msec: 100
        }
      }]
    };
    const url = `https://www.google-analytics.com/mp/collect?measurement_id=${GA4_MEASUREMENT_ID}&api_secret=${GA4_API_SECRET}`;
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } catch (e) {
    console.error('GA4 forward error:', e.message);
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
    const page = req.body?.page || req.url;
    const referrer = req.body?.referrer || req.headers.referer || '';
    const userAgent = req.body?.userAgent || req.headers['user-agent'] || '';
    const visits = loadVisits();
    visits.push({
      page,
      referrer,
      userAgent,
      ip,
      city: geo.city,
      country: geo.country,
      region: geo.region,
      timestamp: req.body?.timestamp || new Date().toISOString()
    });
    saveVisits(visits);
    await sendToGA4(page, req.body?.page_title, referrer, userAgent, ip);
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
