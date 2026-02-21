"use client";

/** Shared SVG gradient definitions for Recharts. Use inside <ResponsiveContainer> or chart wrapper. */
export function ChartDefs() {
  return (
    <defs>
      <linearGradient id="chartGradientPrimary" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#6366f1" stopOpacity={1} />
        <stop offset="100%" stopColor="#6366f1" stopOpacity={0.6} />
      </linearGradient>
      <linearGradient id="chartGradientSecondary" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#8b5cf6" stopOpacity={1} />
        <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.6} />
      </linearGradient>
      <linearGradient id="chartGradientAccent" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#06b6d4" stopOpacity={1} />
        <stop offset="100%" stopColor="#06b6d4" stopOpacity={0.5} />
      </linearGradient>
      <linearGradient id="chartGradientSuccess" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#10b981" stopOpacity={1} />
        <stop offset="100%" stopColor="#10b981" stopOpacity={0.5} />
      </linearGradient>
    </defs>
  );
}
