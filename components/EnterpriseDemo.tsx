"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import {
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
import { TrendingUp, DollarSign, Users, Activity, RefreshCw } from "lucide-react";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

export default function EnterpriseDemo() {
  const { financeData, ecommerceData, marketingData, hrData, healthcareData, isLoading, refreshData } = useData();
  const [activeDataset, setActiveDataset] = useState<string>("finance");

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const getFinanceMetrics = () => {
    if (financeData.length === 0) return null;
    const totalVolume = financeData.reduce((sum, r) => sum + r.amount, 0);
    const fraudCount = financeData.filter(r => r.is_fraud === 1).length;
    const avgAmount = totalVolume / financeData.length;
    return { totalVolume, fraudCount, avgAmount, total: financeData.length };
  };

  const getEcommerceMetrics = () => {
    if (ecommerceData.length === 0) return null;
    const totalRevenue = ecommerceData.reduce((sum, r) => sum + r.total_amount, 0);
    const avgOrder = totalRevenue / ecommerceData.length;
    const returnRate = (ecommerceData.filter(r => r.returned === 1).length / ecommerceData.length) * 100;
    return { totalRevenue, avgOrder, returnRate, total: ecommerceData.length };
  };

  const getMarketingMetrics = () => {
    if (marketingData.length === 0) return null;
    const totalSpend = marketingData.reduce((sum, r) => sum + r.spend, 0);
    const totalRevenue = marketingData.reduce((sum, r) => sum + r.revenue, 0);
    const avgROAS = marketingData.reduce((sum, r) => sum + r.roas, 0) / marketingData.length;
    return { totalSpend, totalRevenue, avgROAS, total: marketingData.length };
  };

  const getHRMetrics = () => {
    if (hrData.length === 0) return null;
    const avgSalary = hrData.reduce((sum, r) => sum + r.salary, 0) / hrData.length;
    const avgPerformance = hrData.reduce((sum, r) => sum + r.performance_score, 0) / hrData.length;
    const turnoverRate = (hrData.filter(r => r.left_company === 1).length / hrData.length) * 100;
    return { avgSalary, avgPerformance, turnoverRate, total: hrData.length };
  };

  const getHealthcareMetrics = () => {
    if (healthcareData.length === 0) return null;
    const avgAge = healthcareData.reduce((sum, r) => sum + r.age, 0) / healthcareData.length;
    const readmitRate = (healthcareData.filter(r => r.readmission_risk === 1).length / healthcareData.length) * 100;
    const totalCost = healthcareData.reduce((sum, r) => sum + r.cost, 0);
    return { avgAge, readmitRate, totalCost, total: healthcareData.length };
  };

  const financeMetrics = getFinanceMetrics();
  const ecommerceMetrics = getEcommerceMetrics();
  const marketingMetrics = getMarketingMetrics();
  const hrMetrics = getHRMetrics();
  const healthcareMetrics = getHealthcareMetrics();

  // Prepare chart data
  const financeByCategory = financeData.reduce((acc: any, r) => {
    acc[r.category] = (acc[r.category] || 0) + r.amount;
    return acc;
  }, {});

  const financeChartData = Object.entries(financeByCategory)
    .map(([category, amount]) => ({ category, amount: amount as number }))
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 7);

  const financeFraudByCategory = financeData.reduce((acc: any, r) => {
    if (!acc[r.category]) acc[r.category] = { total: 0, fraud: 0 };
    acc[r.category].total += 1;
    if (r.is_fraud === 1) acc[r.category].fraud += 1;
    return acc;
  }, {});

  const fraudChartData = Object.entries(financeFraudByCategory).map(([category, data]: [string, any]) => ({
    category,
    fraudRate: (data.fraud / data.total) * 100,
  }));

  // Time series data
  const financeTimeSeries = financeData.slice(0, 100).map((r, idx) => ({
    date: new Date(r.date).toLocaleDateString(),
    amount: r.amount,
    index: idx,
  }));

  const ecommerceByProduct = ecommerceData.reduce((acc: any, r) => {
    acc[r.product] = (acc[r.product] || 0) + r.total_amount;
    return acc;
  }, {});

  const ecommerceChartData = Object.entries(ecommerceByProduct)
    .map(([product, revenue]) => ({ product, revenue: revenue as number }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5);

  const ecommerceByRegion = ecommerceData.reduce((acc: any, r) => {
    acc[r.region] = (acc[r.region] || 0) + r.total_amount;
    return acc;
  }, {});

  const regionChartData = Object.entries(ecommerceByRegion).map(([region, revenue]) => ({
    region,
    revenue: revenue as number,
  }));

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
    spend: data.spend,
    revenue: data.revenue,
  }));

  const hrByDepartment = hrData.reduce((acc: any, r) => {
    if (!acc[r.department]) {
      acc[r.department] = { count: 0, totalSalary: 0 };
    }
    acc[r.department].count += 1;
    acc[r.department].totalSalary += r.salary;
    return acc;
  }, {});

  const hrChartData = Object.entries(hrByDepartment).map(([department, data]: [string, any]) => ({
    department,
    avgSalary: data.totalSalary / data.count,
    count: data.count,
  }));

  const datasets = [
    { id: "finance", label: "💳 Finance", color: "from-pink-500 to-rose-500", data: financeData },
    { id: "ecommerce", label: "🛒 E-commerce", color: "from-blue-500 to-cyan-500", data: ecommerceData },
    { id: "marketing", label: "📢 Marketing", color: "from-green-500 to-emerald-500", data: marketingData },
    { id: "hr", label: "👥 HR", color: "from-purple-500 to-indigo-500", data: hrData },
    { id: "healthcare", label: "🏥 Healthcare", color: "from-teal-500 to-blue-500", data: healthcareData },
  ];

  return (
    <div className="space-y-6" data-tour="demo">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🎯 Enterprise Demo Showcase</h1>
          <p className="text-gray-600">Real-world datasets with stunning visualizations and actionable insights</p>
        </div>
        <button
          onClick={refreshData}
          className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh Data
        </button>
      </div>

      {/* Dataset Selector */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {datasets.map((dataset) => (
          <button
            key={dataset.id}
            onClick={() => setActiveDataset(dataset.id)}
            className={`p-4 rounded-xl transition-all ${
              activeDataset === dataset.id
                ? `bg-gradient-to-br ${dataset.color} text-white shadow-lg scale-105`
                : "bg-white text-gray-700 shadow hover:shadow-md"
            }`}
          >
            <div className="font-semibold">{dataset.label}</div>
            <div className="text-xs mt-1 opacity-75">
              {dataset.data.length.toLocaleString()} records
            </div>
          </button>
        ))}
      </div>

      {/* Finance Dashboard */}
      {activeDataset === "finance" && financeMetrics && (
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
              title="Transactions"
              value={financeMetrics.total.toLocaleString()}
              subtitle="Total count"
            />
            <MetricCard
              title="Avg Transaction"
              value={`$${financeMetrics.avgAmount.toFixed(2)}`}
            />
            <MetricCard
              title="Fraud Cases"
              value={financeMetrics.fraudCount}
              subtitle={`${((financeMetrics.fraudCount / financeMetrics.total) * 100).toFixed(2)}%`}
              trend="down"
              gradient="from-red-500 to-orange-500"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Transactions by Category</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={financeChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="amount" fill="#667eea" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Fraud Rate by Category (%)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={fraudChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="fraudRate" fill="#f5576c" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-bold mb-4">Transaction Timeline</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={financeTimeSeries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="index" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="amount" stroke="#667eea" fill="#667eea" fillOpacity={0.6} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <DataTable data={financeData} title="Finance Data" maxRows={10} />
        </motion.div>
      )}

      {/* E-commerce Dashboard */}
      {activeDataset === "ecommerce" && ecommerceMetrics && (
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
              gradient="from-blue-500 to-cyan-500"
            />
            <MetricCard
              title="Total Orders"
              value={ecommerceMetrics.total.toLocaleString()}
            />
            <MetricCard
              title="Avg Order Value"
              value={`$${ecommerceMetrics.avgOrder.toFixed(2)}`}
            />
            <MetricCard
              title="Return Rate"
              value={`${ecommerceMetrics.returnRate.toFixed(2)}%`}
              trend="down"
              gradient="from-orange-500 to-red-500"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Top Products by Revenue</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={ecommerceChartData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="product" type="category" width={100} />
                  <Tooltip />
                  <Bar dataKey="revenue" fill="#4facfe" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-bold mb-4">Revenue by Region</h3>
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie
                    data={regionChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ region, percent }) => `${region} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
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

      {/* Marketing Dashboard */}
      {activeDataset === "marketing" && marketingMetrics && (
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
              value={marketingMetrics.total.toLocaleString()}
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

      {/* HR Dashboard */}
      {activeDataset === "hr" && hrMetrics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard
              title="Total Employees"
              value={hrMetrics.total.toLocaleString()}
              icon={Users}
              gradient="from-purple-500 to-indigo-500"
            />
            <MetricCard
              title="Avg Salary"
              value={`$${(hrMetrics.avgSalary / 1000).toFixed(0)}K`}
            />
            <MetricCard
              title="Avg Performance"
              value={hrMetrics.avgPerformance.toFixed(1)}
              subtitle="Out of 100"
            />
            <MetricCard
              title="Turnover Rate"
              value={`${hrMetrics.turnoverRate.toFixed(1)}%`}
              trend="down"
              gradient="from-red-500 to-pink-500"
            />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-bold mb-4">Average Salary by Department</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={hrChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="department" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="avgSalary" fill="#764ba2" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <DataTable data={hrData} title="HR Data" maxRows={10} />
        </motion.div>
      )}

      {/* Healthcare Dashboard */}
      {activeDataset === "healthcare" && healthcareMetrics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard
              title="Total Patients"
              value={healthcareMetrics.total.toLocaleString()}
              icon={Activity}
              gradient="from-teal-500 to-blue-500"
            />
            <MetricCard
              title="Avg Age"
              value={healthcareMetrics.avgAge.toFixed(1)}
            />
            <MetricCard
              title="Readmission Risk"
              value={`${healthcareMetrics.readmitRate.toFixed(1)}%`}
              trend="down"
            />
            <MetricCard
              title="Total Cost"
              value={`$${(healthcareMetrics.totalCost / 1000).toFixed(1)}K`}
            />
          </div>

          <DataTable data={healthcareData} title="Healthcare Data" maxRows={10} />
        </motion.div>
      )}
    </div>
  );
}
