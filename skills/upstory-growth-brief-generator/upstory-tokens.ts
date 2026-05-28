/**
 * Upstory growth brief — semi-custom 1-pager language.
 * Warm off-white canvas, Manrope for structure, Source Serif 4 for prose.
 */
export const UPOSTORY_BRIEF_TOKENS = {
  ink: '#151D1F',
  ink2: '#4a5254',
  ink3: '#8a8f90',
  bg: '#fcfcfa',
  surface: '#f5f5f1',
  surfaceRaised: '#ffffff',
  rule: '#ececea',
  accent: '#111111',
  bronze: '#876333',
} as const;

export const UPOSTORY_BRIEF_FONTS = {
  sans: '"Manrope", system-ui, sans-serif',
  serif: '"Source Serif 4", Georgia, serif',
} as const;

export const UPOSTORY_BRIEF_FONT_URL =
  'https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&display=swap';

export const upstoryBriefStyle = {
  '--upstory-ink': UPOSTORY_BRIEF_TOKENS.ink,
  '--upstory-ink-2': UPOSTORY_BRIEF_TOKENS.ink2,
  '--upstory-ink-3': UPOSTORY_BRIEF_TOKENS.ink3,
  '--upstory-bg': UPOSTORY_BRIEF_TOKENS.bg,
  '--upstory-surface': UPOSTORY_BRIEF_TOKENS.surface,
  '--upstory-surface-raised': UPOSTORY_BRIEF_TOKENS.surfaceRaised,
  '--upstory-rule': UPOSTORY_BRIEF_TOKENS.rule,
  '--upstory-accent': UPOSTORY_BRIEF_TOKENS.accent,
  '--upstory-bronze': UPOSTORY_BRIEF_TOKENS.bronze,
  '--font-sans': UPOSTORY_BRIEF_FONTS.sans,
  '--font-serif': UPOSTORY_BRIEF_FONTS.serif,
} as const;
