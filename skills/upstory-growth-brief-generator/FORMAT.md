# Growth brief format (locked)

One page. Six blocks in a fixed order. **Do not add sections.** Reference implementation: `stake/index.html`, `examples/stake.tsx`.

## The arc (always this order)

| # | Block | Component / markup | Client-specific? |
|---|--------|-------------------|------------------|
| 1 | **Co-branded header** | `BriefHeader` | Logo + tone metadata per company |
| 2 | **Outcome headline** | `OutcomeHeadline` | Yes — metric + quantified claim |
| 3 | **Insight** | `MainInsight` (`What we see` + lightbulb) | Yes — unique per client |
| 4 | **Opportunities to explore** | `OpportunitiesIntro` + `SolutionBlock` × 3 | Yes — titles, prose, artifacts |
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
- **Voice:** partnership, not lecture. Lead with **We believe we can help {CasualizedName}…**
- **Outcome (required):** one **measurable result** (same metric family as **Ways to measure success**).
- **Quant (required):** a specific number, rate, count, or ratio. Write it like a target you would put in a brief to a CEO, not a hedge.

**Pick the quant shape that fits the row** (do not default to “lift by X%”):

| Shape | Example |
|-------|---------|
| **Rate** | `…move 40% of UMoveFree renters to first rent payment.` |
| **Increment per 100** | `…get 8 more first rent payments per 100 UMoveFree signups.` |
| **Absolute count** | `…add 90 five-star App Store ratings.` |
| **Ratio** | `…turn 1 in 4 homepage visitors into an account.` |
| **Time-to-outcome (metric itself)** | `…cut median days-to-certification to 45 in each new state.` |

**Hard avoids:** `about`, `~`, **deadline windows in the headline** (`within 30 days`, `in the next 90 days`, `by Q3`), `lift … by X%` as a lazy template, inflection-point rhetoric, unmeasured “improve onboarding,” strategy essays. Leading indicators in **Ways to measure** may still use time windows.

---

## 3. Insight (`What we see`)

Warm card under the headline. This is what you would **say to them on a call**, not an internal research recap or memo to Upstory.

- **Eyebrow (locked):** `What we see` only.
- **Body:** Source Serif 4, **max 3 sentences**, full width of the card.
- **Audience:** write to **them** (`you` / `your` where natural). Plain language. They should feel you looked at the product and are handing them the insight, not reporting on a dossier.
- **Do not:** restate their funding, launch, or press back to them; open with “{News} is an opportunity to create value”; use internal phrasing (`our read`, `we would focus`, `from the outside`, `the opportunity is`); sound like a brief **to** your team.
- **Do:** one sharp observation from the product or funnel; where the wedge is in the UI or journey; optional short bridge to the opportunities section (`Here's where we'd start in the product.` or similar).

**Fail:** `The Series A and mobile launch are an opportunity to create value: families arrive with urgent questions.`

**Pass:** `When someone hits your homepage, they are already leaning in. The signup screen still asks for email before the Advocate runs. That gap is what we would close first.`

---

## 4. Opportunities to explore

**Section break:** `border-top`, H2 **Opportunities to explore**, serif lead (default: *Three places we'd start in the product.*).

Each block:

| Element | Rules |
|---------|--------|
| **Index** | `01` `02` `03` beside title — never the word “Solution” |
| **Title** | Manrope, product-specific (hypothesis, not a committed roadmap) |
| **Body** | Serif, **≤ 2 sentences**, exploratory voice: **We'd start by…**, **worth testing…**, not prescriptive **We will** / **You should** |
| **Artifact** | Optional — see below |
| **Spacing** | `48px` vertical padding between blocks (after the first) |

### Artifacts (visuals)

**Nothing is better than something wrong.** Write the opportunity title and body first, then decide if a visual earns its place. If it does not pass the relevance test below, omit it.

#### How to choose (per block)

1. Finish the prose. One sentence: *what change are we proposing?*
2. Ask: *If we sketched this on a whiteboard, would it be a path, a narrowing funnel, or a set of labels?*
3. Pick **one** form that matches, or **none**.

| If the opportunity is about… | Use | Do not use |
|------------------------------|-----|------------|
| **Reordering or inserting a step** in a flow (show value before ask, handoff, onboarding path) | `journey` | funnel, calculator |
| **Where people fall off** between named stages (signup → account → payment) | `funnel` | journey, calculator |
| **Sizing the prize** if we fix X (sliders + live outcome tied to headline metric) | `calculator` | funnel, journey |
| **Defining 2–3 concrete tags** for this block only (thresholds, cohort labels) | `chips` (rare) | journey, funnel, calculator |
| **Cohort rules, analytics hygiene, positioning, copy-only UX** | **none** | any chart that repeats the paragraph |

Typical page: **1–2 artifacts total**. Never assign `01` journey / `02` funnel / `03` chips by habit.

#### Relevance test (all must pass, or omit the artifact)

- [ ] Step or stage **labels are theirs** (product, partner, screen names), not `Step 1` / `Onboarding`.
- [ ] The **highlighted** journey step or funnel stage is the moment your title proposes to fix.
- [ ] Deleting the visual would remove a **relationship** (order or relative drop) that the prose does not already carry.
- [ ] You cannot swap this visual to another opportunity without changing labels and meaning.
- [ ] Funnel bars are **illustrative** unless you have real data; label **Illustrative. Where we'd look first.**

#### Reference pairings (this repo)

| Brief | Block | Artifact | Why it fits |
|-------|-------|----------|-------------|
| Stake | 01 Show payoff before deposit | `journey` | Sequence: partner → value → deposit ask |
| Stake | 02 First rent payment | `funnel` | Drop-off from signup to payment |
| Stake | 03 Cohort measurement | **none** | Analytics; measure section owns metrics |
| Citizen | 01 Demo before email | `journey` | Sequence: visit → demo → signup |
| Citizen | 02 App Store reviews | `calculator` | Interactive sizing of projected ratings (MAU × prompt × convert) |
| Citizen | 03 Cohort readout | **none** | Instrumentation, not a flow diagram |
| Abby | 01 One guided path | `journey` | Apply → training/forms → certified |
| Abby | 02 First paid shift | `funnel` | Application → approval → first shift |
| Abby | 03 Per-state rollup | **none** | Reporting structure, not visualized here |

**Width:** artifacts use **100%** of the opportunity column.

#### Impact calculator (`calculator`)

Use when the opportunity is about **how much upside** is on the table if the product change works. Recipient can drag sliders and see the outcome move.

- **Static HTML:** `shared/brief-impact-calc.js` + markup class `vis-impact-calc` with `data-formula` (see `citizen-health/brief/index.html`).
- **React:** `type: 'calculator'` on `SolutionBlock` → `brief-impact-calc.tsx` (client component).
- **Formulas (extend in both files):** `app_store_ratings_90d`, `umove_first_payment_lift`.
- **Rules:** 2–3 inputs max; defaults documented in helper text; baseline line uses their **current** public number (e.g. 9 ratings); never present outputs as their actual data.
- **Skip** if you do not have defensible inputs or the opportunity is not about volume/rate sizing.

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

Each brief is **`/<slug>/index.html`** in this repo, not a standalone deployable folder. It depends on **`/shared/`** at the site root (`brief.css`, `favicon-light.svg` / `favicon-dark.svg` [Upstory bolt, same as upstory.co], Upstory logo, Rick avatar, `logos/<slug>.*`). In `<head>`, after `<title>`:

```html
<link rel="icon" href="/shared/favicon-light.svg" type="image/svg+xml" media="(prefers-color-scheme: light)">
<link rel="icon" href="/shared/favicon-dark.svg" type="image/svg+xml" media="(prefers-color-scheme: dark)">
```

Briefs do not link to each other. See repo root **`DEPLOY.md`** for client handoff.

## Before ship: quality review

Run `QA.md` against the draft. The format can be correct and the copy still fail QA (condescending tone, AI phrasing, filler artifacts). **Format lock ≠ ship without review.**

---

## Not a skill failure, not bad CSV

Older templates stacked **five essays** and a **duplicate hero**. Your row is fine if the agent follows **this** file.
