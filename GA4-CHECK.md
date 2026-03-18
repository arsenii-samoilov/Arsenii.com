# Google Analytics GA4 Troubleshooting

If GA4 isn't showing data or "does not come up", check these:

## Pi-hole: Whitelist these domains (Group management → Domains → Whitelist)

- `analytics.google.com` — GA4 dashboard
- `www.googletagmanager.com` — gtag.js script
- `googletagmanager.com`
- `www.google-analytics.com` — data collection
- `google-analytics.com`
- `region1.google-analytics.com` (optional)

After adding, restart DNS: `pihole restartdns` (or use Pi-hole UI).

## If GA4 keeps going down intermittently
- **Measurement ID may be invalid**: Go to [analytics.google.com](https://analytics.google.com) → Admin → Data Streams. If the property was reset or the stream was deleted, create a new Web stream and copy the new Measurement ID (G-XXXXXXXXXX). Update all HTML files.
- **Create a fresh GA4 property**: Admin → Create property → Add stream → Web → copy the new G- ID. Replace G-LJE40VWDPW in all files.

## Quick test: Debug mode
In GA4 Admin → DebugView, or add `debug_mode: true` to the config:
```js
gtag('config', 'G-LJE40VWDPW', { debug_mode: true });
```
Then open the browser console (F12) when visiting your site.

## 1. Verify Measurement ID
- Go to [analytics.google.com](https://analytics.google.com) → Admin → Data Streams
- Click your Web stream → copy the **Measurement ID** (starts with `G-`)
- It must exactly match `G-LJE40VWDPW` in the code (case-sensitive)

## 2. Data Stream URL (critical for page counting)
- In Data Streams → your stream → **Stream details**
- **Website URL** must exactly match your live domain:
  - If your site is `https://arsenii.com` → use `https://arsenii.com` (no www)
  - If your site is `https://www.arsenii.com` → use `https://www.arsenii.com`
- Mismatch (e.g. stream set to www but site is non-www) can cause data loss
- If using GitHub Pages with custom domain, use `https://arsenii.com`

## 3. Test in Real-time
- Visit your live site (arsenii.com)
- In GA4: **Reports → Realtime**
- You should appear within 1–2 minutes
- **Disable ad blockers** when testing (uBlock, Privacy Badger, etc.)

## 4. Debug mode (optional)
Add `?debug_mode=true` to your config temporarily to see events in the browser console:
```js
gtag('config', 'G-LJE40VWDPW', { send_page_view: true, debug_mode: true });
```

## 5. Processing delay
- **Realtime** updates in minutes
- **Standard reports** can take 24–48 hours

## 6. Tag Assistant
- Use [Tag Assistant](https://tagassistant.google.com) to verify the tag fires on your site

## 7. Low active users / page count not increasing
- **Data stream URL**: Verify step 2 above — URL mismatch is a common cause
- **Pages with GA4**: index (home), about.html, career.html, contact.html, pricing.html — all use Measurement ID `G-LJE40VWDPW` with explicit `page_path` and `page_title`
- **Engagement report**: Reports → Engagement → Pages and screens — verify each page appears
- **Realtime**: Visit each page (/, /about.html, /career.html, /contact.html) and confirm events in Realtime

## 8. Server-side GA4 (bypasses Pi-hole/adblockers)

When the analytics server is deployed with `GA4_API_SECRET`:
1. track.js sends visits to your server (set `ARSENII_API_URL` in api-config.js)
2. Server forwards to GA4 Measurement Protocol
3. Works even when client-side gtag is blocked

**Setup**: analytics.google.com → Admin → Data Streams → your stream → Measurement Protocol API secrets → Create. Add the secret to Render/Railway as `GA4_API_SECRET`.
