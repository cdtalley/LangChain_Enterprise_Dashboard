"use client";

import { motion } from "framer-motion";
import { Activity, Zap, Bot, Database, TrendingUp } from "lucide-react";

const stats = [
  { icon: Activity, label: "Status", value: "Operational", subtext: "99.9% Uptime", color: "text-green-500" },
  { icon: Zap, label: "Performance", value: "1.2s", subtext: "Avg Response", color: "text-blue-500" },
  { icon: Bot, label: "Agents", value: "3 Active", subtext: "Specialized", color: "text-purple-500" },
  { icon: Database, label: "Models", value: "12", subtext: "Registered", color: "text-indigo-500" },
  { icon: TrendingUp, label: "Features", value: "50+", subtext: "Available", color: "text-pink-500" },
];

export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {stats.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05, y: -5 }}
            className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all"
          >
            <div className="flex items-center justify-between mb-4">
              <Icon className={`w-8 h-8 ${stat.color}`} />
            </div>
            <div className="space-y-1">
              <p className="text-sm text-gray-600 font-medium">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-xs text-gray-500">{stat.subtext}</p>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

