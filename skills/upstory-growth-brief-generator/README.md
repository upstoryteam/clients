# upstory-growth-brief-generator

Turn one row of company research into one Upstory growth brief page.

## What this is

A short strategy memo at `clients.upstory.co/<company-slug>`, linked from a cold email. Goal: a 30-minute call with Rick. This skill writes the page, not the email or deploy.

## Locked format (six blocks)

Read **`FORMAT.md`** before generating.

1. **Co-branded header** — Upstory for client logo  
2. **Outcome headline** — quantified, “We believe we can help…”  
3. **Insight** — `What we see` (unique per client, plain language to them)  
4. **Opportunities to explore** — `01`–`03` + optional artifacts (`journey`, `funnel`, `chips`)  
5. **Ways to measure success** — three bullets  
6. **Pitch** — locked Upstory closer + footer  

Reference: `stake/index.html`, `examples/stake.tsx`.

## Quality review

Structure alone is not enough. Run **`QA.md`** before ship (tone, no AI jargon, artifacts that earn their space, no condescending copy).

## Skill contents

```
upstory-growth-brief-generator/
  SKILL.md           generation rules, trust hints, process
  FORMAT.md          locked layout contract
  QA.md              pre-ship checklist
  LOGO-TONE.md       header band vs plate
  upstory-tokens.ts  colors + fonts
  brief-ui.tsx       React components
  scaffold.tsx       template with {{placeholders}}
  examples/stake.tsx filled reference brief
```

Repo root: `shared/brief.css` mirrors the same layout for static previews.

## Required input

One CSV row:

- Company Name, CasualizedName, Trust Type (`Money` | `Identity` | `Health` | `Real-World Action` | `Reputation`)
- Recent News Summary, Outreach Insight, Hiring Focus Summary, Person Enrichment Summary, First Name

Empty or thin fields → stop. No logo from company site → stop and ask.

## Output

`app/<company-slug>/page.tsx` in the host Next.js project, plus cached logo under `shared/logos/<slug>.*` when generating in this repo.

## Install

```bash
ln -s ~/Desktop/upstory-audits/skills/upstory-growth-brief-generator \
      ~/.claude/skills/upstory-growth-brief-generator
```

## Invoke

> Use the upstory-growth-brief-generator skill. Here is the row: …

After generation, run **QA.md** on the draft.
