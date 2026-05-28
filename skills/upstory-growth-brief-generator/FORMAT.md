# Growth brief format (locked)

One page. Six blocks in a fixed order. **Do not add sections.** Reference implementation: `stake/index.html`, `examples/stake.tsx`.

## The arc (always this order)

| # | Block | Component / markup | Client-specific? |
|---|--------|-------------------|------------------|
| 1 | **Co-branded header** | `BriefHeader` | Logo + tone metadata per company |
| 2 | **Outcome headline** | `OutcomeHeadline` | Yes — metric + quantified claim |
| 3 | **Insight** | `MainInsight` (`Our read` + lightbulb) | Yes — unique per client |
| 4 | **Opportunities** | `OpportunitiesIntro` + `SolutionBlock` × 3 | Yes — titles, prose, artifacts |
| 5 | **Ways to measure success** | `WaysToMeasure` | Yes — three bullets tied to headline metric |
| 6 | **Pitch** | `UpstoryCloser` + `BriefFooter` | Locked copy (do not paraphrase) |

Nothing else: no second hero, no “why this fits” essay, no numbered measurement cards, no fifth recommendation section.

---

## 1. Co-branded header

**`[Upstory logo] for [Client logo]`**

- Set `clientLogoTone` + `headerVariant` per `LOGO-TONE.md` and `shared/logos/<slug>.meta.json`.
- Never edit client logo files.
- Page `<title>`: `Upstory for {Company Name}` (not `For {First Name} at …`).

---

## 2. Outcome headline

- **Font:** Manrope, one line when possible.
- **Voice:** partnership, not lecture. Lead with **we can help**, not “here is what your company must do.”
- **Outcome (required):** name a **measurable result** you are offering to move (conversion, first payment, activation, completion, show-up rate, etc.).
- **Quant (required):** include a number or defensible range on that same outcome (same metric family as **Ways to measure success**).
- **Examples:** `We believe we can help {CasualizedName} lift first rent payment conversion on the UMoveFree cohort by about 10%.`
- **Avoid:** inflection-point rhetoric, unmeasured “improve onboarding,” strategy essays, contrast pivots (`not X, but Y`).

---

## 3. Insight (`Our read`)

Warm card under the headline (bronze top gradient, lightbulb + eyebrow on one row, body below).

- **Eyebrow (locked):** `Our read` only.
- **Body:** Source Serif 4, **max 3 sentences**, full width of the card.
- **Structure:** (1) what you see in their situation — use **opportunity / value** framing, not “real opening” filler; (2) **In the product…** — where leverage lives; (3) bridge — **The opportunities below…**
- **Tone:** observant peer, not auditor. “Your {news} is an opportunity to create value…” / “We would focus on…”

---

## 4. Opportunities

**Section break:** `border-top`, H2 **Opportunities**, serif lead (default: *Three places we would start in the product.*).

Each block:

| Element | Rules |
|---------|--------|
| **Index** | `01` `02` `03` beside title — never the word “Solution” |
| **Title** | Manrope, product-specific |
| **Body** | Serif, **≤ 2 sentences**, full width of the 700px column (no `ch` caps, no extra left indent) |
| **Artifact** | Optional — see below |
| **Spacing** | `48px` vertical padding between blocks (after the first) |

### Artifacts (visuals)

Artifacts sit **inside** the opportunity they support. They should **earn their space** — clarify a moment, path, or metric; not decorate.

| Variant | When to use | Layout |
|---------|-------------|--------|
| `journey` | 3-step path to the outcome moment; emphasize the key step | Inline, dashed top rule; steps span full width |
| `funnel` | Stage drop-off or conversion; directional % | Card box; bars span full width; label **Illustrative** if not real data |
| `chips` | 2–3 tight metric tags (north-star, cohort, win) | Inline; chips share row width equally |
| *(none)* | Prose is enough | Valid for any block — do not force a visual |

**Distribution:** Prefer **one** strong artifact on the page (often `funnel` on `02`). Inline `journey` or `chips` on other blocks is fine. All three blocks do **not** need a visual.

**Width:** `.visual`, journey, funnel, and chips use **100%** of the opportunity column.

---

## 5. Ways to measure success

Same section pattern as Opportunities: `border-top`, H2 **Ways to measure success**, serif lead (default: *A few ideas for leading indicators we could track with you.*).

- **Three bullets** only — bronze dot, serif, full width.
- **No** `01`–`03`, no card box.
- Bullets must reference the **same primary metric** as the headline (north-star, cohort/isolation, readout/threshold).

---

## 6. Pitch (Upstory closer)

Locked layout at the bottom; all client value sits above.

1. Top border, generous spacing.
2. Upstory logo (`/shared/upstory-logo.png`).
3. **Firm pitch (locked):**

   > **Upstory is a product design firm.** We specialize in growth and retention for consumer products that ask for sensitive information. Our focus is in health, fintech, and identity, with client work featuring LifeMD, Firefox, and Wander.

4. Rick block: `/shared/rick-russie.avif`, `Rick Russie`, `Founder and Design Lead, Upstory`.
5. **Tagline footer (locked):** `We design the moments where consumer products earn users.` / `© Upstory 2026`

No calendar CTA, no “happy to chat” / “if helpful.”

---

## Design system (not client brand)

- Background `#fcfcfa`, ink `#151D1F`, bronze `#876333`
- **Manrope** (UI, headlines) + **Source Serif 4** (insight, opportunity body, measure bullets, closer)
- Page column: **700px** max, horizontal padding **28px**
- Static CSS: `shared/brief.css`. React: `brief-ui.tsx` + `upstory-tokens.ts`

---

## Prose limits (hard)

| Field | Limit |
|-------|--------|
| Main insight | ≤ 3 sentences, ≤ 75 words |
| Each opportunity body | ≤ 2 sentences, ≤ 50 words |
| Each measure bullet | 1 sentence, ≤ 20 words |
| Headline | 1 sentence |

---

## Deployment (repo layout)

Each brief is **`/<slug>/index.html`** in this repo, not a standalone deployable folder. It depends on **`/shared/`** at the site root (`brief.css`, Upstory logo, Rick avatar, `logos/<slug>.*`). Briefs do not link to each other. See repo root **`DEPLOY.md`** for client handoff.

## Before ship: quality review

Run `QA.md` against the draft. The format can be correct and the copy still fail QA (condescending tone, AI phrasing, filler artifacts). **Format lock ≠ ship without review.**

---

## Not a skill failure, not bad CSV

Older templates stacked **five essays** and a **duplicate hero**. Your row is fine if the agent follows **this** file.
