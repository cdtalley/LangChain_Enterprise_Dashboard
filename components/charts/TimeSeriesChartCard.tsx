"use client";

import {
  AreaChart,
  Area,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import ChartCard from "./ChartCard";
import { CHART_COLORS } from "@/lib/utils";

export interface TimeSeriesChartCardDataItem {
  [key: string]: string | number;
}

interface TimeSeriesChartCardProps {
  title: string;
  subtitle?: string;
  data: TimeSeriesChartCardDataItem[];
  /** Key for the value (area/line) */
  valueKey: string;
  /** Key for x-axis (e.g. date, index) */
  xKey: string;
  variant?: "area" | "line";
  /** Color index in CHART_COLORS. Default 0 (primary). */
  colorIndex?: number;
  height?: number;
  formatValue?: (value: number) => string;
}

const defaultFormat = (v: number) => v.toLocaleString();

export default function TimeSeriesChartCard({
  title,
  subtitle,
  data,
  valueKey,
  xKey,
  variant = "area",
  colorIndex = 0,
  height = 300,
  formatValue = defaultFormat,
}: TimeSeriesChartCardProps) {
  const stroke = CHART_COLORS[colorIndex % CHART_COLORS.length];

  return (
    <ChartCard title={title} subtitle={subtitle}>
      <ResponsiveContainer width="100%" height={height}>
        {variant === "area" ? (
          <AreaChart
            data={data}
            margin={{ top: 8, right: 8, left: 0, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="var(--border)"
              vertical={false}
            />
            <XAxis
              dataKey={xKey}
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--border)" }}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) =>
                v >= 1000 ? `${(v / 1000).toFixed(1)}k` : String(v)
              }
            />
            <Tooltip
              contentStyle={{
                borderRadius: "12px",
                border: "1px solid var(--border)",
                boxShadow: "var(--shadow-lg)",
                padding: "12px 16px",
              }}
              labelStyle={{ fontWeight: 600, color: "var(--foreground)" }}
              formatter={(value: number) => [formatValue(value), valueKey]}
              labelFormatter={(label) => String(label)}
            />
            <Area
              type="monotone"
              dataKey={valueKey}
              stroke={stroke}
              strokeWidth={2}
              fill={stroke}
              fillOpacity={0.35}
            />
          </AreaChart>
        ) : (
          <LineChart
            data={data}
            margin={{ top: 8, right: 8, left: 0, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="var(--border)"
              vertical={false}
            />
            <XAxis
              dataKey={xKey}
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={{ stroke: "var(--border)" }}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 12, fill: "var(--muted)" }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) =>
                v >= 1000 ? `${(v / 1000).toFixed(1)}k` : String(v)
              }
            />
            <Tooltip
              contentStyle={{
                borderRadius: "12px",
                border: "1px solid var(--border)",
                boxShadow: "var(--shadow-lg)",
                padding: "12px 16px",
              }}
              labelStyle={{ fontWeight: 600, color: "var(--foreground)" }}
              formatter={(value: number) => [formatValue(value), valueKey]}
              labelFormatter={(label) => String(label)}
            />
            <Line
              type="monotone"
              dataKey={valueKey}
              stroke={stroke}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6, fill: stroke, strokeWidth: 2, stroke: "#fff" }}
            />
          </LineChart>
        )}
      </ResponsiveContainer>
    </ChartCard>
  );
}
