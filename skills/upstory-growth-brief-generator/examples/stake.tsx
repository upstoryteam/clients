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
          We believe we can help Stake lift first rent payment conversion on the UMoveFree cohort by about 10%.
        </OutcomeHeadline>

        <MainInsight>
          <p>
            The Lighthouse fold-in is an opportunity to create value: renters arrive from UMoveFree with housing intent. In the
            product, the handoff and first weeks need to make Cash Back concrete fast. The opportunities below are where
            we would focus.
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
              That payment converts curiosity into belief. We would look closely at the stretch between onboarding
              complete and first payment scheduled.
            </p>
          </SolutionBlock>

          <SolutionBlock
            index={3}
            title="Measure the UMoveFree cohort on its own terms"
            visual={{
              type: 'chips',
              cells: [
                { label: 'North-star', value: 'First rent payment in 30 days' },
                { label: 'Cohort', value: 'UMoveFree, 10% holdout' },
                { label: 'Win', value: '+5–10 pp at 60 days' },
              ],
            }}
          >
            <p>Hold the partner channel to its own bar so wins are readable without blending organic signups.</p>
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
