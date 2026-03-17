# Google Analytics GA4 Troubleshooting

If GA4 isn't showing data or "does not come up", check these:

## Quick test: Debug mode
Visit your site with `?ga_debug=1` (e.g. `https://arsenii.com/?ga_debug=1`).
Open the browser console (F12 → Console). You should see GA4 debug messages if the tag is firing.

## 1. Verify Measurement ID
- Go to [analytics.google.com](https://analytics.google.com) → Admin → Data Streams
- Click your Web stream → copy the **Measurement ID** (starts with `G-`)
- It must exactly match `G-LJE40VWDPW` in the code (case-sensitive)

## 2. Data Stream URL
- In Data Streams → your stream → **Stream details**
- Ensure the **Website URL** includes your live domain (e.g. `https://arsenii.com`)
- If using GitHub Pages with custom domain, add `arsenii.com`
- If using `*.github.io`, add that domain

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
