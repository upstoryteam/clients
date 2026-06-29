import { createHash } from 'node:crypto';

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const WORKSHOP_DATE = 'July 14, 2026 · 1p CDT';
const WORKSHOP_TITLE = 'How to become an AI-native product designer';
const META_PIXEL_ID = process.env.META_PIXEL_ID || '1099381639935282';
const META_GRAPH_VERSION = process.env.META_GRAPH_VERSION || 'v19.0';

function normalizeText(value) {
  if (typeof value !== 'string') return '';
  return value.trim();
}

function firstName(name) {
  return name.split(/\s+/)[0] || name;
}

function getResendConfig() {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) return null;

  return {
    apiKey,
    from: process.env.WAITLIST_FROM_EMAIL || 'Upstory <workshop@upstory.co>',
  };
}

async function sendResendEmail({ apiKey, from, to, replyTo, subject, html, text }) {
  const payload = { from, to, subject, html, text };
  if (replyTo) payload.reply_to = replyTo;

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Resend ${response.status}: ${body}`);
  }

  return { sent: true };
}

async function sendConfirmationEmail({ name, workEmail }) {
  const config = getResendConfig();
  if (!config) return { skipped: true };

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

  return sendResendEmail({
    apiKey: config.apiKey,
    from: config.from,
    to: [workEmail],
    replyTo,
    subject: `You're registered — AI workshop on ${WORKSHOP_DATE}`,
    html,
    text,
  });
}

function getTeamNotifyEmails() {
  const base = process.env.WAITLIST_NOTIFY_EMAIL || 'sales@upstory.co';
  const emails = base.split(',').map((email) => email.trim()).filter(Boolean);
  const alwaysInclude = ['nash@upstory.co', 'steph@upstory.co'];
  return [...new Set([...emails, ...alwaysInclude])];
}

async function sendTeamNotificationEmail({ name, workEmail, title, workshop }) {
  const config = getResendConfig();
  if (!config) return { skipped: true };

  const notifyEmails = getTeamNotifyEmails();
  const titleLine = title || '—';

  const html = `
    <div style="font-family: Manrope, Arial, sans-serif; color: #151d1f; line-height: 1.6; max-width: 520px;">
      <p style="margin: 0 0 16px;">New workshop signup for <strong>${WORKSHOP_TITLE}</strong>.</p>
      <ul style="margin: 0; padding-left: 20px;">
        <li><strong>Name:</strong> ${name}</li>
        <li><strong>Email:</strong> ${workEmail}</li>
        <li><strong>Title:</strong> ${titleLine}</li>
        <li><strong>Workshop:</strong> ${workshop}</li>
      </ul>
    </div>
  `.trim();

  const text = [
    `New workshop signup for ${WORKSHOP_TITLE}.`,
    '',
    `Name: ${name}`,
    `Email: ${workEmail}`,
    `Title: ${titleLine}`,
    `Workshop: ${workshop}`,
  ].join('\n');

  return sendResendEmail({
    apiKey: config.apiKey,
    from: config.from,
    to: notifyEmails,
    replyTo: workEmail,
    subject: `New workshop signup: ${name}`,
    html,
    text,
  });
}

async function handleSignupEmails(signup) {
  const results = await Promise.allSettled([
    sendConfirmationEmail(signup),
    sendTeamNotificationEmail(signup),
  ]);

  results.forEach((result, index) => {
    if (result.status === 'rejected') {
      const label = index === 0 ? 'Confirmation email' : 'Team notification';
      console.error(`${label} failed:`, result.reason.message);
    }
  });
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function getClientIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (typeof forwarded === 'string' && forwarded.length) {
    return forwarded.split(',')[0].trim();
  }
  return req.socket?.remoteAddress || undefined;
}

function parseCookies(req) {
  const header = req.headers.cookie;
  const cookies = {};
  if (typeof header !== 'string') return cookies;

  header.split(';').forEach((part) => {
    const index = part.indexOf('=');
    if (index === -1) return;
    const key = part.slice(0, index).trim();
    if (!key) return;
    cookies[key] = decodeURIComponent(part.slice(index + 1).trim());
  });

  return cookies;
}

// Server-side Conversions API event. Mirrors the browser pixel's
// CompleteRegistration so registrations are still counted when the browser
// pixel is blocked by ad blockers / tracking protection. Shares the event_id
// with the browser event so Meta can deduplicate when both arrive.
async function sendMetaConversion({ req, name, workEmail, eventId }) {
  const accessToken = process.env.META_CAPI_ACCESS_TOKEN;
  if (!accessToken) return { skipped: true };

  const cookies = parseCookies(req);
  const userData = {
    em: [sha256(workEmail)],
  };

  const givenName = firstName(name).toLowerCase();
  if (givenName) userData.fn = [sha256(givenName)];

  const clientIp = getClientIp(req);
  if (clientIp) userData.client_ip_address = clientIp;

  const userAgent = req.headers['user-agent'];
  if (userAgent) userData.client_user_agent = userAgent;

  if (cookies._fbp) userData.fbp = cookies._fbp;
  if (cookies._fbc) userData.fbc = cookies._fbc;

  const event = {
    event_name: 'CompleteRegistration',
    event_time: Math.floor(Date.now() / 1000),
    action_source: 'website',
    user_data: userData,
    custom_data: {
      content_name: 'ai-product-design-101',
      status: true,
    },
  };

  if (eventId) event.event_id = eventId;
  const eventSourceUrl = req.headers.referer || req.headers.origin;
  if (eventSourceUrl) event.event_source_url = eventSourceUrl;

  const body = { data: [event] };
  if (process.env.META_TEST_EVENT_CODE) {
    body.test_event_code = process.env.META_TEST_EVENT_CODE;
  }

  const response = await fetch(
    `https://graph.facebook.com/${META_GRAPH_VERSION}/${META_PIXEL_ID}/events?access_token=${encodeURIComponent(accessToken)}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }
  );

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Meta CAPI ${response.status}: ${errorBody}`);
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
  const eventId = normalizeText(payload.event_id) || null;

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
    const [, conversionResult] = await Promise.allSettled([
      handleSignupEmails({ name, workEmail, title, workshop }),
      sendMetaConversion({ req, name, workEmail, eventId }),
    ]);

    if (conversionResult.status === 'rejected') {
      console.error('Meta Conversions API failed:', conversionResult.reason.message);
    }

    return res.status(201).json({ ok: true });
  }

  if (insertResponse.status === 409) {
    return res.status(200).json({
      ok: true,
      alreadyRegistered: true,
      message: "You're already registered. We'll send joining details before July 14 at 1p CDT.",
    });
  }

  const errorBody = await insertResponse.text();
  console.error('Supabase insert failed:', insertResponse.status, errorBody);
  return res.status(502).json({ error: 'Could not save your signup. Please try again.' });
}
