"use client";

import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import HeroSection from "@/components/HeroSection";
import StatsGrid from "@/components/StatsGrid";
import FeatureCards from "@/components/FeatureCards";
import DashboardTabs from "@/components/DashboardTabs";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import { DollarSign, ShoppingCart, TrendingUp, Users } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

export default function WelcomePage() {
  const { financeData, ecommerceData, marketingData, hrData, isLoading } = useData();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  // Calculate metrics
  const financeMetrics = {
    totalVolume: financeData.reduce((sum, r) => sum + r.amount, 0),
    totalTransactions: financeData.length,
    fraudCount: financeData.filter((r) => r.is_fraud === 1).length,
    avgAmount: financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length,
  };

  const ecommerceMetrics = {
    totalRevenue: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0),
    totalOrders: ecommerceData.length,
    avgOrder: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0) / ecommerceData.length,
  };

  const marketingMetrics = {
    avgROAS: marketingData.reduce((sum, r) => sum + r.roas, 0) / marketingData.length,
    totalCampaigns: marketingData.length,
  };

  const hrMetrics = {
    totalEmployees: hrData.length,
    avgSalary: hrData.reduce((sum, r) => sum + r.salary, 0) / hrData.length,
  };

  // Prepare chart data
  const financeByCategory = financeData.reduce((acc: any, r) => {
    acc[r.category] = (acc[r.category] || 0) + r.amount;
    return acc;
  }, {});

  const financeChartData = Object.entries(financeByCategory)
    .map(([category, amount]) => ({ category, amount: amount as number }))
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 5);

  const ecommerceByProduct = ecommerceData.reduce((acc: any, r) => {
    acc[r.product] = (acc[r.product] || 0) + r.total_amount;
    return acc;
  }, {});

  const ecommerceChartData = Object.entries(ecommerceByProduct)
    .map(([product, revenue]) => ({ product, revenue: revenue as number }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5);

  return (
    <div className="space-y-8">
      <HeroSection />
      <div data-tour="welcome-stats">
        <StatsGrid />
      </div>

      {/* Live Dataset Showcase */}
      <div>
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Live Dataset Showcase</h2>
          <p className="text-gray-600">Real-time data processing and analytics across multiple domains</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <MetricCard
            title="Finance"
            value={`$${(financeMetrics.totalVolume / 1000).toFixed(1)}K`}
            subtitle={`${financeMetrics.totalTransactions.toLocaleString()} transactions`}
            icon={DollarSign}
            gradient="from-pink-500 to-rose-500"
          />
          <MetricCard
            title="E-commerce"
            value={`$${(ecommerceMetrics.totalRevenue / 1000).toFixed(1)}K`}
            subtitle={`${ecommerceMetrics.totalOrders.toLocaleString()} orders`}
            icon={ShoppingCart}
            gradient="from-blue-500 to-cyan-500"
          />
          <MetricCard
            title="Marketing"
            value={`${marketingMetrics.avgROAS.toFixed(2)}x`}
            subtitle={`${marketingMetrics.totalCampaigns.toLocaleString()} campaigns`}
            icon={TrendingUp}
            gradient="from-green-500 to-emerald-500"
          />
          <MetricCard
            title="HR"
            value={hrMetrics.totalEmployees.toLocaleString()}
            subtitle={`$${(hrMetrics.avgSalary / 1000).toFixed(0)}K avg salary`}
            icon={Users}
            gradient="from-purple-500 to-indigo-500"
          />
        </div>

        {/* Quick Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold mb-4">Top Finance Categories</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={financeChartData}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="amount" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold mb-4">Top E-commerce Products</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ecommerceChartData}>
                <XAxis dataKey="product" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="revenue" fill="#4facfe" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Data Preview Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DataTable
            data={financeData.slice(0, 100)}
            title="Finance Data Preview"
            maxRows={5}
          />
          <DataTable
            data={ecommerceData.slice(0, 100)}
            title="E-commerce Data Preview"
            maxRows={5}
          />
        </div>
      </div>

      <FeatureCards />
      <DashboardTabs />
    </div>
  );
}
