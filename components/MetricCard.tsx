"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
  gradient?: string;
}

export default function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendValue,
  gradient = "from-indigo-500 to-violet-500",
}: MetricCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className={cn(
        "bg-gradient-to-br text-white rounded-xl shadow-[var(--shadow-md)] p-6",
        "border border-white/10 transition-shadow duration-200 hover:shadow-[var(--shadow-lg)]",
        gradient
      )}
    >
      <div className="flex items-center justify-between mb-3">
        {Icon && (
          <div className="w-10 h-10 rounded-lg bg-white/15 flex items-center justify-center">
            <Icon className="w-5 h-5 opacity-95" />
          </div>
        )}
        {trend && (
          <span
            className={cn(
              "text-xs font-semibold px-2 py-1 rounded-md",
              trend === "up" && "bg-emerald-400/25 text-emerald-100",
              trend === "down" && "bg-red-400/25 text-red-100",
              trend === "neutral" && "bg-white/15 text-white/90"
            )}
          >
            {trend === "up" && "↑"} {trend === "down" && "↓"} {trendValue ?? "—"}
          </span>
        )}
      </div>
      <div className="text-2xl md:text-3xl font-bold tracking-tight mb-0.5">{value}</div>
      <div className="text-sm font-medium text-white/90">{title}</div>
      {subtitle && <div className="text-xs text-white/75 mt-1">{subtitle}</div>}
    </motion.div>
  );
}

