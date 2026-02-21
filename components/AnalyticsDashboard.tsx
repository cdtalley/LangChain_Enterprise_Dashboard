"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import BarChartCard from "@/components/charts/BarChartCard";
import ChartCard from "@/components/charts/ChartCard";
import { DollarSign, ShoppingCart, TrendingUp } from "lucide-react";
import { CHART_COLORS } from "@/lib/utils";

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
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-[var(--foreground)] mb-1">Analytics Dashboard</h1>
          <p className="text-[var(--muted)]">Interactive data visualization and insights</p>
        </div>
        <div className="flex gap-2">
          {(["ecommerce", "finance", "marketing"] as const).map((key) => (
            <button
              key={key}
              onClick={() => setSelectedDataset(key)}
              className={`px-4 py-2.5 rounded-xl font-medium text-sm transition-all ${
                selectedDataset === key
                  ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/25"
                  : "bg-white border border-[var(--border)] text-[var(--muted)] hover:bg-slate-50 hover:text-[var(--foreground)]"
              }`}
            >
              {key === "ecommerce" ? "E-commerce" : key === "finance" ? "Finance" : "Marketing"}
            </button>
          ))}
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
            <BarChartCard
              title="Revenue by Product"
              subtitle="Top products by revenue"
              data={productChartData}
              dataKey="revenue"
              nameKey="product"
              color={0}
              formatValue={(v) => `$${v.toLocaleString()}`}
            />
            <ChartCard title="Revenue by Region" subtitle="Share by region">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={regionChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ region, percent }) => `${region} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={90}
                    innerRadius={40}
                    stroke="none"
                    dataKey="revenue"
                  >
                    {regionChartData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      borderRadius: "12px",
                      border: "1px solid var(--border)",
                      boxShadow: "var(--shadow-lg)",
                      padding: "12px 16px",
                    }}
                    formatter={(value: number) => [`$${value.toLocaleString()}`, "Revenue"]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </ChartCard>
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

          <BarChartCard
            title="Transactions by Category"
            subtitle="Volume by category"
            data={financeChartData}
            dataKey="amount"
            nameKey="category"
            color={0}
            height={400}
            formatValue={(v) => `$${v.toLocaleString()}`}
          />

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

          <BarChartCard
            title="ROAS by Channel"
            subtitle="Return on ad spend"
            data={marketingChartData}
            dataKey="roas"
            nameKey="channel"
            color={4}
            height={400}
            formatValue={(v) => `${v.toFixed(2)}x`}
          />

          <DataTable data={marketingData} title="Marketing Data" maxRows={10} />
        </motion.div>
      )}
    </div>
  );
}
