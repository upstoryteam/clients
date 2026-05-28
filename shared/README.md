# Shared audit assets

Used by growth brief pages and available site-wide on Vercel at `/shared/<filename>`.

| File | Purpose |
|---|---|
| `brief.css` | Growth brief layout + Upstory design tokens (Manrope, Inria Serif, logo plate) |
| `upstory-logo.png` | Upstory mark in the brief closer (matches Citizen Health audit) |
| `rick-russie.avif` | Rick Russie headshot in the closer signature block |
| `logos/<slug>.svg` | Per-company logos cached from their marketing site (unchanged artwork) |
| `logos/<slug>.meta.json` | `tone` (`light` \| `dark`) and `headerVariant` (`plate` \| `band`) for header contrast |

When generating Next.js briefs, copy this folder to `public/shared/` in the host project.
