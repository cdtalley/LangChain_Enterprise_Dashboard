"use client";

import { motion } from "framer-motion";
import { Database, TrendingUp, FileText, Download } from "lucide-react";
import DataGenerator from "@/components/DataGenerator";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";

export default function DatasetsPage() {
  const { financeData, ecommerceData, marketingData, hrData, healthcareData, isLoading } = useData();

  const datasets = [
    {
      name: "Finance",
      records: financeData.length,
      description: "Financial transactions with fraud detection",
      icon: TrendingUp,
      gradient: "from-pink-500 to-rose-500",
      data: financeData,
    },
    {
      name: "E-commerce",
      records: ecommerceData.length,
      description: "Online retail orders and customer data",
      icon: FileText,
      gradient: "from-blue-500 to-cyan-500",
      data: ecommerceData,
    },
    {
      name: "Marketing",
      records: marketingData.length,
      description: "Campaign performance and ROI metrics",
      icon: TrendingUp,
      gradient: "from-green-500 to-emerald-500",
      data: marketingData,
    },
    {
      name: "HR",
      records: hrData.length,
      description: "Employee data and performance metrics",
      icon: Database,
      gradient: "from-purple-500 to-indigo-500",
      data: hrData,
    },
    {
      name: "Healthcare",
      records: healthcareData.length,
      description: "Patient records and medical data",
      icon: Database,
      gradient: "from-teal-500 to-blue-500",
      data: healthcareData,
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const totalRecords = datasets.reduce((sum, d) => sum + d.records, 0);

  return (
    <div className="space-y-6" data-tour="datasets">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">📚 Datasets & Models</h1>
        <p className="text-gray-600">Pre-loaded datasets with automated model training and evaluation</p>
      </div>

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Total Datasets"
          value={datasets.length}
          icon={Database}
          gradient="from-purple-500 to-indigo-500"
        />
        <MetricCard
          title="Total Records"
          value={totalRecords.toLocaleString()}
          icon={FileText}
        />
        <MetricCard
          title="Available Models"
          value="12"
          icon={TrendingUp}
          gradient="from-green-500 to-emerald-500"
        />
        <MetricCard
          title="Training Status"
          value="Ready"
          icon={Download}
          gradient="from-blue-500 to-cyan-500"
        />
      </div>

      {/* Dataset Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {datasets.map((dataset, idx) => {
          const Icon = dataset.icon;
          return (
            <motion.div
              key={dataset.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className={`bg-gradient-to-br ${dataset.gradient} text-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all`}
            >
              <div className="flex items-center justify-between mb-4">
                <Icon className="w-8 h-8" />
                <span className="px-3 py-1 bg-white bg-opacity-20 rounded-full text-sm font-semibold">
                  {dataset.records.toLocaleString()} records
                </span>
              </div>
              <h3 className="text-xl font-bold mb-2">{dataset.name}</h3>
              <p className="text-sm opacity-90 mb-4">{dataset.description}</p>
              <div className="flex gap-2">
                <button className="flex-1 px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm font-semibold transition-all">
                  View Data
                </button>
                <button className="px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm font-semibold transition-all">
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Data Generator */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Generate Custom Dataset</h2>
        <DataGenerator />
      </div>

      {/* Quick Data Previews */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DataTable data={financeData.slice(0, 100)} title="Finance Dataset Preview" maxRows={5} />
        <DataTable data={ecommerceData.slice(0, 100)} title="E-commerce Dataset Preview" maxRows={5} />
      </div>
    </div>
  );
}
