"use client";

import { TrendingUp, Calendar } from "lucide-react";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import TimeSeriesChartCard from "@/components/charts/TimeSeriesChartCard";

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
        <h1 className="text-3xl font-bold tracking-tight text-[var(--foreground)] mb-1">Time Series</h1>
        <p className="text-[var(--muted)]">Time series analysis and forecasting</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard
          title="Finance Trend"
          value="↑ 12.5%"
          icon={TrendingUp}
          gradient="from-indigo-500 to-violet-500"
          trend="up"
          trendValue="12.5%"
        />
        <MetricCard
          title="E-commerce Trend"
          value="↑ 8.3%"
          icon={Calendar}
          gradient="from-cyan-500 to-blue-500"
          trend="up"
          trendValue="8.3%"
        />
        <MetricCard
          title="Data Points"
          value={financeData.length.toLocaleString()}
          gradient="from-violet-500 to-purple-500"
          trendValue="—"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TimeSeriesChartCard
          title="Finance Transaction Timeline"
          subtitle="Daily average transaction amount"
          data={dailyFinanceData}
          valueKey="avgAmount"
          xKey="date"
          variant="area"
          colorIndex={0}
          formatValue={(v) => `$${v.toLocaleString()}`}
        />
        <TimeSeriesChartCard
          title="E-commerce Revenue Timeline"
          subtitle="Revenue over time"
          data={ecommerceTimeSeries.slice(0, 30)}
          valueKey="revenue"
          xKey="date"
          variant="line"
          colorIndex={2}
          formatValue={(v) => `$${v.toLocaleString()}`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DataTable data={financeData.slice(0, 100)} title="Finance Time Series Data" maxRows={5} />
        <DataTable data={ecommerceData.slice(0, 100)} title="E-commerce Time Series Data" maxRows={5} />
      </div>
    </div>
  );
}
