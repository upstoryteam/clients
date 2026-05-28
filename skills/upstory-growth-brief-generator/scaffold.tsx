import type { Metadata } from 'next';
import {
  BriefFooter,
  BriefPage,
  BriefShell,
  BriefHeader,
  WaysToMeasure,
  MainInsight,
  OutcomeHeadline,
  SolutionBlock,
  OpportunitiesGroup,
  OpportunitiesIntro,
  UpstoryCloser,
} from './brief-ui';
import { UPOSTORY_BRIEF_FONT_URL } from './upstory-tokens';

// See FORMAT.md — locked arc: headline → insight → opportunities (+ optional artifacts) → measure → pitch

export const metadata: Metadata = {
  title: 'Upstory for {{company_name}}',
  description: 'A short note from Upstory.',
  robots: { index: false, follow: false },
};

export { UPOSTORY_BRIEF_FONT_URL };

export default function Page() {
  return (
    <BriefShell>
      <BriefPage>
        <BriefHeader
          clientSrc="{{company_logo_url}}"
          clientAlt="{{company_name}}"
          clientLogoTone="{{client_logo_tone}}"
          headerVariant="{{header_variant}}"
        />

        <OutcomeHeadline>{{hero_headline}}</OutcomeHeadline>
        <MainInsight>
          <p>{{main_insight}}</p>
        </MainInsight>

        <OpportunitiesIntro lead="{{opportunities_lead}}" />

        {/* Per block: journey = sequence, funnel = drop-off, chips = rare. Delete visual={{...}} if FORMAT.md relevance test fails. */}
        <OpportunitiesGroup>
          <SolutionBlock
            index={1}
            title="{{solution_1_title}}"
            visual={{
              type: 'journey',
              steps: ['{{solution_1_vis_step_1}}', '{{solution_1_vis_step_2}}', '{{solution_1_vis_step_3}}'],
              keyIndex: 2,
            }}
          >
            <p>{{solution_1_body}}</p>
          </SolutionBlock>

          <SolutionBlock
            index={2}
            title="{{solution_2_title}}"
            visual={{
              type: 'funnel',
              rows: [
                { label: '{{solution_2_funnel_1_label}}', pct: 100 },
                { label: '{{solution_2_funnel_2_label}}', pct: 62 },
                { label: '{{solution_2_funnel_3_label}}', pct: 38, key: true },
              ],
            }}
          >
            <p>{{solution_2_body}}</p>
          </SolutionBlock>

          <SolutionBlock index={3} title="{{solution_3_title}}">
            <p>{{solution_3_body}}</p>
          </SolutionBlock>
        </OpportunitiesGroup>

        <WaysToMeasure
          lead="{{measure_lead}}"
          lines={['{{closing_line_1}}', '{{closing_line_2}}', '{{closing_line_3}}']}
        />

        <UpstoryCloser />
        <BriefFooter />
      </BriefPage>
    </BriefShell>
  );
}
