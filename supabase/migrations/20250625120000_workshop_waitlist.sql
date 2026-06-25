-- Workshop waitlist signups (AI Product Design 101 and future workshops)
create table if not exists public.workshop_waitlist (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(trim(name)) > 0),
  work_email text not null check (work_email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  title text,
  workshop text not null default 'ai-product-design-101',
  created_at timestamptz not null default now(),
  constraint workshop_waitlist_email_workshop_unique unique (work_email, workshop)
);

create index if not exists workshop_waitlist_workshop_created_at_idx
  on public.workshop_waitlist (workshop, created_at desc);

alter table public.workshop_waitlist enable row level security;

-- No public read/update/delete; inserts go through the serverless API using the service role key.

comment on table public.workshop_waitlist is 'Workshop waitlist signups from clients.upstory.co/ai-for-design';
