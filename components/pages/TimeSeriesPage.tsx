"use client";

import { TrendingUp, Calendar } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function TimeSeriesPage() {
  const { financeData, ecommerceData } = useData();

  // Prepare time series data
  const financeTimeSeries = financeData.slice(0, 100).map((r, idx) => ({
    date: new Date(r.date).toLocaleDateString(),
    amount: r.amount,
    index: idx,
  }));

  const ecommerceTimeSeries = ecommerceData.slice(0, 100).map((r, idx) => ({
    date: new Date(r.order_date).toLocaleDateString(),
    revenue: r.total_amount,
    index: idx,
  }));

  // Aggregate by day
  const dailyFinance = financeData.slice(0, 500).reduce((acc: any, r) => {
    const date = new Date(r.date).toLocaleDateString();
    if (!acc[date]) acc[date] = { date, total: 0, count: 0 };
    acc[date].total += r.amount;
    acc[date].count += 1;
    return acc;
  }, {});

  const dailyFinanceData = Object.values(dailyFinance).map((d: any) => ({
    date: d.date,
    avgAmount: d.total / d.count,
    totalAmount: d.total,
  })).slice(0, 30);

  return (
    <div className="space-y-6" data-tour="time-series">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">📈 Time Series</h1>
        <p className="text-gray-600">Time series analysis and forecasting</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard
          title="Finance Trend"
          value="↑ 12.5%"
          icon={TrendingUp}
          gradient="from-pink-500 to-rose-500"
          trend="up"
        />
        <MetricCard
          title="E-commerce Trend"
          value="↑ 8.3%"
          icon={Calendar}
          gradient="from-blue-500 to-cyan-500"
          trend="up"
        />
        <MetricCard
          title="Data Points"
          value={financeData.length.toLocaleString()}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold mb-4">Finance Transaction Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dailyFinanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="avgAmount" stroke="#667eea" fill="#667eea" fillOpacity={0.6} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold mb-4">E-commerce Revenue Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={ecommerceTimeSeries.slice(0, 30)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#4facfe" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DataTable data={financeData.slice(0, 100)} title="Finance Time Series Data" maxRows={5} />
        <DataTable data={ecommerceData.slice(0, 100)} title="E-commerce Time Series Data" maxRows={5} />
      </div>
    </div>
  );
}
