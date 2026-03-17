# Admin & Visit Tracking

## Setup

1. Install dependencies:
   ```bash
   cd server && npm install
   ```

2. Set environment variables (optional):
   - `ADMIN_PASSWORD` — Admin login password (default: arsenii2026)
   - `PORT` — Server port (default: 3000)
   - `SESSION_SECRET` — For production, set a random secret

3. Run the server:
   ```bash
   npm start
   ```

## Usage

- **Site**: http://localhost:3000 (serves the static site + API)
- **Admin**: http://localhost:3000/admin
- **Login**: Use the password from ADMIN_PASSWORD

## Deployment

Deploy the server to a Node.js host (Railway, Render, Fly.io, etc.). Set ADMIN_PASSWORD and SESSION_SECRET in the host's environment. Point your domain to the server.

For static-only hosts (GitHub Pages, Netlify): The tracking and admin require the Node server. Deploy the server separately and update track.js to use the full API URL (e.g. `https://api.arsenii.com/api/visit`).
