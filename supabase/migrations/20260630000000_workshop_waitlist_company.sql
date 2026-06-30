-- Capture company name instead of job title on workshop signups.
-- Adds a nullable `company` column; the legacy `title` column is kept so
-- existing rows are preserved (new signups only populate `company`).
alter table public.workshop_waitlist
  add column if not exists company text;
