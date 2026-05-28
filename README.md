# Upstory Audits

Static HTML audits Upstory sends to dream-client prospects. Each `<client>/` folder is one **URL** (`audits.example.com/<client>`). Growth briefs share repo-level `shared/` assets; see **`DEPLOY.md`** before handoff.

## Structure

Each `[client-name]/` folder contains:

- `index.html` — the page. Long audits (e.g. Citizen Health) keep assets in-folder; **growth briefs** link to `/shared/brief.css` and `/shared/logos/<slug>.*` (deploy the whole repo root).
- `README.md` — internal notes (who it's for, when it was sent, status, any follow-up).

The `shared/` folder holds cross-audit assets (Upstory logo, Rick photo) served at `/shared/` for growth brief closers and future audits.

## Deployment

Auto-deploys via Vercel to `audits.upstory.co` once DNS is wired. Path-based routing means each folder becomes a URL:

- `audits.upstory.co/citizen-health` (long-form audit)
- `audits.upstory.co/citizen-health/brief` (growth brief format)
- `audits.upstory.co/stake`, `audits.upstory.co/abby-care` (growth briefs)
- `audits.upstory.co/qa-briefs.html` (internal QA index — context + links to all growth briefs)
- Priority 1 previews (draft): `akko/`, `cloaked/`, `eternal/`, `dorsia/`, `caramel/`, `brave/`, `whisker-labs/`, `vinovest/`, `goldin/`, `poparide/`, `portola/`, `legit-app/`, `winit/`, `lolli/`, `getmyboat/`, `swifto/`
- `audits.upstory.co/[next-client]`

`vercel.json` only sets `trailingSlash`. **Client handoff:** read `DEPLOY.md` (full-repo deploy vs per-folder pitfalls).

## Brand and voice

All audits follow the Upstory brand and voice system (eventually codified as the `upstory-asset-creator` skill). Key rules:

- Brand tokens live in the audit HTML as CSS variables and stay verbatim across audits.
- Client colors only appear inside mockups of the client's own product. Never in our analytical tools (calculators, stat blocks, page chrome).
- No em dashes. No decorative italics. Single CTA per audit. Sentence-shaped headlines.
- Soft pitch in the closer. Value-add first, engagement opt-in second.

## Privacy

Each audit ships with `<meta name="robots" content="noindex, nofollow">` so it stays out of search engines. URLs are obscure but the content is intentionally shareable with the named recipient.

## Adding a new audit

1. Create a `[client-name]/` folder.
2. Build `index.html` (use the skill when ready, or copy from an existing audit as a starting point).
3. Add a per-audit `README.md` with internal notes.
4. Commit and push. Vercel deploys automatically.
