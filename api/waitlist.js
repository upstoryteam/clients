const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const WORKSHOP_DATE = 'July 14, 2026';
const WORKSHOP_TITLE = 'How to become an AI-native product designer';

function normalizeText(value) {
  if (typeof value !== 'string') return '';
  return value.trim();
}

function firstName(name) {
  return name.split(/\s+/)[0] || name;
}

async function sendConfirmationEmail({ name, workEmail }) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) return { skipped: true };

  const from = process.env.WAITLIST_FROM_EMAIL || 'Upstory <workshop@upstory.co>';
  const replyTo = process.env.WAITLIST_REPLY_TO_EMAIL || 'rick@upstory.co';
  const greeting = firstName(name);

  const html = `
    <div style="font-family: Manrope, Arial, sans-serif; color: #151d1f; line-height: 1.6; max-width: 520px;">
      <p style="margin: 0 0 16px;">Hi ${greeting},</p>
      <p style="margin: 0 0 16px;">You're registered for <strong>${WORKSHOP_TITLE}</strong>.</p>
      <p style="margin: 0 0 16px;">The live workshop is on <strong>${WORKSHOP_DATE}</strong>. We'll email joining details before the session.</p>
      <p style="margin: 0 0 24px;">See you there,<br>Rick Russie<br>Upstory</p>
      <p style="margin: 0; font-size: 13px; color: #8a8f90;">Questions? Just reply to this email.</p>
    </div>
  `.trim();

  const text = [
    `Hi ${greeting},`,
    '',
    `You're registered for ${WORKSHOP_TITLE}.`,
    '',
    `The live workshop is on ${WORKSHOP_DATE}. We'll email joining details before the session.`,
    '',
    'See you there,',
    'Rick Russie',
    'Upstory',
    '',
    'Questions? Just reply to this email.',
  ].join('\n');

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [workEmail],
      reply_to: replyTo,
      subject: `You're registered — AI workshop on ${WORKSHOP_DATE}`,
      html,
      text,
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Resend ${response.status}: ${body}`);
  }

  return { sent: true };
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
    try {
      await sendConfirmationEmail({ name, workEmail });
    } catch (error) {
      console.error('Confirmation email failed:', error.message);
    }

    return res.status(201).json({ ok: true });
  }

  if (insertResponse.status === 409) {
    return res.status(200).json({
      ok: true,
      alreadyRegistered: true,
      message: "You're already registered. We'll send joining details before July 14.",
    });
  }

  const errorBody = await insertResponse.text();
  console.error('Supabase insert failed:', insertResponse.status, errorBody);
  return res.status(502).json({ error: 'Could not save your signup. Please try again.' });
}
