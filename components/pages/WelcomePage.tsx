"use client";

import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import HeroSection from "@/components/HeroSection";
import StatsGrid from "@/components/StatsGrid";
import FeatureCards from "@/components/FeatureCards";
import DashboardTabs from "@/components/DashboardTabs";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import BarChartCard from "@/components/charts/BarChartCard";
import TimeSeriesChartCard from "@/components/charts/TimeSeriesChartCard";
import { DollarSign, ShoppingCart, TrendingUp, Users, Briefcase, Target } from "lucide-react";

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

  // Daily aggregates for executive trend
  const dailyFinance = financeData.slice(0, 500).reduce((acc: Record<string, { date: string; total: number; count: number }>, r) => {
    const date = new Date(r.date).toLocaleDateString("en-US", { month: "short", day: "numeric" });
    if (!acc[date]) acc[date] = { date, total: 0, count: 0 };
    acc[date].total += r.amount;
    acc[date].count += 1;
    return acc;
  }, {});
  const executiveTrendData = Object.values(dailyFinance)
    .map((d) => ({ date: d.date, amount: Math.round(d.total / d.count) }))
    .slice(-14);

  return (
    <div className="space-y-10">
      <HeroSection />
      <div data-tour="welcome-stats">
        <StatsGrid />
      </div>

      {/* Executive Summary */}
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="rounded-2xl border border-[var(--border)] bg-white/80 backdrop-blur-sm p-6 md:p-8 shadow-[var(--shadow-md)]"
      >
        <div className="flex flex-wrap items-center gap-3 mb-6">
          <Briefcase className="w-6 h-6 text-[var(--primary)]" />
          <h2 className="text-2xl font-bold tracking-tight text-[var(--foreground)]">
            Executive Summary
          </h2>
          <span className="text-xs font-medium text-[var(--muted)] bg-slate-100 px-2.5 py-1 rounded-full">
            Live data
          </span>
        </div>
        <p className="text-[var(--muted)] max-w-2xl mb-6">
          Key performance indicators and trends across finance, e‑commerce, marketing, and HR. Use the Analytics and Time Series views for deeper analysis.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <MetricCard
            title="Finance"
            value={`$${(financeMetrics.totalVolume / 1000).toFixed(1)}K`}
            subtitle={`${financeMetrics.totalTransactions.toLocaleString()} transactions`}
            icon={DollarSign}
            gradient="from-indigo-500 to-violet-500"
          />
          <MetricCard
            title="E-commerce"
            value={`$${(ecommerceMetrics.totalRevenue / 1000).toFixed(1)}K`}
            subtitle={`${ecommerceMetrics.totalOrders.toLocaleString()} orders`}
            icon={ShoppingCart}
            gradient="from-cyan-500 to-blue-500"
          />
          <MetricCard
            title="Marketing"
            value={`${marketingMetrics.avgROAS.toFixed(2)}x`}
            subtitle={`${marketingMetrics.totalCampaigns.toLocaleString()} campaigns`}
            icon={TrendingUp}
            gradient="from-emerald-500 to-teal-500"
          />
          <MetricCard
            title="HR"
            value={hrMetrics.totalEmployees.toLocaleString()}
            subtitle={`$${(hrMetrics.avgSalary / 1000).toFixed(0)}K avg salary`}
            icon={Users}
            gradient="from-violet-500 to-purple-500"
          />
        </div>
        {executiveTrendData.length > 0 && (
          <div className="mt-6 pt-6 border-t border-[var(--border)]">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-[var(--primary)]" />
              <h3 className="text-sm font-semibold text-[var(--foreground)]">Finance — Avg transaction (last 14 periods)</h3>
            </div>
            <TimeSeriesChartCard
              title=""
              subtitle=""
              data={executiveTrendData}
              valueKey="amount"
              xKey="date"
              variant="line"
              colorIndex={0}
              height={200}
              formatValue={(v) => `$${v.toLocaleString()}`}
            />
          </div>
        )}
      </motion.section>

      {/* Live Dataset Showcase */}
      <div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold tracking-tight text-[var(--foreground)] mb-1">
            Live Dataset Showcase
          </h2>
          <p className="text-[var(--muted)]">Real-time data processing and analytics across multiple domains</p>
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

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <BarChartCard
            title="Top Finance Categories"
            subtitle="Volume by category"
            data={financeChartData}
            dataKey="amount"
            nameKey="category"
            color={0}
            formatValue={(v) => `$${v.toLocaleString()}`}
          />
          <BarChartCard
            title="Top E-commerce Products"
            subtitle="Revenue by product"
            data={ecommerceChartData}
            dataKey="revenue"
            nameKey="product"
            color={2}
            formatValue={(v) => `$${v.toLocaleString()}`}
          />
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
