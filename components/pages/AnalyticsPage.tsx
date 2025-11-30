"use client";

import { useData } from "@/lib/DataContext";
import AnalyticsDashboard from "@/components/AnalyticsDashboard";

export default function AnalyticsPage() {
  return <div data-tour="analytics"><AnalyticsDashboard /></div>;
}

