#!/usr/bin/env bash
# Provision Supabase storage for the AI Product Design 101 waitlist.
#
# Usage:
#   export SUPABASE_ACCESS_TOKEN="sbp_..."
#   export SUPABASE_PROJECT_REF="your-project-ref"   # optional; creates "upstory-clients" if unset
#   ./scripts/setup-workshop-waitlist-supabase.sh
#
# After running, add the printed env vars to Vercel and redeploy.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${SUPABASE_ACCESS_TOKEN:-}" ]]; then
  echo "Missing SUPABASE_ACCESS_TOKEN."
  echo "Create one at https://supabase.com/dashboard/account/tokens"
  exit 1
fi

echo "Logging in to Supabase CLI..."
npx supabase login --token "$SUPABASE_ACCESS_TOKEN" --name "upstory-clients-setup"

PROJECT_REF="${SUPABASE_PROJECT_REF:-}"

if [[ -z "$PROJECT_REF" ]]; then
  echo "No SUPABASE_PROJECT_REF set. Looking for an existing 'upstory-clients' project..."
  PROJECT_REF="$(npx supabase projects list --output json | node -e "
    const rows = JSON.parse(require('fs').readFileSync(0, 'utf8'));
    const match = rows.find((p) => p.name === 'upstory-clients');
    if (match) process.stdout.write(match.id);
  " || true)"

  if [[ -z "$PROJECT_REF" ]]; then
    ORG_ID="$(npx supabase orgs list --output json | node -e "
      const rows = JSON.parse(require('fs').readFileSync(0, 'utf8'));
      if (!rows.length) process.exit(1);
      process.stdout.write(rows[0].id);
    ")"

    DB_PASS="$(openssl rand -base64 24 | tr -dc 'A-Za-z0-9' | head -c 24)"
    echo "Creating Supabase project 'upstory-clients'..."
    CREATE_JSON="$(npx supabase projects create upstory-clients \
      --org-id "$ORG_ID" \
      --db-password "$DB_PASS" \
      --region us-east-1 \
      --output json)"
    PROJECT_REF="$(node -e "process.stdout.write(JSON.parse(process.argv[1]).id)" "$CREATE_JSON")"
    echo "Created project: $PROJECT_REF"
    echo "Waiting for project to become active..."
    for _ in $(seq 1 60); do
      STATUS="$(npx supabase projects list --output json | node -e "
        const rows = JSON.parse(require('fs').readFileSync(0, 'utf8'));
        const row = rows.find((p) => p.id === process.argv[1]);
        if (row) process.stdout.write(row.status || '');
      " "$PROJECT_REF")"
      [[ "$STATUS" == "ACTIVE_HEALTHY" ]] && break
      sleep 10
    done
  fi
fi

echo "Linking project $PROJECT_REF..."
npx supabase link --project-ref "$PROJECT_REF" --yes

# Persist project ref for future db push runs.
if grep -q '^project_id = ""' supabase/config.toml; then
  sed -i "s/^project_id = \"\"/project_id = \"$PROJECT_REF\"/" supabase/config.toml
fi

echo "Applying waitlist migration..."
npx supabase db push --linked --yes

echo "Fetching API keys..."
KEYS_JSON="$(npx supabase projects api-keys --project-ref "$PROJECT_REF" --reveal --output json)"
SUPABASE_URL="https://${PROJECT_REF}.supabase.co"
SERVICE_ROLE_KEY="$(node -e "
  const rows = JSON.parse(process.argv[1]);
  const row = rows.find((k) => k.type === 'secret') || rows.find((k) => k.name === 'service_role');
  if (!row) process.exit(1);
  process.stdout.write(row.api_key);
" "$KEYS_JSON")"

cat <<EOF

Done. Add these to Vercel (Project → Settings → Environment Variables):

SUPABASE_URL=$SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY

Then redeploy the clients project.

Verify signups:
  select name, work_email, title, created_at
  from workshop_waitlist
  order by created_at desc;
EOF
