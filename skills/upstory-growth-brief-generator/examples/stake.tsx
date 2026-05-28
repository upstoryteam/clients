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
  SHARED,
  UpstoryCloser,
} from '../brief-ui';

export const metadata: Metadata = {
  title: 'Upstory for Stake',
  description: 'A short note from Upstory.',
  robots: { index: false, follow: false },
};

export default function StakePage() {
  return (
    <BriefShell>
      <BriefPage>
        <BriefHeader
          clientSrc={`${SHARED}/logos/stake.svg`}
          alt="Stake"
          clientLogoTone="light"
          headerVariant="band"
        />

        <OutcomeHeadline>
          We believe we can help Stake move 40% of UMoveFree renters to first rent payment within 30 days.
        </OutcomeHeadline>

        <MainInsight>
          <p>
            You have a short window right after UMoveFree handoff while renters still have the apartment math in mind. Cash
            Back should land in that first session. The opportunities below are where we would start.
          </p>
        </MainInsight>

        <OpportunitiesIntro />

        <OpportunitiesGroup>
          <SolutionBlock
            index={1}
            title="Show the payoff before the deposit ask"
            visual={{
              type: 'journey',
              steps: ['UMoveFree signup', 'Value + math', 'Deposit ask'],
              keyIndex: 2,
            }}
          >
            <p>
              UMoveFree renters arrive looking for an apartment. The first screen after handoff should prove the math,
              then ask for money.
            </p>
          </SolutionBlock>

          <SolutionBlock
            index={2}
            title="Design for first rent payment as the proof moment"
            visual={{
              type: 'funnel',
              rows: [
                { label: 'UMoveFree signup', pct: 100 },
                { label: 'Onboarding done', pct: 62 },
                { label: 'First rent payment', pct: 38, key: true },
              ],
            }}
          >
            <p>
              First rent payment is when the product proves itself. We would map every step from onboarding complete to
              payment scheduled.
            </p>
          </SolutionBlock>

          <SolutionBlock index={3} title="Measure the UMoveFree cohort on its own terms">
            <p>
              Hold UMoveFree as its own cohort with a matched organic baseline so you can read lift without blending
              channels.
            </p>
          </SolutionBlock>
        </OpportunitiesGroup>

        <WaysToMeasure
          lines={[
            'Higher completion from onboarding to payment scheduled within 7 days.',
            'Cash Back activation within seven days of first payment.',
            'UMoveFree cohort trending above organic matched by signup week.',
          ]}
        />

        <UpstoryCloser />
        <BriefFooter />
      </BriefPage>
    </BriefShell>
  );
}
