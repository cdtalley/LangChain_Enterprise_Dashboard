"use client";

import { Zap, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function EnsemblingPage() {
  const { ecommerceData, financeData } = useData();

  const models = [
    { name: "Model A", accuracy: 92.5, weight: 0.3 },
    { name: "Model B", accuracy: 94.2, weight: 0.4 },
    { name: "Model C", accuracy: 93.8, weight: 0.3 },
  ];

  const ensembleAccuracy = models.reduce((sum, m) => sum + m.accuracy * m.weight, 0);

  return (
    <div className="space-y-6" data-tour="ensembling">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Model Ensembling</h1>
        <p className="text-gray-600">Combine multiple models for improved performance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard
          title="Ensemble Accuracy"
          value={`${ensembleAccuracy.toFixed(2)}%`}
          icon={Zap}
          gradient="from-purple-500 to-indigo-500"
        />
        <MetricCard
          title="Individual Models"
          value={models.length}
        />
        <MetricCard
          title="Improvement"
          value={`+${(ensembleAccuracy - Math.max(...models.map(m => m.accuracy))).toFixed(2)}%`}
          icon={TrendingUp}
          gradient="from-green-500 to-emerald-500"
          trend="up"
        />
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-bold mb-4">Model Performance Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={models}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="accuracy" fill="#667eea" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-bold mb-4">Ensemble Configuration</h3>
        <div className="space-y-3">
          {models.map((model, idx) => (
            <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <div className="font-bold">{model.name}</div>
                <div className="text-sm text-gray-600">Accuracy: {model.accuracy}%</div>
              </div>
              <div className="text-right">
                <div className="font-bold">Weight: {(model.weight * 100).toFixed(0)}%</div>
                <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                  <div
                    className="bg-purple-600 h-2 rounded-full"
                    style={{ width: `${model.weight * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
