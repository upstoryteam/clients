const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function normalizeText(value) {
  if (typeof value !== 'string') return '';
  return value.trim();
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !supabaseServiceRoleKey) {
    console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
    return res.status(503).json({ error: 'Waitlist is not configured yet.' });
  }

  const payload = req.body || {};
  const name = normalizeText(payload.name);
  const workEmail = normalizeText(payload.work_email).toLowerCase();
  const title = normalizeText(payload.title) || null;
  const workshop = normalizeText(payload.workshop) || 'ai-product-design-101';

  if (!name) {
    return res.status(400).json({ error: 'Name is required.' });
  }

  if (!workEmail || !EMAIL_PATTERN.test(workEmail)) {
    return res.status(400).json({ error: 'A valid work email is required.' });
  }

  const insertResponse = await fetch(`${supabaseUrl}/rest/v1/workshop_waitlist`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      apikey: supabaseServiceRoleKey,
      Authorization: `Bearer ${supabaseServiceRoleKey}`,
      Prefer: 'return=minimal',
    },
    body: JSON.stringify({
      name,
      work_email: workEmail,
      title,
      workshop,
    }),
  });

  if (insertResponse.ok) {
    return res.status(201).json({ ok: true });
  }

  if (insertResponse.status === 409) {
    return res.status(200).json({
      ok: true,
      alreadyRegistered: true,
      message: "You're already on the list. We'll email when a date is set.",
    });
  }

  const errorBody = await insertResponse.text();
  console.error('Supabase insert failed:', insertResponse.status, errorBody);
  return res.status(502).json({ error: 'Could not save your signup. Please try again.' });
}
