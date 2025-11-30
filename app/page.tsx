"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Sidebar, { navItems } from "@/components/Sidebar";
import WelcomePage from "@/components/pages/WelcomePage";
import MultiAgentPage from "@/components/pages/MultiAgentPage";
import RAGPage from "@/components/pages/RAGPage";
import ToolsPage from "@/components/pages/ToolsPage";
import AnalyticsPage from "@/components/pages/AnalyticsPage";
import DemoPage from "@/components/pages/DemoPage";
import RegistryPage from "@/components/pages/RegistryPage";
import ABTestingPage from "@/components/pages/ABTestingPage";
import ExperimentsPage from "@/components/pages/ExperimentsPage";
import MonitoringPage from "@/components/pages/MonitoringPage";
import FineTuningPage from "@/components/pages/FineTuningPage";
import DatasetsPage from "@/components/pages/DatasetsPage";
import ProfilingPage from "@/components/pages/ProfilingPage";
import StatisticsPage from "@/components/pages/StatisticsPage";
import AutoMLPage from "@/components/pages/AutoMLPage";
import TimeSeriesPage from "@/components/pages/TimeSeriesPage";
import EnsemblingPage from "@/components/pages/EnsemblingPage";
import LangChainPage from "@/components/pages/LangChainPage";

const pageComponents: Record<string, React.ComponentType> = {
  "/": WelcomePage,
  "/multi-agent": MultiAgentPage,
  "/rag": RAGPage,
  "/tools": ToolsPage,
  "/analytics": AnalyticsPage,
  "/demo": DemoPage,
  "/registry": RegistryPage,
  "/ab-testing": ABTestingPage,
  "/experiments": ExperimentsPage,
  "/monitoring": MonitoringPage,
  "/fine-tuning": FineTuningPage,
  "/datasets": DatasetsPage,
  "/profiling": ProfilingPage,
  "/statistics": StatisticsPage,
  "/automl": AutoMLPage,
  "/time-series": TimeSeriesPage,
  "/ensembling": EnsemblingPage,
  "/langchain": LangChainPage,
};

export default function Home() {
  const [activePath, setActivePath] = useState("/");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const ActiveComponent = pageComponents[activePath] || WelcomePage;

  if (!mounted) {
    return null;
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Sidebar activePath={activePath} onNavigate={setActivePath} />
      <main className="flex-1 ml-64 p-8">
        <motion.div
          key={activePath}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <ActiveComponent />
        </motion.div>
      </main>
    </div>
  );
}
