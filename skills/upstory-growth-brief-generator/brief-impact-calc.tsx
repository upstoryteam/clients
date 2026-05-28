'use client';

import { useMemo, useState } from 'react';

export type ImpactCalcFormula = 'app_store_ratings_90d' | 'umove_first_payment_lift';

type CalcInputDef = {
  id: string;
  label: string;
  min: number;
  max: number;
  step: number;
  defaultValue: number;
  format: 'number' | 'percent';
};

const PRESETS: Record<
  ImpactCalcFormula,
  {
    inputs: CalcInputDef[];
    compute: (v: Record<string, number>) => number;
    helper?: string;
    multiplier?: (result: number, baseline: number) => number;
  }
> = {
  app_store_ratings_90d: {
    inputs: [
      { id: 'mau', label: 'Monthly active users', min: 500, max: 20000, step: 500, defaultValue: 3000, format: 'number' },
      { id: 'prompt', label: 'Prompted at the right moment', min: 10, max: 80, step: 5, defaultValue: 40, format: 'percent' },
      { id: 'convert', label: 'Of prompted, who rate', min: 2, max: 20, step: 1, defaultValue: 8, format: 'percent' },
    ],
    compute: (v) => Math.round(v.mau * (v.prompt / 100) * (v.convert / 100) * 3),
    helper:
      "Defaults reflect Apple's published benchmarks for in-app rating prompts. Drag any slider to see how the numbers move.",
    multiplier: (result, baseline) => Math.max(1, Math.round((result + baseline) / Math.max(baseline, 1))),
  },
  umove_first_payment_lift: {
    inputs: [
      { id: 'signups', label: 'UMoveFree signups / month', min: 100, max: 5000, step: 50, defaultValue: 800, format: 'number' },
      { id: 'baseline', label: 'Current first-payment rate', min: 20, max: 50, step: 1, defaultValue: 38, format: 'percent' },
      { id: 'lift', label: 'Lift from product changes', min: 5, max: 15, step: 1, defaultValue: 10, format: 'percent' },
    ],
    compute: (v) => Math.round(v.signups * (v.lift / 100)),
    helper: 'Illustrative model for additional first rent payments per month from a focused cohort fix.',
  },
};

export function ImpactCalculator({
  formula,
  outputLabel,
  outputDesc,
  baseline,
  baselineCount = 0,
}: {
  formula: ImpactCalcFormula;
  outputLabel: string;
  outputDesc?: string;
  baseline?: string;
  baselineCount?: number;
}) {
  const preset = PRESETS[formula];
  const [values, setValues] = useState(() =>
    Object.fromEntries(preset.inputs.map((i) => [i.id, i.defaultValue]))
  );

  const result = useMemo(() => preset.compute(values), [preset, values]);
  const multiplier = preset.multiplier?.(result, baselineCount);

  return (
    <div className="vis-impact-calc w-full">
      <div className="vis-calc-inputs">
        {preset.inputs.map((input) => (
          <div key={input.id} className="vis-calc-input">
            <div className="vis-calc-label-row">
              <span className="vis-calc-label">{input.label}</span>
              <span className="vis-calc-value">
                {input.format === 'percent' ? `${values[input.id]}%` : values[input.id].toLocaleString()}
              </span>
            </div>
            <input
              type="range"
              className="vis-calc-slider"
              min={input.min}
              max={input.max}
              step={input.step}
              value={values[input.id]}
              onChange={(e) =>
                setValues((prev) => ({ ...prev, [input.id]: parseFloat(e.target.value) }))
              }
            />
          </div>
        ))}
        {preset.helper ? <p className="vis-calc-helper">{preset.helper}</p> : null}
      </div>
      <div className="vis-calc-output-pane">
        <p className="vis-calc-out-label">{outputLabel}</p>
        <p className="vis-calc-out-number">{result.toLocaleString()}</p>
        {outputDesc ? <p className="vis-calc-out-desc">{outputDesc}</p> : null}
        {baseline ? (
          <p className="vis-calc-out-baseline">
            {baseline}
            {multiplier ? (
              <>
                {' '}
                At these assumptions, that is <strong>{multiplier}×</strong> your public count today.
              </>
            ) : null}
          </p>
        ) : null}
      </div>
    </div>
  );
}
