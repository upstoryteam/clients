import type { CSSProperties, ReactNode } from 'react';
import { ImpactCalculator, type ImpactCalcFormula } from './brief-impact-calc';
import { FunnelVisual } from './FunnelVisual';
import { upstoryBriefStyle } from './upstory-tokens';

export const SHARED = '/shared';

const serif: CSSProperties = { fontFamily: 'var(--font-serif)' };

function LightbulbIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      width="26"
      height="26"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M9 18h6" />
      <path d="M10 22h4" />
      <path d="M12 2a7 7 0 0 1 7 7c0 2.5-1.5 4.5-3.5 5.5V17H8.5v-2.5C6.5 13.5 5 11.5 5 9a7 7 0 0 1 7-7z" />
    </svg>
  );
}

export function BriefShell({ children }: { children: ReactNode }) {
  return (
    <div
      className="min-h-screen bg-[var(--upstory-bg)] text-[var(--upstory-ink)] antialiased"
      style={{ ...upstoryBriefStyle, fontFamily: 'var(--font-sans)' } as CSSProperties}
    >
      {children}
    </div>
  );
}

export function BriefPage({ children }: { children: ReactNode }) {
  return <main className="mx-auto max-w-[700px] px-7 pb-10 pt-[52px]">{children}</main>;
}

export type ClientLogoTone = 'light' | 'dark';
export type HeaderVariant = 'plain' | 'plate' | 'band';

/**
 * Co-branded header. `clientLogoTone` describes the client artwork (not the page).
 * `plain` = logo on cream, no plate; `plate` = small plate behind client; `band` = full dark strip (light logos).
 */
export function BriefHeader({
  clientSrc,
  clientAlt,
  clientLogoTone = 'dark',
  headerVariant = 'plain',
}: {
  clientSrc: string;
  clientAlt: string;
  /** Light artwork (white mark) vs dark artwork on transparent */
  clientLogoTone?: ClientLogoTone;
  headerVariant?: HeaderVariant;
}) {
  const useBand = headerVariant === 'band' && clientLogoTone === 'light';
  const clientPlateClass = useBand
    ? ''
    : headerVariant === 'plate' && clientLogoTone === 'dark'
      ? 'is-light-plate'
      : headerVariant === 'plate' && clientLogoTone === 'light'
        ? 'is-dark-plate'
        : '';

  return (
    <header
      className={`brief-header mb-11 border-b border-[var(--upstory-rule)] pb-7 ${useBand ? 'is-band -mx-7 bg-[var(--upstory-ink)] px-7 pt-6' : ''}`}
    >
      <div className="brief-header-brands flex flex-wrap items-center gap-x-5 gap-y-3">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`${SHARED}/upstory-logo.png`}
          alt="Upstory"
          className={`brief-header-upstory block h-[22px] w-auto shrink-0 ${useBand ? 'opacity-90' : ''}`}
        />
        <span className="brief-header-for font-serif text-[17px] italic leading-none text-[var(--upstory-ink-3)]">
          for
        </span>
        {headerVariant === 'plain' && !useBand ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={clientSrc}
            alt={clientAlt}
            className="brief-header-logo block h-7 w-auto max-w-[180px] shrink-0 object-contain"
          />
        ) : (
          <div className={`brief-header-client inline-flex shrink-0 items-center justify-start ${clientPlateClass}`}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={clientSrc} alt={clientAlt} className="block h-7 w-auto max-w-[180px] object-contain" />
          </div>
        )}
      </div>
    </header>
  );
}

/** @deprecated use BriefHeader — clientPlate was inverted naming */
export function ClientLogo({
  src,
  alt,
  clientPlate,
  clientLogoTone,
  headerVariant,
}: {
  src: string;
  alt: string;
  forLabel?: ReactNode;
  /** @deprecated use clientLogoTone */
  clientPlate?: 'dark' | 'light';
  clientLogoTone?: ClientLogoTone;
  headerVariant?: HeaderVariant;
}) {
  const tone =
    clientLogoTone ?? (clientPlate === 'light' ? 'dark' : clientPlate === 'dark' ? 'light' : 'dark');
  return (
    <BriefHeader
      clientSrc={src}
      clientAlt={alt}
      clientLogoTone={tone}
      headerVariant={headerVariant}
    />
  );
}

export function OutcomeHeadline({ children }: { children: ReactNode }) {
  return (
    <h1 className="m-0 w-full text-[clamp(1.85rem,5vw,2.35rem)] font-extrabold leading-[1.1] tracking-[-0.032em]">
      {children}
    </h1>
  );
}

export function MainInsight({
  eyebrow = 'Our read',
  children,
}: {
  eyebrow?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="relative mt-8 flex flex-col items-start gap-3 overflow-hidden rounded-xl border border-[var(--upstory-rule)] bg-gradient-to-b from-[var(--upstory-surface-raised)] to-[#fafaf8] px-[26px] py-[22px] shadow-[0_1px_0_rgba(21,29,31,0.04)] before:absolute before:inset-x-0 before:top-0 before:h-[3px] before:bg-gradient-to-r before:from-[var(--upstory-bronze)] before:via-[#c4a574] before:to-transparent">
      <div className="relative z-[1] flex items-center gap-2.5">
        <LightbulbIcon className="shrink-0 text-[var(--upstory-bronze)]" />
        <p className="m-0 text-[11px] font-bold uppercase tracking-[0.12em] text-[var(--upstory-bronze)]">
          {eyebrow}
        </p>
      </div>
      <div className="relative z-[1] w-full text-[1.125rem] leading-[1.58] text-[var(--upstory-ink-2)]" style={serif}>
        {children}
      </div>
    </div>
  );
}

type JourneyVisual = { type: 'journey'; steps: string[]; keyIndex: number; note?: string };
type FunnelVisual = {
  type: 'funnel';
  rows: { label: string; pct: number; key?: boolean }[];
};
type ChipsVisual = { type: 'chips'; cells: { label: string; value: string }[] };
type CalculatorVisual = {
  type: 'calculator';
  formula: ImpactCalcFormula;
  outputLabel: string;
  outputDesc?: string;
  baseline?: string;
  /** For multiplier line (e.g. current public rating count) */
  baselineCount?: number;
};

export type SolutionVisual = JourneyVisual | FunnelVisual | ChipsVisual | CalculatorVisual;

export function SolutionBlock({
  index,
  title,
  children,
  visual,
}: {
  index: 1 | 2 | 3;
  title: ReactNode;
  children: ReactNode;
  visual?: SolutionVisual;
}) {
  const num = String(index).padStart(2, '0');
  const inline = visual?.type === 'journey' || visual?.type === 'chips';
  const visualPanel = visual ? <SolutionVisualPanel visual={visual} inline={inline} /> : null;

  return (
    <article className={index === 1 ? 'pt-0' : 'border-t border-[var(--upstory-rule)] py-12'}>
      <div className="mb-3.5 flex items-start gap-4">
        <span className="shrink-0 pt-[5px] text-[13px] font-extrabold tracking-wide text-[var(--upstory-bronze)]">
          {num}
        </span>
        <h2 className="m-0 flex-1 text-[1.3rem] font-bold leading-[1.25] tracking-[-0.02em]">{title}</h2>
      </div>
      <div
        className={`w-full text-[17px] leading-[1.6] text-[var(--upstory-ink-2)] ${visual ? 'mb-5' : 'mb-0'}`}
        style={serif}
      >
        {children}
      </div>
      {visualPanel}
    </article>
  );
}

export function BriefSectionIntro({
  title,
  lead,
  listSpacing = true,
}: {
  title: ReactNode;
  lead?: ReactNode;
  /** false when list follows in same section with custom spacing */
  listSpacing?: boolean;
}) {
  return (
    <div className="mt-12 border-t border-[var(--upstory-rule)] pt-10">
      <h2 className="m-0 mb-2.5 text-2xl font-extrabold tracking-[-0.02em] text-[var(--upstory-ink)]">
        {title}
      </h2>
      {lead ? (
        <p
          className={`m-0 w-full font-serif text-base leading-normal text-[var(--upstory-ink-3)] ${listSpacing ? 'mb-8' : 'mb-0'}`}
        >
          {lead}
        </p>
      ) : null}
    </div>
  );
}

export function OpportunitiesIntro({
  lead = 'Three places we would start in the product.',
}: {
  lead?: ReactNode;
}) {
  return <BriefSectionIntro title="Opportunities" lead={lead} />;
}

/** @deprecated use OpportunitiesIntro */
export const SolutionsIntro = OpportunitiesIntro;

export function OpportunitiesGroup({ children }: { children: ReactNode }) {
  return <section className="space-y-0">{children}</section>;
}

/** @deprecated use OpportunitiesGroup */
export const SolutionsGroup = OpportunitiesGroup;

function SolutionVisualPanel({ visual, inline }: { visual: SolutionVisual; inline: boolean }) {
  const wrap = inline
    ? 'w-full border-t border-dashed border-[var(--upstory-rule)] py-3.5'
    : 'w-full rounded-[10px] border border-[var(--upstory-rule)] bg-[var(--upstory-surface-raised)] px-5 py-[22px]';

  return (
    <div className={`${wrap} max-w-full`}>
      {visual.type === 'journey' && (
        <>
          <div className="flex w-full items-center gap-3 text-sm font-semibold text-[var(--upstory-ink-2)]">
            {visual.steps.map((step, i) => (
              <span key={i} className="contents">
                {i > 0 && <span className="shrink-0 font-normal text-[var(--upstory-ink-3)]">→</span>}
                <span
                  className={`min-w-0 flex-1 ${i === visual.keyIndex ? 'text-[var(--upstory-ink)]' : ''}`}
                >
                  {step}
                </span>
              </span>
            ))}
          </div>
          {visual.note ? (
            <p className="mt-2.5 text-[11px] font-semibold uppercase tracking-[0.06em] text-[var(--upstory-ink-3)]">
              {visual.note}
            </p>
          ) : null}
        </>
      )}
      {visual.type === 'funnel' && <FunnelVisual rows={visual.rows} />}
      {visual.type === 'chips' && (
        <div className="flex w-full gap-2">
          {visual.cells.map((cell, i) => (
            <div
              key={i}
              className="min-w-0 flex-1 rounded-md border border-[var(--upstory-rule)] bg-[var(--upstory-surface)] px-3 py-2 font-sans text-xs font-semibold leading-snug text-[var(--upstory-ink)]"
            >
              <span className="mb-0.5 block text-[10px] font-bold uppercase tracking-[0.08em] text-[var(--upstory-ink-3)]">
                {cell.label}
              </span>
              {cell.value}
            </div>
          ))}
        </div>
      )}
      {visual.type === 'calculator' && (
        <ImpactCalculator
          formula={visual.formula}
          outputLabel={visual.outputLabel}
          outputDesc={visual.outputDesc}
          baseline={visual.baseline}
          baselineCount={visual.baselineCount}
        />
      )}
    </div>
  );
}

/** Same section pattern as Opportunities: large heading, optional lead, simple bullets (no 01–03) */
export function WaysToMeasure({
  title = 'Ways to measure success',
  lead = 'A few ideas for leading indicators we could track with you.',
  lines,
}: {
  title?: ReactNode;
  lead?: ReactNode;
  lines: ReactNode[];
}) {
  return (
    <section className="pb-4">
      <BriefSectionIntro title={title} lead={lead} />
      <ul className="m-0 mb-14 w-full list-none space-y-3.5 p-0">
        {lines.map((line, i) => (
          <li key={i} className="flex gap-3 text-[17px] leading-[1.6] text-[var(--upstory-ink-2)]" style={serif}>
            <span className="mt-0.5 shrink-0 font-bold text-[var(--upstory-bronze)]">&middot;</span>
            <span>{line}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

/** @deprecated use WaysToMeasure */
export const ClosingFrame = WaysToMeasure;

export function UpstoryCloser() {
  return (
    <section className="mt-20 border-t border-[var(--upstory-rule)] pt-12">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={`${SHARED}/upstory-logo.png`} alt="Upstory" className="mb-[18px] block h-[22px] w-auto" />
      <div className="w-full text-pretty text-[17px] leading-[1.55] text-[var(--upstory-ink-2)]" style={serif}>
        <p>
          <strong className="font-semibold text-[var(--upstory-ink)]">Upstory is a product design firm</strong>.
          We specialize in growth and retention for consumer products that ask for sensitive
          information. Our focus is in health, fintech, and identity, with client work featuring
          LifeMD, Firefox, and Wander.
        </p>
      </div>
      <div className="mt-6 flex items-center gap-3.5">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`${SHARED}/rick-russie.avif`}
          alt="Rick Russie"
          className="h-[52px] w-[52px] rounded-full border border-[var(--upstory-rule)] object-cover"
        />
        <div>
          <p className="m-0 text-[15px] font-bold">Rick Russie</p>
          <p className="mt-1 text-sm text-[var(--upstory-ink-2)]" style={serif}>
            Founder and Design Lead, Upstory
          </p>
        </div>
      </div>
      <a
        href="https://www.upstory.co"
        className="mt-5 inline-block text-sm font-medium text-[var(--upstory-ink-2)] no-underline hover:text-[var(--upstory-ink)]"
      >
        upstory.co <span className="text-[13px]">↗</span>
      </a>
    </section>
  );
}

export function BriefFooter() {
  return (
    <footer className="mt-10 flex flex-wrap items-center justify-between gap-3 border-t border-[var(--upstory-rule)] pt-6 text-[15px] text-[var(--upstory-ink-2)]" style={serif}>
      <span>We design the moments where consumer products earn users.</span>
      <span className="font-sans text-xs text-[var(--upstory-ink-3)]">&copy; Upstory 2026</span>
    </footer>
  );
}
