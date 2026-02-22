import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Executive-ready chart palette: primary, secondary, accent, success, warning, muted */
export const CHART_COLORS = [
  "#6366f1", // indigo-500
  "#8b5cf6", // violet-500
  "#06b6d4", // cyan-500
  "#10b981", // emerald-500
  "#f59e0b", // amber-500
  "#ec4899", // pink-500
  "#64748b", // slate-500
] as const;

export const CHART_GRADIENTS = {
  primary: "url(#chartGradientPrimary)",
  secondary: "url(#chartGradientSecondary)",
  accent: "url(#chartGradientAccent)",
  success: "url(#chartGradientSuccess)",
} as const;

/** Format for "Data as of" / "Last updated" copy. */
export function formatDataAsOf(date: Date | null): string {
  if (!date) return "—";
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1) return "Just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}
