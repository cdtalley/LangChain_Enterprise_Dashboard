"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import { DollarSign, ShoppingCart, TrendingUp, Activity } from "lucide-react";

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

export default function AnalyticsDashboard() {
  const { ecommerceData, financeData, marketingData, isLoading } = useData();
  const [selectedDataset, setSelectedDataset] = useState<"ecommerce" | "finance" | "marketing">("ecommerce");

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const data = selectedDataset === "ecommerce" ? ecommerceData : selectedDataset === "finance" ? financeData : marketingData;

  // E-commerce analytics
  const ecommerceMetrics = {
    totalRevenue: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0),
    avgOrder: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0) / ecommerceData.length,
    returnRate: (ecommerceData.filter(r => r.returned === 1).length / ecommerceData.length) * 100,
    totalOrders: ecommerceData.length,
  };

  const productRevenue = ecommerceData.reduce((acc: any, r) => {
    acc[r.product] = (acc[r.product] || 0) + r.total_amount;
    return acc;
  }, {});

  const productChartData = Object.entries(productRevenue)
    .map(([product, revenue]) => ({ product, revenue: revenue as number }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 8);

  const regionData = ecommerceData.reduce((acc: any, r) => {
    acc[r.region] = (acc[r.region] || 0) + r.total_amount;
    return acc;
  }, {});

  const regionChartData = Object.entries(regionData).map(([region, revenue]) => ({
    region,
    revenue: revenue as number,
  }));

  // Finance analytics
  const financeMetrics = {
    totalVolume: financeData.reduce((sum, r) => sum + r.amount, 0),
    avgAmount: financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length,
    fraudCount: financeData.filter(r => r.is_fraud === 1).length,
    totalTransactions: financeData.length,
  };

  const financeByCategory = financeData.reduce((acc: any, r) => {
    acc[r.category] = (acc[r.category] || 0) + r.amount;
    return acc;
  }, {});

  const financeChartData = Object.entries(financeByCategory)
    .map(([category, amount]) => ({ category, amount: amount as number }))
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 7);

  // Marketing analytics
  const marketingMetrics = {
    totalSpend: marketingData.reduce((sum, r) => sum + r.spend, 0),
    totalRevenue: marketingData.reduce((sum, r) => sum + r.revenue, 0),
    avgROAS: marketingData.reduce((sum, r) => sum + r.roas, 0) / marketingData.length,
    totalCampaigns: marketingData.length,
  };

  const marketingByChannel = marketingData.reduce((acc: any, r) => {
    if (!acc[r.channel]) {
      acc[r.channel] = { spend: 0, revenue: 0 };
    }
    acc[r.channel].spend += r.spend;
    acc[r.channel].revenue += r.revenue;
    return acc;
  }, {});

  const marketingChartData = Object.entries(marketingByChannel).map(([channel, data]: [string, any]) => ({
    channel,
    roas: data.revenue / data.spend,
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">📈 Analytics Dashboard</h1>
          <p className="text-gray-600">Interactive data visualization and insights</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedDataset("ecommerce")}
            className={`px-4 py-2 rounded-lg transition-all ${
              selectedDataset === "ecommerce"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            E-commerce
          </button>
          <button
            onClick={() => setSelectedDataset("finance")}
            className={`px-4 py-2 rounded-lg transition-all ${
              selectedDataset === "finance"
                ? "bg-pink-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            Finance
          </button>
          <button
            onClick={() => setSelectedDataset("marketing")}
            className={`px-4 py-2 rounded-lg transition-all ${
              selectedDataset === "marketing"
                ? "bg-green-600 text-white"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            Marketing
          </button>
        </div>
      </div>

      {/* E-commerce View */}
      {selectedDataset === "ecommerce" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard
              title="Total Revenue"
              value={`$${(ecommerceMetrics.totalRevenue / 1000).toFixed(1)}K`}
              icon={DollarSign}
              gradient="from-purple-500 to-pink-500"
            />
            <MetricCard
              title="Avg Order Value"
              value={`$${ecommerceMetrics.avgOrder.toFixed(2)}`}
            />
            <MetricCard
              title="Return Rate"
              value={`${ecommerceMetrics.returnRate.toFixed(2)}%`}
              trend="down"
            />
            <MetricCard
              title="Total Orders"
              value={ecommerceMetrics.totalOrders.toLocaleString()}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Revenue by Product</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={productChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="product" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="revenue" fill="#667eea" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Revenue by Region</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={regionChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ region, percent }) => `${region} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="revenue"
                  >
                    {regionChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <DataTable data={ecommerceData} title="E-commerce Data" maxRows={10} />
        </motion.div>
      )}

      {/* Finance View */}
      {selectedDataset === "finance" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard
              title="Total Volume"
              value={`$${(financeMetrics.totalVolume / 1000).toFixed(1)}K`}
              icon={DollarSign}
              gradient="from-pink-500 to-rose-500"
            />
            <MetricCard
              title="Avg Transaction"
              value={`$${financeMetrics.avgAmount.toFixed(2)}`}
            />
            <MetricCard
              title="Fraud Cases"
              value={financeMetrics.fraudCount}
              trend="down"
            />
            <MetricCard
              title="Transactions"
              value={financeMetrics.totalTransactions.toLocaleString()}
            />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-bold mb-4">Transactions by Category</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={financeChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="amount" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <DataTable data={financeData} title="Finance Data" maxRows={10} />
        </motion.div>
      )}

      {/* Marketing View */}
      {selectedDataset === "marketing" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard
              title="Avg ROAS"
              value={`${marketingMetrics.avgROAS.toFixed(2)}x`}
              icon={TrendingUp}
              gradient="from-green-500 to-emerald-500"
            />
            <MetricCard
              title="Total Spend"
              value={`$${(marketingMetrics.totalSpend / 1000).toFixed(1)}K`}
            />
            <MetricCard
              title="Total Revenue"
              value={`$${(marketingMetrics.totalRevenue / 1000).toFixed(1)}K`}
            />
            <MetricCard
              title="Campaigns"
              value={marketingMetrics.totalCampaigns.toLocaleString()}
            />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-bold mb-4">ROAS by Channel</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={marketingChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="channel" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="roas" fill="#43e97b" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <DataTable data={marketingData} title="Marketing Data" maxRows={10} />
        </motion.div>
      )}
    </div>
  );
}
