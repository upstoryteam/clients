import type { FunnelRowInput } from './funnel-geometry';
import { buildFunnelModel } from './funnel-geometry';

export function FunnelVisual({ rows }: { rows: FunnelRowInput[] }) {
  const model = buildFunnelModel(rows);

  return (
    <div className="vis-funnel">
      <div className="vis-funnel-layout" style={{ '--funnel-stage-h': `${model.stageH}px` }}>
        <div className="vis-funnel-aside vis-funnel-labels">
          {model.rows.map((row, i) => (
            <div key={i} className={`vis-funnel-meta${row.key ? ' is-key' : ''}`}>
              {row.label}
            </div>
          ))}
        </div>
        <svg
          className="vis-funnel-svg"
          viewBox={`0 0 ${model.vbW} ${model.vbH}`}
          role="img"
          aria-label="Conversion funnel"
        >
          {model.segments.map((seg, i) => (
            <path
              key={i}
              d={seg.d}
              className={seg.key ? 'vis-funnel-fill is-key' : 'vis-funnel-fill'}
            />
          ))}
          {model.dividers.map((div, i) => (
            <line
              key={`d-${i}`}
              x1={div.x1}
              y1={div.y}
              x2={div.x2}
              y2={div.y}
              className="vis-funnel-divider"
            />
          ))}
        </svg>
        <div className="vis-funnel-aside vis-funnel-pcts">
          {model.rows.map((row, i) => (
            <div key={i} className={`vis-funnel-meta${row.key ? ' is-key' : ''}`}>
              {row.pct}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
