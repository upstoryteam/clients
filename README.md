# Upstory Audits

Static HTML audits Upstory sends to dream-client prospects. Each folder is one audit, fully self-contained.

## Structure

Each `[client-name]/` folder contains:

- `index.html` — the audit, with CSS, JS, fonts, logo, and any imagery inlined or referenced via CDN. No build step, no dependencies, no missing assets.
- `README.md` — internal notes (who it's for, when it was sent, status, any follow-up).

## Deployment

Auto-deploys via Vercel to `audits.upstory.co` once DNS is wired. Path-based routing means each folder becomes a URL:

- `audits.upstory.co/citizen-health/`
- `audits.upstory.co/[next-client]/`

No `vercel.json` is required for static HTML at the root.

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
