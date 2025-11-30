"use client";

import { Eye, AlertTriangle, TrendingUp, Activity } from "lucide-react";
import { motion } from "framer-motion";
import MetricCard from "@/components/MetricCard";
import { useData } from "@/lib/DataContext";
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

export default function MonitoringPage() {
  const { financeData, ecommerceData } = useData();

  // Simulate monitoring metrics over time
  const performanceData = Array.from({ length: 30 }, (_, i) => ({
    day: i + 1,
    accuracy: 95 + Math.random() * 3,
    latency: 1.0 + Math.random() * 0.5,
    throughput: 100 + Math.random() * 50,
  }));

  const fraudRate = (financeData.filter(r => r.is_fraud === 1).length / financeData.length) * 100;
  const returnRate = (ecommerceData.filter(r => r.returned === 1).length / ecommerceData.length) * 100;

  return (
    <div className="space-y-6" data-tour="monitoring">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🔍 Model Monitoring</h1>
        <p className="text-gray-600">Performance tracking, drift detection, and anomaly detection</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Model Accuracy"
          value="99.2%"
          icon={TrendingUp}
          gradient="from-green-500 to-emerald-500"
          trend="up"
          trendValue="+0.5%"
        />
        <MetricCard
          title="Avg Latency"
          value="1.2s"
          icon={Activity}
          trend="down"
          trendValue="-0.3s"
        />
        <MetricCard
          title="Fraud Rate"
          value={`${fraudRate.toFixed(2)}%`}
          icon={AlertTriangle}
          gradient="from-orange-500 to-red-500"
        />
        <MetricCard
          title="Return Rate"
          value={`${returnRate.toFixed(2)}%`}
          icon={Eye}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold mb-4">Model Accuracy Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="accuracy" stroke="#43e97b" fill="#43e97b" fillOpacity={0.6} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-lg font-bold mb-4">Latency Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="latency" stroke="#667eea" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-lg font-bold mb-4">Alerts & Anomalies</h3>
        <div className="space-y-2">
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm font-semibold">All systems operational</span>
            </div>
          </div>
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-sm font-semibold">Latency spike detected at 2:34 PM</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
