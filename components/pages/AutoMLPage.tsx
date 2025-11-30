"use client";

import { useState } from "react";
import { Sparkles, Play, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

export default function AutoMLPage() {
  const { ecommerceData, financeData } = useData();
  const [isTraining, setIsTraining] = useState(false);
  const [models] = useState([
    { name: "Random Forest", accuracy: 94.2, trainingTime: "2.3s" },
    { name: "XGBoost", accuracy: 96.5, trainingTime: "3.1s" },
    { name: "LightGBM", accuracy: 95.8, trainingTime: "1.8s" },
    { name: "Neural Network", accuracy: 93.1, trainingTime: "12.4s" },
  ]);

  const handleTrain = () => {
    setIsTraining(true);
    setTimeout(() => setIsTraining(false), 3000);
  };

  return (
    <div className="space-y-6" data-tour="automl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🤖 AutoML</h1>
          <p className="text-gray-600">Automated machine learning pipeline</p>
        </div>
        <button
          onClick={handleTrain}
          disabled={isTraining}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50"
        >
          {isTraining ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Training...
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              Start AutoML Pipeline
            </>
          )}
        </button>
      </div>

      {/* Dataset Selection */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Select Training Dataset</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-500 transition-colors cursor-pointer">
            <h3 className="font-bold mb-2">E-commerce Data</h3>
            <p className="text-sm text-gray-600">{ecommerceData.length.toLocaleString()} records</p>
          </div>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-500 transition-colors cursor-pointer">
            <h3 className="font-bold mb-2">Finance Data</h3>
            <p className="text-sm text-gray-600">{financeData.length.toLocaleString()} records</p>
          </div>
        </div>
      </div>

      {/* Model Results */}
      {models.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Model Comparison</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={models}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
            {models.map((model, idx) => (
              <div key={idx} className="bg-gray-50 rounded-lg p-4">
                <div className="font-bold mb-2">{model.name}</div>
                <div className="text-2xl font-bold text-purple-600">{model.accuracy}%</div>
                <div className="text-sm text-gray-600">Training: {model.trainingTime}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <DataTable data={ecommerceData.slice(0, 100)} title="Training Data Preview" maxRows={5} />
    </div>
  );
}
