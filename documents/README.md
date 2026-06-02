# Resume download

- `Arsenii Samoilov.pdf` — public resume (PDF only on the site)

Source: export PDF from `~/Desktop/Desktop/Arsenii Resume/Arsenii Samoilov Resume.docx`

## Update the live site (no SSH)

From the repo root:

```bash
./update-resume.sh
```

That copies the Desktop PDF, commits, pushes to `main`, and GitHub Actions deploys to arsenii.com automatically.

Or manually:

```bash
cp "/Users/arsenii/Desktop/Desktop/Arsenii Resume/Arsenii Samoilov Resume.pdf" \
  documents/Arsenii\ Samoilov.pdf
./deploy.sh "Resume: sync latest PDF"
```

Check deploy status: GitHub → **Actions** → **Deploy to arsenii.com**.
