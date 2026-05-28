# Deploying growth briefs (client handoff)

## How this repo is meant to work

Each company brief lives in its **own URL path**, not its own isolated folder on disk:

| Path on site | Files in repo |
|--------------|----------------|
| `https://clients.upstory.co/stake` | `stake/index.html` |
| `https://clients.upstory.co/citizen-health` | `citizen-health/index.html` (growth brief) |
| `https://clients.upstory.co/citizen-health/legacy-audit` | `citizen-health/legacy-audit/index.html` (archived long-form) |
| `https://clients.upstory.co/shared/...` | `shared/*` (shared by all growth briefs) |

**One Vercel (or static) project deploys the whole repo root.** Path-based routing serves each `/<slug>/index.html`. There are **no links between briefs**; pages do not reference each other.

## What is shared today (growth brief format)

`stake/index.html` (and future `<slug>/index.html` briefs) load assets from the **site root**, not from inside the slug folder:

| Reference in HTML | Repo path |
|-------------------|-----------|
| `/shared/brief.css` | `shared/brief.css` |
| `/shared/upstory-logo.png` | `shared/upstory-logo.png` |
| `/shared/rick-russie.avif` | `shared/rick-russie.avif` |
| `/shared/logos/<slug>.svg` | `shared/logos/<slug>.svg` |

Fonts load from Google Fonts via `brief.css` (network required).

**These paths break if you upload only `stake/`** without also deploying `shared/` at the domain root.

## Safe handoff to the client

### Option A — Recommended: deploy the full repo

1. Client connects this GitHub repo to Vercel (or similar).
2. Point subdomain DNS (e.g. `clients.upstory.co`) at that project.
3. Keep **`shared/`** and every **`<slug>/`** folder in the same deployment.
4. Do **not** need `skills/` for production (agent tooling only; optional to omit from deploy or leave in repo).

Result: `/stake`, `/shared/brief.css`, etc. all resolve. URLs omit trailing slashes (`vercel.json` → `trailingSlash: false`). Adding a new brief = new `<slug>/` folder + logo in `shared/logos/` + redeploy.

### Option B — One folder per deploy (not supported out of the box)

If the client must deploy **only** `stake/` as a separate project or subdirectory app, you must either:

- Copy into `stake/`: `brief.css`, Upstory logo, Rick avatar, and `stake.svg`, then change HTML to **relative** paths (e.g. `./assets/...`), or
- Run a small build step that bundles shared files per slug.

The skill docs assume **Option A** unless you add a bundle step.

## Citizen Health vs growth briefs

| | Growth brief (`stake/`) | Citizen Health audit |
|--|-------------------------|----------------------|
| Format | `FORMAT.md` six-block brief | Long-form audit (inline CSS) |
| Shared deps | `shared/brief.css` + `shared/*` | Assets under `/citizen-health/` |
| Self-contained on disk | No (uses `/shared/`) | Yes for that page’s assets |

Do not mix patterns without updating paths.

## Next.js host (if they migrate off static HTML)

- Copy repo `shared/` → `public/shared/` once per app.
- Each brief → `app/<slug>/page.tsx` from `scaffold.tsx`.
- Same absolute paths: `/shared/...` still work.

## Checklist before transfer

- [ ] Client will deploy **repo root**, not individual slug folders alone.
- [ ] `shared/upstory-logo.png` and `shared/rick-russie.avif` are in the repo (not gitignored).
- [ ] Each new brief has `shared/logos/<slug>.svg` (or `.png`) if using co-branded header.
- [ ] `skills/` explained as internal generator tooling (optional in their workflow).
- [ ] DNS + Vercel project documented for their subdomain.

## Adding a new growth brief

1. Create `<slug>/index.html` (copy `stake/` structure or generate from skill).
2. Add `shared/logos/<slug>.svg` + `shared/logos/<slug>.meta.json`.
3. Commit; redeploy. URL is `/<slug>/`.

No changes to other briefs required.
