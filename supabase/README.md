# Supabase — workshop waitlist

## Quick setup

```bash
export SUPABASE_ACCESS_TOKEN="sbp_..."   # https://supabase.com/dashboard/account/tokens
# optional if you already have a project:
# export SUPABASE_PROJECT_REF="your-project-ref"
./scripts/setup-workshop-waitlist-supabase.sh
```

The script creates or reuses an `upstory-clients` project, applies the migration, and prints the Vercel env vars to add.

## Migration

Apply `migrations/20250625120000_workshop_waitlist.sql` to create the `workshop_waitlist` table.

Using the Supabase CLI (linked project):

```bash
supabase db push
```

Or paste the migration SQL into Supabase → SQL Editor → Run.

## Vercel environment variables

Add these in Vercel → Project → Settings → Environment Variables:

| Variable | Where to find it |
|----------|------------------|
| `SUPABASE_URL` | Supabase → Settings → API → Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Settings → API → service_role key |

The service role key is used only by `/api/waitlist` on the server. Do not expose it in client-side code.

Redeploy after adding env vars.

## Schema

```sql
workshop_waitlist (
  id uuid,
  name text not null,
  work_email text not null,
  title text,        -- legacy; kept for existing rows
  company text,      -- captured from the signup form
  workshop text not null,
  created_at timestamptz
)
```

Unique on `(work_email, workshop)` so duplicate signups get a friendly response.
