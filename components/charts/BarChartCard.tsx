"use client";

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import ChartCard from "./ChartCard";
import { CHART_COLORS } from "@/lib/utils";

export interface BarChartCardDataItem {
  [key: string]: string | number;
}

interface BarChartCardProps {
  title: string;
  subtitle?: string;
  data: BarChartCardDataItem[];
  dataKey: string;
  nameKey: string;
  /** Bar color: CSS color or index into CHART_COLORS. Default: primary gradient. */
  color?: string | number;
  height?: number;
  /** Format value in tooltip (e.g. (v) => `$${v.toLocaleString()}`). */
  formatValue?: (value: number) => string;
}

const defaultFormat = (v: number) => v.toLocaleString();

export default function BarChartCard({
  title,
  subtitle,
  data,
  dataKey,
  nameKey,
  color = 0,
  height = 300,
  formatValue = defaultFormat,
}: BarChartCardProps) {
  const barColor =
    typeof color === "number"
      ? CHART_COLORS[color % CHART_COLORS.length]
      : color;

  return (
    <ChartCard title={title} subtitle={subtitle}>
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart
          data={data}
          margin={{ top: 8, right: 8, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="barGradientPrimary" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={1} />
              <stop offset="100%" stopColor="#6366f1" stopOpacity={0.75} />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="var(--border)"
            vertical={false}
          />
          <XAxis
            dataKey={nameKey}
            tick={{ fontSize: 12, fill: "var(--muted)" }}
            axisLine={{ stroke: "var(--border)" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 12, fill: "var(--muted)" }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => (v >= 1000 ? `${(v / 1000).toFixed(1)}k` : String(v))}
          />
          <Tooltip
            contentStyle={{
              borderRadius: "12px",
              border: "1px solid var(--border)",
              boxShadow: "var(--shadow-lg)",
              padding: "12px 16px",
            }}
            labelStyle={{ fontWeight: 600, color: "var(--foreground)" }}
            formatter={(value: number) => [formatValue(value), dataKey]}
            labelFormatter={(label) => String(label)}
          />
          <Bar
            dataKey={dataKey}
            radius={[6, 6, 0, 0]}
            maxBarSize={56}
            fill={barColor}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={barColor} />
            ))}
          </Bar>
        </RechartsBarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
