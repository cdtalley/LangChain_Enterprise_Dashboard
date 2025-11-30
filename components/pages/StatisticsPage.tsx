"use client";

import { FlaskConical, TrendingUp } from "lucide-react";
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

export default function StatisticsPage() {
  const { financeData, ecommerceData } = useData();

  // Calculate statistics
  const financeStats = {
    mean: financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length,
    median: [...financeData].sort((a, b) => a.amount - b.amount)[Math.floor(financeData.length / 2)].amount,
    std: Math.sqrt(
      financeData.reduce((sum, r) => {
        const mean = financeData.reduce((s, x) => s + x.amount, 0) / financeData.length;
        return sum + Math.pow(r.amount - mean, 2);
      }, 0) / financeData.length
    ),
    min: Math.min(...financeData.map(r => r.amount)),
    max: Math.max(...financeData.map(r => r.amount)),
  };

  const ecommerceStats = {
    mean: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0) / ecommerceData.length,
    median: [...ecommerceData].sort((a, b) => a.total_amount - b.total_amount)[Math.floor(ecommerceData.length / 2)].total_amount,
    std: Math.sqrt(
      ecommerceData.reduce((sum, r) => {
        const mean = ecommerceData.reduce((s, x) => s + x.total_amount, 0) / ecommerceData.length;
        return sum + Math.pow(r.total_amount - mean, 2);
      }, 0) / ecommerceData.length
    ),
    min: Math.min(...ecommerceData.map(r => r.total_amount)),
    max: Math.max(...ecommerceData.map(r => r.total_amount)),
  };

  const statsData = [
    { metric: "Mean", finance: financeStats.mean, ecommerce: ecommerceStats.mean },
    { metric: "Median", finance: financeStats.median, ecommerce: ecommerceStats.median },
    { metric: "Std Dev", finance: financeStats.std, ecommerce: ecommerceStats.std },
    { metric: "Min", finance: financeStats.min, ecommerce: ecommerceStats.min },
    { metric: "Max", finance: financeStats.max, ecommerce: ecommerceStats.max },
  ];

  return (
    <div className="space-y-6" data-tour="statistics">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🔬 Statistical Analysis</h1>
        <p className="text-gray-600">Advanced statistical tests and hypothesis testing</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricCard
          title="Finance Mean"
          value={`$${financeStats.mean.toFixed(2)}`}
          icon={TrendingUp}
          gradient="from-pink-500 to-rose-500"
        />
        <MetricCard
          title="Finance Std Dev"
          value={`$${financeStats.std.toFixed(2)}`}
        />
        <MetricCard
          title="E-commerce Mean"
          value={`$${ecommerceStats.mean.toFixed(2)}`}
          icon={FlaskConical}
          gradient="from-blue-500 to-cyan-500"
        />
        <MetricCard
          title="E-commerce Std Dev"
          value={`$${ecommerceStats.std.toFixed(2)}`}
        />
        <MetricCard
          title="Sample Size"
          value={financeData.length.toLocaleString()}
        />
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-bold mb-4">Statistical Comparison</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={statsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="metric" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="finance" fill="#667eea" name="Finance" />
            <Bar dataKey="ecommerce" fill="#4facfe" name="E-commerce" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-bold mb-4">Finance Statistics</h3>
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <div className="flex justify-between">
              <span className="font-semibold">Mean:</span>
              <span>${financeStats.mean.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Median:</span>
              <span>${financeStats.median.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Std Deviation:</span>
              <span>${financeStats.std.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Min:</span>
              <span>${financeStats.min.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Max:</span>
              <span>${financeStats.max.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-bold mb-4">E-commerce Statistics</h3>
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <div className="flex justify-between">
              <span className="font-semibold">Mean:</span>
              <span>${ecommerceStats.mean.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Median:</span>
              <span>${ecommerceStats.median.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Std Deviation:</span>
              <span>${ecommerceStats.std.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Min:</span>
              <span>${ecommerceStats.min.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-semibold">Max:</span>
              <span>${ecommerceStats.max.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DataTable data={financeData.slice(0, 100)} title="Finance Data" maxRows={5} />
        <DataTable data={ecommerceData.slice(0, 100)} title="E-commerce Data" maxRows={5} />
      </div>
    </div>
  );
}
