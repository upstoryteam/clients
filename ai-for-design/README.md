# AI for Design

Landing page for the **AI Product Design 101** workshop, served at `clients.upstory.co/ai-for-design`.

Duplicated from the `upstory-workshop` project (https://github.com/stephdiedrich/upstory-workshop / https://upstory-workshop.vercel.app/).

## Files

- `index.html` — the page.
- `styles.css` — page styles (self-contained; fonts and a few images load from remote CDNs).
- `assets/` — local images (`rick-russie.png`, `cursor-logo.png`).

## Notes

- Asset references use absolute `/ai-for-design/...` paths so they resolve correctly under `vercel.json` `trailingSlash: false` (the URL has no trailing slash).
- Waitlist forms POST to Formspree. Replace `YOUR_FORM_ID` in `index.html` with the real form ID before sending traffic.
