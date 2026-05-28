---
name: upstory-growth-brief-generator
description: Generate one Upstory growth brief page (headline → insight → opportunities with artifacts → ways to measure → pitch) from a structured CSV row. Output is `app/[company-slug]/page.tsx` matching FORMAT.md and examples/stake.tsx. Run QA.md before ship. Not for long-form audits or unstructured inputs.
---

# Upstory Growth Brief Generator

A skill for producing one cold-outreach brief page at a time from structured company research. Each page is a short, confident strategy memo that lives at `audits.upstory.co/<company-slug>` and gets linked from a personal email to a senior leader at the recipient company.

## When to use

Use this skill when given one CSV row (or equivalent structured input) for an Upstory target. The skill produces exactly one `.tsx` file. Run it once per company. If processing many companies, invoke the skill once per row.

Do not use this skill for:

- Long-form bespoke audits (those follow the Upstory audit pattern, e.g., the Citizen Health audit).
- Generic marketing or capabilities pages.
- Inputs that aren't structured per the required fields below.

## Required input fields

The skill expects the following named fields. All are required.

- **Company Name** (e.g., "Stake", "Citizen Health")
- **CasualizedName** — short form used in copy (e.g., "Stake")
- **Trust Type** — one of: `Money`, `Identity`, `Health`, `Real-World Action`, `Reputation`
- **Recent News Summary** — a paragraph about recent funding, launches, acquisitions, or partnerships
- **Outreach Insight** — a paragraph reasoning about where the company is going and what is high-leverage
- **Hiring Focus Summary** — what roles the company is hiring for (signals which outcomes they optimize for)
- **Person Enrichment Summary** — context about the named recipient
- **First Name** — recipient first name

### Edge cases

- **Trust Type is `None` or anything other than the five supported values.** Stop. Tell the user which row you received and ask how they want to handle it. Do not invent a template.
- **Any field is empty or thinner than ~15 words.** Stop. Flag the specific field by name. Do not invent content to compensate.
- **First Name is missing.** Stop. Briefs are personally addressed and shouldn't go out generic.
- **You cannot find a usable company logo URL from the company's own site.** Stop and ask the user for a logo URL. Do not guess domains (e.g. `stake.com` is the wrong company; renter Stake uses `stakerent.com`). Prefer SVG/PNG from their marketing site, not third-party logo APIs unless verified.

## What the skill produces

One `.tsx` file. The content is a fully formed Next.js App Router page (default-export React component plus a `metadata` export). The file should be written to `app/<slug>/page.tsx` in the user's Next.js project.

Assumptions about the host project:

- Next.js 14+ with the App Router enabled.
- Tailwind CSS configured.
- Inter font loaded at the root layout (so `font-sans` resolves to Inter).
- No additional dependencies required. Use a plain `<img>` for the company logo (not `next/image`) unless the host project already allows the logo domain.

## Slug generation

Company Name → slug:

1. Lowercase.
2. Replace spaces with dashes.
3. Strip non-alphanumeric characters except dashes.
4. Collapse multiple dashes, strip leading/trailing dashes.

Examples:

- "Citizen Health" → `citizen-health`
- "Stake" → `stake`
- "OurFamilyWizard" → `ourfamilywizard`
- "Super Unlimited Inc." → `super-unlimited-inc`

## Page structure (locked — read `FORMAT.md` first)

**Six blocks, fixed order.** Do not add sections. Reference: `examples/stake.tsx`, `stake/index.html`.

| Order | Block | Notes |
|-------|--------|--------|
| 1 | **Co-branded header** | `BriefHeader` — Upstory for client logo; see `LOGO-TONE.md` |
| 2 | **Outcome headline** | `OutcomeHeadline` — Manrope, quantified, “We believe we can help…” |
| 3 | **Insight** | `MainInsight` — eyebrow `Our read`, lightbulb, **unique per client**, max 3 sentences |
| 4 | **Opportunities** | `OpportunitiesIntro` + three `SolutionBlock`s — optional **artifacts** per block |
| 5 | **Ways to measure success** | `WaysToMeasure` — three bronze-dot bullets, same metric as headline |
| 6 | **Pitch** | `UpstoryCloser` + `BriefFooter` — **locked** copy |

**Insight** is the only block that should read completely different company to company. Headline, opportunities, artifacts, and measure bullets are derived from the CSV row but follow the same shape every time.

**Artifacts** (`journey`, `funnel`, `chips`) are optional per block. They must add clarity, not fill space. Prefer one strong visual (often funnel on `02`). See `FORMAT.md` and `QA.md` artifact checks.

**Before ship:** run every item in `QA.md` (tone, no AI gobbledygook, artifacts earn their space, layout not truncating).

Headline must include a number or defensible range in a **we can help** frame. Map opportunities from **Outreach Insight** and **Hiring Focus**. Trust-type hints below are **starting angles** when the row is thin — not verbatim paste unless the row offers nothing specific.

### Trust-type solution hints (for visuals + copy)

| Trust Type | Solution 1 angle | Solution 2 angle | Funnel/key moment |
|---|---|---|---|
| Money | Value before deposit | First money action | Payment / transfer |
| Identity | Why share data | First useful output | Connect / verify |
| Health | Reduce intake load | First session win | Book / complete visit |
| Real-World Action | Reversible commit | Show up | Complete action |
| Reputation | Proof before risk | First public signal | Review / badge |

### Trust-type copy hints (for opportunities + measure bullets when the row is thin)

Use these as angles inside **opportunity blocks** and **ways to measure** — rewrite in the client’s language. Do not add a sixth section. When Outreach Insight is rich, **ignore generic templates** and write specific copy (see `examples/stake.tsx`).

#### Money template (Trust Type = `Money`)

- Sequencing value before friction, showing the payoff before asking for sensitive financial information.
- One concrete reassurance element at the moment of commit, whether a badge, social proof, or guarantee.
- Post-commit confirmation that converts to action within 24 hours, not generic onboarding.

#### Identity template (Trust Type = `Identity`)

- Making the value of data sharing explicit and immediate, not buried in terms of service.
- Showing reversibility at the moment of commit, with clear paths to edit, delete, or withdraw.
- A first-week moment that proves the data they gave you is doing something useful for them.

#### Health template (Trust Type = `Health`)

- Reducing the cognitive load of the first health input, where progressive disclosure beats long forms.
- Building credibility before asking for symptoms or history, through clinical signals and named providers.
- A first-session outcome that gives the user something to take away, whether a summary, next step, or just peace of mind.

#### Real-World Action template (Trust Type = `Real-World Action`)

- Making commitment feel reversible until the last possible moment, even when the action itself cannot be undone.
- Sharpening the proof that the other side will hold up their end, with host verification, guarantees, or escrow.
- A pre-action moment that lowers anxiety, through preview, walkthrough, or sample.

#### Reputation template (Trust Type = `Reputation`)

- Surfacing third-party proof before the user takes a reputational risk, not after they have already committed.
- Making the first public signal easy to generate, so early users become visible advocates without extra friction.
- A post-commit moment that gives them something shareable or countable within the first week.

### Ways to measure success (`WaysToMeasure`)

Block 5 in the arc. Same header pattern as **Opportunities**.

- **Title (locked):** `Ways to measure success`
- **Lead (default, locked unless reviewed):** `A few ideas for leading indicators we could track with you.`
- **Body:** three bronze-dot bullets, serif, one sentence each, full column width.

**Bullet 1 (north-star):** metric + denominator + time window.  
**Bullet 2 (cohort / instrumentation):** how you isolate signal.  
**Bullet 3 (readout):** what success looks like, tied to the headline quant; conservative ranges if the row is thin.

Must reference the **same primary metric** as the outcome headline.

Trust-type measurement defaults when the row is thin:

| Trust Type | Bullet 1 anchor | Bullet 2 isolation | Bullet 3 readout |
|---|---|---|---|
| Money | First money action rate, 30-day window | Partner channel vs. organic cohort | +X pp vs. control; secondary funding/activation event |
| Identity | Connect / verify completion, 7-day window | New vs. returning user split | +X pp completion; time-to-first useful output |
| Health | Intake or first-session completion | Landing source or condition segment | +X pp completion; clinician handoff or summary delivered |
| Real-World Action | Booking or show-up rate | Intent source or inventory type | +X pp show-up; no-show rate flat or down |
| Reputation | Public signal rate (review, share, badge) | High-intent vs. browse cohort | +X signals per 100 commits; time-to-first public proof |

### Upstory closer (locked layout, block 6)

Matches the [Citizen Health audit](https://upstory-audits.vercel.app/citizen-health/) closer: Upstory owns the bottom; all company value sits above.

**Structure (use `UpstoryCloser` in `scaffold.tsx`):**

1. Top border rule, generous top padding.
2. **Upstory logo** — `<img src="/shared/upstory-logo.png">` (not the company logo).
3. **Firm pitch** — locked copy below. Do not paraphrase.

> **Upstory is a product design firm.** We specialize in growth and retention for consumer products that ask for sensitive information. Our focus is in health, fintech, and identity, with client work featuring LifeMD, Firefox, and Wander.

4. **Rick signature block:** circular avatar (`/shared/rick-russie.avif`), name `Rick Russie`, title `Founder and Design Lead, Upstory`.
5. **CTA:** text link `upstory.co` → `https://www.upstory.co` with external-arrow styling. No calendar button, no "Book 30 minutes" pill.

No "happy to chat" / "if helpful" copy.

### Tagline footer

Thin top border. Flex row:

- **Line (locked):** `We design the moments where consumer products earn users.`
- **Meta (locked):** `© Upstory 2026`

## Shared assets (required in host project)

Copy the repo `shared/` folder into the Next.js host as `public/shared/`:

| File | Use |
|---|---|
| `upstory-logo.png` | Closer logo |
| `rick-russie.avif` | Rick avatar |

On this static audits repo (Vercel), files are served at `/shared/<file>`. Same paths in generated pages.

## Page design

Warm `#fcfcfa`, Manrope + Source Serif 4, bronze accent. **700px** column; prose and artifacts span full column width (no `ch` caps on body or visuals).

| File | Role |
|------|------|
| `FORMAT.md` | Locked six-block arc + layout rules |
| `QA.md` | Pre-ship quality checklist (tone, artifacts, jargon) |
| `brief-ui.tsx` | `BriefHeader`, `OutcomeHeadline`, `MainInsight`, `OpportunitiesIntro`, `SolutionBlock`, `WaysToMeasure`, `UpstoryCloser` |
| `shared/brief.css` | Static HTML/CSS mirror |
| `examples/stake.tsx` | Filled reference brief |

**If structure does not match `FORMAT.md`, the skill failed.** If structure matches but copy fails `QA.md`, fix copy before ship.

## Company logo (per brief, required)

Extract the logo **from the company's own marketing site** (header or footer asset). Save a stable copy under `shared/logos/<slug>.svg` (or `.png`) in this repo when generating static previews. In Next.js hosts, also place under `public/shared/logos/`.

Layout: **`BriefHeader`** with `clientLogoTone` and `headerVariant` (see `LOGO-TONE.md`). Never edit client logo files. Cache `shared/logos/<slug>.meta.json`. Page title: `Upstory for {Company Name}`.

`{{company_logo_url}}` in generated pages should be `/shared/logos/<slug>.svg` when cached locally, or the absolute CDN URL from their site if the host does not cache assets.

Page title: `Upstory for {Company Name}` (not `For {First Name} at …`).

## Voice and style rules

Hard constraints.

### Never

- The word **"trust"** in external-facing copy.
- **Em dashes** in page copy. Use periods or commas.
- **Contrast pivots** that read like AI: “it’s not X, it’s Y,” “not X but Y,” or a positive clause followed by **“, not …”** (e.g. “within a week, not a month out”). Write what you mean in one affirmative sentence.
- **actually**, **real** / **something real** / **a real [noun]** as hype or emphasis (the category phrase **real-world** is fine in internal docs only; do not use **real** on the brief page).
- AI-sounding language: "leverage" (as a noun), "synergy", "ecosystem", "unlock potential", "drive value", "best-in-class", "world-class", "deep dive", "circle back", "touch base", "make a dent", "move the needle".
- Closer fluff: "happy to chat", "if helpful", "would love to", "looking forward to hearing from you".
- Decorative italics.
- Summarizing what the recipient already knows.
- Generic praise ("exciting time for X").
- Headlines without a **quantified, measurable outcome** (see `QA.md` outcome headline section).
- More than 3 sentences in a section paragraph.
- Publishing without quantified headline, logo, three opportunities, or ways to measure section.
- Shipping without running `QA.md`.
- Forcing an artifact on every opportunity when prose alone is enough.
- Using client brand colors for page background, surfaces, or accents.

### Always

- Plain, confident language.
- **Outcome headline:** one measurable result + number/range + “We believe we can help {CasualizedName}…”
- **Insight:** why that outcome is reachable in *their* product now; no duplicate lecture.
- Specific product, channel, audience, moment.
- Active voice. One idea per sentence. **Affirmative phrasing** (say what happens, not what it isn’t).
- "We" voice for Upstory.
- Run **`QA.md`** before ship, including AI phrasing and quantified-outcome checks.

## Process

For each company:

1. **Validate input** — five trust types only; all fields substantive; stop if not.
2. **Read `FORMAT.md`** — confirm six-block arc before writing.
3. **Derive slug** from Company Name.
4. **Logo** — extract from company site; cache `shared/logos/<slug>.*` + `*.meta.json` per `LOGO-TONE.md`; stop if blocked.
5. **Choose outcome metric** from Outreach Insight + Hiring Focus; pick headline quant (defensible range).
6. **Write outcome headline** — partnership voice, number in sentence.
7. **Write main insight** — unique to client; `Our read`; opportunity framing; max 3 sentences; bridge to opportunities.
8. **Write three opportunities** — titles + ≤2 sentences each; attach artifacts only where they add clarity (see `FORMAT.md`).
9. **Write ways to measure** — default lead + 3 bullets tied to headline metric.
10. **Assemble** from `scaffold.tsx` (closer/footer locked).
11. **Run `QA.md`** — fix failures.
12. **Copy `shared/`** into host `public/shared/` when deploying a new project (skip if present).
13. **Save** to `app/<slug>/page.tsx`.
14. **Print validation summary.**

## Validation summary format

```
Generated <Company Name> page (app/<slug>/page.tsx).
Arc: header → headline → insight → opportunities (artifacts: <journey|funnel|chips|none per block>) → measure → pitch.
Trust Type: <type>. Outcome metric: <name>. Headline quant: <number/range>.
QA: <passed | N items failed — list>.
Logo: <path>. Word count: ~<n>.
```

If judgment calls:

```
Judgment call: <one short sentence>.
```

## Reference

- `FORMAT.md` — locked format contract
- `QA.md` — pre-ship quality checklist
- `LOGO-TONE.md` — header band vs plate
- `scaffold.tsx` — `{{placeholders}}` for generation
- `examples/stake.tsx` — reference brief (Stake / Money / UMoveFree)
