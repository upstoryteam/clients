# Shared audit assets

Used by growth brief pages and available site-wide on Vercel at `/shared/<filename>`.

| File | Purpose |
|---|---|
| `favicon-light.svg` / `favicon-dark.svg` | Upstory lightning bolt favicons (from [upstory.co](https://upstory.co); light/dark by `prefers-color-scheme`) |
| `brief.css` | Growth brief layout + Upstory design tokens (Manrope, Source Serif 4) |
| `brief-impact-calc.js` | Optional interactive impact calculators on static briefs |
| `upstory-logo.png` | Upstory mark in the brief closer (matches Citizen Health audit) |
| `rick-russie.avif` | Rick Russie headshot in the closer signature block |
| `logos/<slug>.svg` | Per-company logos cached from their marketing site (unchanged artwork) |
| `logos/<slug>.meta.json` | `tone` (`light` \| `dark`) and `headerVariant` (`plate` \| `band`) for header contrast |

When generating Next.js briefs, copy this folder to `public/shared/` in the host project.
