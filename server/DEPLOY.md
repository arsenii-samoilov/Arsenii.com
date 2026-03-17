# Deploy Analytics Server

Deploy the Node server to enable visit tracking and the admin analytics page.

## Option 1: Render (Free tier)

1. Go to [render.com](https://render.com) and sign up.
2. **New → Web Service**
3. Connect your GitHub repo `arsenii-samoilov/Arsenii.com`
4. Configure:
   - **Root Directory**: `server`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. **Environment**:
   - `ADMIN_PASSWORD` — Set a strong password for admin login
   - `SESSION_SECRET` — Generate a random string (e.g. `openssl rand -hex 32`)
6. Deploy. You'll get a URL like `https://arsenii-analytics.onrender.com`

## Option 2: Railway

1. Go to [railway.app](https://railway.app) and sign up.
2. **New Project → Deploy from GitHub** → select your repo
3. Configure:
   - **Root Directory**: `server`
   - **Start Command**: `node server.js` (or use the Procfile)
4. **Variables**: Add `ADMIN_PASSWORD` and `SESSION_SECRET`
5. Deploy and copy the public URL

## After deployment

1. Edit `api-config.js` in your repo root:
   ```js
   window.ARSENII_API_URL = 'https://your-app.onrender.com';  // Your server URL
   ```

2. Commit and push. Your static site (GitHub Pages) will now send visits to the API.

3. **Admin page**: Visit `https://your-app.onrender.com/admin` and log in with `ADMIN_PASSWORD`.

## Optional: Custom domain

On Render/Railway, add a custom domain like `api.arsenii.com` and point a CNAME record to the host. Then use that URL in `api-config.js`.
