"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import EnterpriseDemo from "./EnterpriseDemo";
import AnalyticsDashboard from "./AnalyticsDashboard";
import DataGenerator from "./DataGenerator";

const tabs = [
  { id: "demo", label: "🎯 Enterprise Demo", component: EnterpriseDemo },
  { id: "analytics", label: "📈 Analytics Dashboard", component: AnalyticsDashboard },
  { id: "generator", label: "🚀 Data Generator", component: DataGenerator },
];

export default function DashboardTabs() {
  const [activeTab, setActiveTab] = useState("demo");

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || EnterpriseDemo;

  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 bg-gradient-to-r from-purple-50 to-blue-50">
        <div className="flex overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-4 font-medium text-sm transition-all relative ${
                activeTab === tab.id
                  ? "text-purple-600 border-b-2 border-purple-600"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {tab.label}
              {activeTab === tab.id && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-600"
                  initial={false}
                  transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <ActiveComponent />
        </motion.div>
      </div>
    </div>
  );
}

