/** Shared SVG funnel geometry for growth brief artifacts */

export type FunnelRowInput = { label: string; pct: number; key?: boolean };

const VB_W = 200;
const STAGE_H = 48;
const PAD_X = 10;
const CX = VB_W / 2;
/** Pull side curves slightly inward for a smooth funnel silhouette (not stacked blocks). */
const CURVE_INSET = 0.94;

export type FunnelSegment = {
  d: string;
  key?: boolean;
};

export function buildFunnelModel(rows: FunnelRowInput[]) {
  const n = rows.length;
  const vbH = n * STAGE_H;
  const maxHw = CX - PAD_X;

  const halfW = (pct: number) => maxHw * (pct / 100);

  const segments: FunnelSegment[] = rows.map((row, i) => {
    const y0 = i * STAGE_H;
    const y1 = (i + 1) * STAGE_H;
    const w0 = halfW(row.pct);
    const w1 = i < n - 1 ? halfW(rows[i + 1].pct) : w0 * 0.92;
    const midY = (y0 + y1) / 2;
    const wMidR = ((w0 + w1) / 2) * CURVE_INSET;
    const wMidL = wMidR;

    const d = [
      `M ${CX - w0} ${y0}`,
      `L ${CX + w0} ${y0}`,
      `Q ${CX + wMidR} ${midY} ${CX + w1} ${y1}`,
      `L ${CX - w1} ${y1}`,
      `Q ${CX - wMidL} ${midY} ${CX - w0} ${y0}`,
      'Z',
    ].join(' ');

    return { d, key: row.key };
  });

  const dividers = rows.slice(0, -1).map((_, i) => {
    const y = (i + 1) * STAGE_H;
    const hw = halfW(rows[i + 1].pct);
    return { y, x1: CX - hw, x2: CX + hw };
  });

  return { vbW: VB_W, vbH, stageH: STAGE_H, segments, dividers, rows };
}

export const FUNNEL_PAD_X = PAD_X;
