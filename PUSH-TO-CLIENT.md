# Pushing briefs to Upstory’s GitHub (Vercel deploy)

Your laptop folder can live anywhere (e.g. `~/Desktop/upstory/audits/`). Vercel only sees **their** GitHub repo on the branch configured in the project (usually `main`).

## What actually deploys

Production needs **repo root** on Vercel:

- `vercel.json`
- `shared/` (CSS, logos, Rick photo)
- Each `<slug>/index.html` growth brief

Optional on the same deploy: `qa-briefs.html`, `growth-brief-review.csv` (no emails; internal QA).

**Do not push** (gitignored here): `data/`, service account JSON, contact CSVs with emails, `.env`, `.vercel/`.

## Additive push (safe)

Goal: add new Wave 2 slugs without deleting what they already have (Stake, Citizen Health, etc.).

1. In GitHub (their org), open the repo Vercel → Settings → Git shows.
2. Clone it next to your work:

   ```bash
   git clone git@github.com:THEIR-ORG/THEIR-REPO.git ~/Desktop/upstory/clients-site
   cd ~/Desktop/upstory/clients-site
   git pull origin main
   ```

3. Copy **only deploy artifacts** from your audits folder (rsync is explicit):

   ```bash
   AUDITS=~/Desktop/upstory/audits   # your path after the move
   CLIENT=~/Desktop/upstory/clients-site

   rsync -av "$AUDITS/shared/" "$CLIENT/shared/"
   rsync -av "$AUDITS/vercel.json" "$CLIENT/"
   rsync -av "$AUDITS/qa-briefs.html" "$CLIENT/" 2>/dev/null || true

   # Every slug dir that has a growth brief
   for d in "$AUDITS"/*/; do
     [ -f "${d}index.html" ] || continue
     slug=$(basename "$d")
     case "$slug" in shared|scripts|data|skills|node_modules) continue ;; esac
     rsync -av "$d" "$CLIENT/$slug/"
   done
   ```

4. Review what changed:

   ```bash
   cd "$CLIENT"
   git status
   git diff --stat
   ```

5. Commit and push **their** repo:

   ```bash
   git add shared vercel.json qa-briefs.html */index.html
   git commit -m "Add Wave 2 growth briefs for clients.upstory.co"
   git push origin main
   ```

6. Vercel builds automatically. When Production is green, check:

   `https://clients.upstory.co/blackbird-labs`

## Your fork (`stephdiedrich/upstory-audits`)

That remote is for your backup/work. Pushing there does **not** update `clients.upstory.co` unless Vercel is wired to that repo (usually it is not).

## After you move the folder on your Mac

1. Move the whole `upstory-audits` directory (Finder or `mv`).
2. Re-open the project in Cursor from the **new** path.
3. Put the GCP JSON in `~/Desktop/upstory/credentials/` (sibling to `audits/`), or set:

   ```bash
   export USTORY_GCP_SERVICE_ACCOUNT_JSON=~/Desktop/upstory/credentials/upstory-494617-fe9165a30344.json
   ```

4. Copy the news export into `audits/data/wave2-company-news-export.csv` if you re-run personalization scripts.

Git history and remotes move with the folder; no need to re-clone your audits repo.
