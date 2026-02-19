"use client";

import { motion } from "framer-motion";
import { Activity, Zap, Database, TrendingUp } from "lucide-react";

const stats = [
  {
    label: "System Uptime",
    value: "99.9%",
    icon: Activity,
    color: "from-green-500 to-emerald-600",
    trend: "+0.1%",
  },
  {
    label: "Avg Response Time",
    value: "1.2s",
    icon: Zap,
    color: "from-blue-500 to-cyan-600",
    trend: "-0.3s",
  },
  {
    label: "Data Processed",
    value: "11K+",
    icon: Database,
    color: "from-purple-500 to-indigo-600",
    trend: "+2.1K",
  },
  {
    label: "Active Models",
    value: "12",
    icon: TrendingUp,
    color: "from-orange-500 to-red-600",
    trend: "+3",
  },
];

export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
      {stats.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -4, scale: 1.02 }}
            className="group relative overflow-hidden bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300"
          >
            {/* Gradient accent */}
            <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${stat.color}`}></div>
            
            {/* Shimmer effect on hover */}
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
              <div className="absolute inset-0 shimmer"></div>
            </div>
            
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded">
                  {stat.trend}
                </span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-sm font-medium text-gray-600">{stat.label}</div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
