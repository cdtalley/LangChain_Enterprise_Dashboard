"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

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
  gradient = "from-purple-500 to-blue-500",
}: MetricCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      className={`bg-gradient-to-br ${gradient} text-white rounded-xl shadow-lg p-6`}
    >
      <div className="flex items-center justify-between mb-4">
        {Icon && <Icon className="w-8 h-8 opacity-90" />}
        {trend && (
          <div
            className={`text-sm font-semibold ${
              trend === "up" ? "text-green-200" : trend === "down" ? "text-red-200" : "text-gray-200"
            }`}
          >
            {trend === "up" && "↑"} {trend === "down" && "↓"} {trendValue}
          </div>
        )}
      </div>
      <div className="text-3xl font-bold mb-1">{value}</div>
      <div className="text-sm opacity-90">{title}</div>
      {subtitle && <div className="text-xs opacity-75 mt-1">{subtitle}</div>}
    </motion.div>
  );
}

