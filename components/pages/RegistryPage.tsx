"use client";

import { useState } from "react";
import { Package, Plus, TrendingUp, Activity, Eye } from "lucide-react";
import { motion } from "framer-motion";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import { useData } from "@/lib/DataContext";
import HelpGuide from "@/components/HelpGuide";

export default function RegistryPage() {
  const { ecommerceData, financeData } = useData();
  const [models] = useState([
    {
      id: "model-001",
      name: "E-commerce Revenue Predictor",
      version: "1.2.0",
      type: "Regression",
      accuracy: 94.5,
      status: "Production",
      created: "2024-01-15",
      records: ecommerceData.length,
    },
    {
      id: "model-002",
      name: "Fraud Detection Classifier",
      version: "2.1.0",
      type: "Classification",
      accuracy: 98.2,
      status: "Staging",
      created: "2024-02-01",
      records: financeData.length,
    },
  ]);

  const totalModels = models.length;
  const productionModels = models.filter(m => m.status === "Production").length;
  const avgAccuracy = models.reduce((sum, m) => sum + m.accuracy, 0) / models.length;

  return (
    <div className="space-y-6" data-tour="registry">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">📦 Model Registry</h1>
          <p className="text-gray-600">Versioning, lifecycle management, and model comparison</p>
        </div>
        <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all">
          <Plus className="w-5 h-5" />
          Register Model
        </button>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use Model Registry"
        description="Manage model versions, track performance, and compare models"
        steps={[
          {
            number: 1,
            title: "View Registered Models",
            description: "See all models in your registry with their versions, types, and status.",
          },
          {
            number: 2,
            title: "Check Model Metrics",
            description: "Review accuracy, status (Production/Staging), and training data size for each model.",
          },
          {
            number: 3,
            title: "Compare Models",
            description: "Use the summary cards to compare overall performance across all models.",
          },
          {
            number: 4,
            title: "Register New Model",
            description: "Click 'Register Model' to add a new model version to the registry.",
            action: () => {
              // Scroll to top where register button is
              window.scrollTo({ top: 0, behavior: 'smooth' });
            },
            actionLabel: "Scroll to Register"
          },
          {
            number: 5,
            title: "Monitor Production Models",
            description: "Track which models are in production vs staging, and their performance metrics.",
          }
        ]}
      />

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard
          title="Total Models"
          value={totalModels}
          icon={Package}
          gradient="from-purple-500 to-indigo-500"
        />
        <MetricCard
          title="Production Models"
          value={productionModels}
          icon={Activity}
          gradient="from-green-500 to-emerald-500"
        />
        <MetricCard
          title="Avg Accuracy"
          value={`${avgAccuracy.toFixed(1)}%`}
          icon={TrendingUp}
          gradient="from-blue-500 to-cyan-500"
        />
      </div>

      {/* Models List */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold">Registered Models</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {models.map((model, idx) => (
            <motion.div
              key={model.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="p-6 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Package className="w-6 h-6 text-purple-600" />
                    <h3 className="text-lg font-bold">{model.name}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${
                      model.status === "Production" 
                        ? "bg-green-100 text-green-700" 
                        : "bg-yellow-100 text-yellow-700"
                    }`}>
                      {model.status}
                    </span>
                  </div>
                  <div className="grid grid-cols-4 gap-4 text-sm text-gray-600">
                    <div>
                      <span className="font-semibold">Version:</span> {model.version}
                    </div>
                    <div>
                      <span className="font-semibold">Type:</span> {model.type}
                    </div>
                    <div>
                      <span className="font-semibold">Accuracy:</span> {model.accuracy}%
                    </div>
                    <div>
                      <span className="font-semibold">Records:</span> {model.records.toLocaleString()}
                    </div>
                  </div>
                </div>
                <button className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  View Details
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
