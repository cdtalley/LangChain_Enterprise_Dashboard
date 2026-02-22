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
import { useTour } from "@/lib/TourContext";

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

const pageTitles: Record<string, string> = {
  "/": "Dashboard",
  "/multi-agent": "Multi-Agent",
  "/rag": "Advanced RAG",
  "/tools": "Tools",
  "/analytics": "Analytics",
  "/demo": "Enterprise Demo",
  "/registry": "Model Registry",
  "/ab-testing": "A/B Testing",
  "/experiments": "Experiments",
  "/monitoring": "Monitoring",
  "/fine-tuning": "Fine-Tuning",
  "/datasets": "Datasets",
  "/profiling": "Data Profiling",
  "/statistics": "Statistics",
  "/automl": "AutoML",
  "/time-series": "Time Series",
  "/ensembling": "Ensembling",
  "/langchain": "LangChain",
};

export default function Home() {
  const [activePath, setActivePath] = useState("/");
  const [mounted, setMounted] = useState(false);
  const { setNavigationHandler } = useTour();

  useEffect(() => {
    setMounted(true);
    const handler = (path: string) => setActivePath(path);
    setNavigationHandler(handler);
  }, [setNavigationHandler]);

  useEffect(() => {
    const title = pageTitles[activePath] ?? "Dashboard";
    document.title = `${title} | LangChain Enterprise`;
  }, [activePath]);

  const ActiveComponent = pageComponents[activePath] || WelcomePage;

  if (!mounted) {
    return null;
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30">
      <Sidebar activePath={activePath} onNavigate={setActivePath} />
      <main className="flex-1 ml-64 p-8 max-w-[1920px] mx-auto print:ml-0 print:p-0">
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
