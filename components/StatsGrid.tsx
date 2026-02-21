"use client";

import { motion } from "framer-motion";
import { Activity, Zap, Database, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

const stats = [
  {
    label: "System Uptime",
    value: "99.9%",
    icon: Activity,
    color: "from-emerald-500 to-teal-600",
    trend: "+0.1%",
    trendUp: true,
  },
  {
    label: "Avg Response Time",
    value: "1.2s",
    icon: Zap,
    color: "from-cyan-500 to-blue-600",
    trend: "-0.3s",
    trendUp: true,
  },
  {
    label: "Data Processed",
    value: "11K+",
    icon: Database,
    color: "from-violet-500 to-indigo-600",
    trend: "+2.1K",
    trendUp: true,
  },
  {
    label: "Active Models",
    value: "12",
    icon: TrendingUp,
    color: "from-amber-500 to-orange-600",
    trend: "+3",
    trendUp: true,
  },
];

export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-12">
      {stats.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.08, duration: 0.35 }}
            whileHover={{ y: -3, scale: 1.01 }}
            className="group relative overflow-hidden bg-white rounded-xl shadow-[var(--shadow-md)] border border-[var(--border)] p-6 hover:shadow-[var(--shadow-lg)] hover:border-indigo-200/60 transition-all duration-250"
          >
            <div className={cn("absolute top-0 left-0 right-0 h-0.5 rounded-t-xl bg-gradient-to-r", stat.color)} />
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className={cn("w-11 h-11 rounded-xl bg-gradient-to-br flex items-center justify-center shadow-sm", stat.color)}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <span className={cn(
                  "text-xs font-semibold px-2 py-1 rounded-lg",
                  stat.trendUp ? "text-emerald-600 bg-emerald-50" : "text-slate-500 bg-slate-100"
                )}>
                  {stat.trend}
                </span>
              </div>
              <div className="text-2xl font-bold tracking-tight text-[var(--foreground)] mb-0.5">{stat.value}</div>
              <div className="text-sm font-medium text-[var(--muted)]">{stat.label}</div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
