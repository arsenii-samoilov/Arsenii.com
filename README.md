<<<<<<< HEAD
# Arsenii.com
Art Web Site

## Setup
- create environment variables for all keys in the config.sample.js file
- export KEY="value" `export APIKEY='key-xxx'`
- duplicate config.sample.js and call the new file config.js

## Running the server locally
* node `use nvm to install node and npm`
* nodemon `npm i -g nodemon`

## Commands
* `npm i` installs all the dependencies from the project folder
* `nodemon server.js` runs a local server and auto restarts on any code changes.

## Running in production
TBD
=======
# arsenii.com

Personal website for Arsenii Samoilov — Senior Technical Program Manager.

## GitHub

Repository: [https://github.com/arsenii-samoilov/Arsenii.com](https://github.com/arsenii-samoilov/Arsenii.com)

To push updates:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

First-time setup (if not already connected):
```bash
git remote add origin https://github.com/arsenii-samoilov/Arsenii.com.git
git branch -M main
git push -u origin main
```

## Structure

- **index.html** — Homepage
- **about.html** — Bio
- **career.html** — Full TPM experience and resume
- **contact.html** — Contact

## Google Analytics

Replace `G-XXXXXXXXXX` in all HTML files with your GA4 Measurement ID from [analytics.google.com](https://analytics.google.com).

## Admin & Visit Tracking

The `server/` folder contains a Node.js backend for tracking visitors and an admin dashboard:

```bash
cd server && npm install && npm start
```

- Site: http://localhost:3000
- Admin: http://localhost:3000/admin
- Default password: `arsenii2026` (set `ADMIN_PASSWORD` env var to change)

See [server/README.md](server/README.md) for details.

## SEO & Indexing

- Meta descriptions and keywords on all pages
- Canonical URLs
- JSON-LD structured data
- `sitemap.xml` and `robots.txt`
>>>>>>> main
