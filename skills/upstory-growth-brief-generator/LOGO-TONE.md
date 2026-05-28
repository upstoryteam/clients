# Client logo tone (how the header adapts)

## Rule

**Never edit, invert, or recolor the client logo file.** Only change the **container** behind it.

## What varies

The cached SVG/PNG from their site is either:

| `clientLogoTone` | Logo artwork | Container |
|------------------|--------------|-----------|
| `light` | White or very light marks (Stake) | Dark background behind **client mark only** (`plate`) or full **header band** |
| `dark` | Dark ink on transparent (most SaaS) | White/light plate on cream page |

Set tone when you cache the logo (see `shared/logos/<slug>.meta.json`). If wrong, open the asset in a browser on white: invisible → `light`, readable → `dark`.

## Not full-page dark mode

The brief body stays **cream** (`#fcfcfa`) for readability. Only the **header zone** adapts. That keeps one Upstory 1-pager system; the variable is logo contrast, not theme toggling.

## Header variants

### `plate` (default)

- Upstory mark on cream.
- Serif “for”.
- Client logo in a small **dark or light plate** (opposite of logo tone).

Use when you want a minimal header or when only the client mark needs help.

### `band` (recommended for `light` logos)

- Full-width **dark header band** (`#151D1F`, Upstory chrome).
- Upstory mark shown in **on-dark** treatment (separate asset or filter on **Upstory-owned** file only).
- “for” in muted light text.
- Client logo **directly on the band** (no extra pill).

Use for white/light client marks so the header feels intentional, not a floating black box.

## Per-brief metadata

```json
// shared/logos/stake.meta.json
{
  "tone": "light",
  "headerVariant": "band",
  "source": "https://stakerent.com/..."
}
```

In generated pages:

```tsx
<BriefHeader
  clientSrc="/shared/logos/stake.svg"
  clientAlt="Stake"
  clientLogoTone="light"
  headerVariant="band"
/>
```

## Skill workflow

1. Download logo from client site (unchanged).
2. Save to `shared/logos/<slug>.svg`.
3. Write `shared/logos/<slug>.meta.json` with `tone` (+ optional `headerVariant`).
4. Pass `clientLogoTone` and `headerVariant` into `BriefHeader`.

Do not guess `stake.com` domains. Do not use Clearbit unless verified.
