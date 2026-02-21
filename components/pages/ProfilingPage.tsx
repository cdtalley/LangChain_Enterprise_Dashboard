"use client";

import { Activity, Database, TrendingUp } from "lucide-react";
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

export default function ProfilingPage() {
  const { financeData, ecommerceData } = useData();

  // Data quality metrics
  const financeQuality = {
    completeness: 100,
    uniqueness: 99.8,
    validity: 98.5,
    consistency: 97.2,
  };

  const ecommerceQuality = {
    completeness: 99.5,
    uniqueness: 99.9,
    validity: 99.1,
    consistency: 98.8,
  };

  const qualityData = [
    { metric: "Completeness", finance: financeQuality.completeness, ecommerce: ecommerceQuality.completeness },
    { metric: "Uniqueness", finance: financeQuality.uniqueness, ecommerce: ecommerceQuality.uniqueness },
    { metric: "Validity", finance: financeQuality.validity, ecommerce: ecommerceQuality.validity },
    { metric: "Consistency", finance: financeQuality.consistency, ecommerce: ecommerceQuality.consistency },
  ];

  return (
    <div className="space-y-6" data-tour="profiling">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Data Profiling</h1>
        <p className="text-gray-600">Data quality analysis and profiling</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Finance Completeness"
          value={`${financeQuality.completeness}%`}
          icon={Database}
          gradient="from-pink-500 to-rose-500"
        />
        <MetricCard
          title="Finance Validity"
          value={`${financeQuality.validity}%`}
          icon={Activity}
        />
        <MetricCard
          title="E-commerce Completeness"
          value={`${ecommerceQuality.completeness}%`}
          icon={Database}
          gradient="from-blue-500 to-cyan-500"
        />
        <MetricCard
          title="E-commerce Validity"
          value={`${ecommerceQuality.validity}%`}
          icon={TrendingUp}
        />
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-bold mb-4">Data Quality Comparison</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={qualityData}>
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
        <DataTable data={financeData.slice(0, 50)} title="Finance Data Profile" maxRows={5} />
        <DataTable data={ecommerceData.slice(0, 50)} title="E-commerce Data Profile" maxRows={5} />
      </div>
    </div>
  );
}
