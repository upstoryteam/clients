# AI for Design

Landing page for the **AI Product Design 101** workshop, served at `clients.upstory.co/ai-for-design`.

Duplicated from the `upstory-workshop` project (https://github.com/stephdiedrich/upstory-workshop / https://upstory-workshop.vercel.app/).

## Files

- `index.html` — the page.
- `styles.css` — page styles (self-contained; fonts and a few images load from remote CDNs).
- `assets/` — local images (`rick-russie.png`, `cursor-logo.png`).

## Waitlist storage

Signups are saved to Supabase via the Vercel serverless route at `/api/waitlist`.

Each signup stores:

| Field | Required |
|-------|----------|
| `name` | Yes |
| `work_email` | Yes |
| `title` | No |
| `workshop` | Hidden (defaults to `ai-product-design-101`) |

### Setup

1. **Create the table** — run the migration in your Supabase project:
   ```bash
   supabase db push
   ```
   Or paste `supabase/migrations/20250625120000_workshop_waitlist.sql` into the Supabase SQL editor.

2. **Add Vercel env vars** (see repo root `.env.example`):
   - `SUPABASE_URL` — project URL from Supabase → Settings → API
   - `SUPABASE_SERVICE_ROLE_KEY` — service role key (server-side only; never expose in the browser)

3. **Redeploy** so the `/api/waitlist` function picks up the env vars.

### Confirmation emails (optional)

After a new signup, `/api/waitlist` sends:
- a confirmation email to the registrant
- a notification email to `sales@upstory.co`, `nash@upstory.co`, and `sd@upstory.co` (or `WAITLIST_NOTIFY_EMAIL` plus those two)

1. Create a Resend account and verify your sending domain (e.g. `upstory.co`).
2. Add Vercel env vars:
   - `RESEND_API_KEY` — from Resend → API Keys
   - `WAITLIST_FROM_EMAIL` — optional, e.g. `Upstory <workshop@upstory.co>` (must use a verified domain)
   - `WAITLIST_REPLY_TO_EMAIL` — optional, defaults to `rick@upstory.co`
   - `WAITLIST_NOTIFY_EMAIL` — optional, defaults to `sales@upstory.co`
3. Redeploy.

If `RESEND_API_KEY` is not set, signups still save — email is skipped.

### Viewing signups

In Supabase → Table Editor → `workshop_waitlist`, or:

```sql
select name, work_email, title, created_at
from workshop_waitlist
where workshop = 'ai-product-design-101'
order by created_at desc;
```

Duplicate emails for the same workshop return a friendly “already on the list” message instead of an error.

## Notes

- Asset references use absolute `/ai-for-design/...` paths so they resolve correctly under `vercel.json` `trailingSlash: false` (the URL has no trailing slash).
