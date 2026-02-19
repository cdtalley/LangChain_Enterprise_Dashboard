"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Home,
  Bot,
  Database,
  Wrench,
  BarChart3,
  Target,
  Package,
  TestTube,
  FileText,
  Eye,
  GraduationCap,
  BookOpen,
  Activity,
  FlaskConical,
  Sparkles,
  Zap,
  TrendingUp,
  Compass,
} from "lucide-react";
import { useTour } from "@/lib/TourContext";

export interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
}

export const navItems: NavItem[] = [
  { id: "welcome", label: "Welcome", icon: Home, path: "/" },
  { id: "multi-agent", label: "Multi-Agent System", icon: Bot, path: "/multi-agent" },
  { id: "rag", label: "Advanced RAG", icon: Database, path: "/rag" },
  { id: "tools", label: "Tool Execution", icon: Wrench, path: "/tools" },
  { id: "analytics", label: "Analytics Dashboard", icon: BarChart3, path: "/analytics" },
  { id: "demo", label: "Enterprise Demo", icon: Target, path: "/demo" },
  { id: "registry", label: "Model Registry", icon: Package, path: "/registry" },
  { id: "ab-testing", label: "A/B Testing", icon: TestTube, path: "/ab-testing" },
  { id: "experiments", label: "Experiment Tracking", icon: FileText, path: "/experiments" },
  { id: "monitoring", label: "Model Monitoring", icon: Eye, path: "/monitoring" },
  { id: "fine-tuning", label: "LLM Fine-Tuning", icon: GraduationCap, path: "/fine-tuning" },
  { id: "datasets", label: "Datasets & Models", icon: BookOpen, path: "/datasets" },
  { id: "profiling", label: "Data Profiling", icon: Activity, path: "/profiling" },
  { id: "statistics", label: "Statistical Analysis", icon: FlaskConical, path: "/statistics" },
  { id: "automl", label: "AutoML", icon: Sparkles, path: "/automl" },
  { id: "time-series", label: "Time Series", icon: TrendingUp, path: "/time-series" },
  { id: "ensembling", label: "Model Ensembling", icon: Zap, path: "/ensembling" },
  { id: "langchain", label: "LangChain Expertise", icon: Bot, path: "/langchain" },
];

interface SidebarProps {
  activePath: string;
  onNavigate: (path: string) => void;
}

export default function Sidebar({ activePath, onNavigate }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);
  const { startTour } = useTour();

  return (
    <motion.div
      initial={{ x: -300 }}
      animate={{ x: isOpen ? 0 : -280 }}
      className="fixed left-0 top-0 h-full bg-gradient-to-b from-purple-900 via-blue-900 to-indigo-900 text-white shadow-2xl z-50 w-64 overflow-y-auto"
      data-tour="sidebar"
    >
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold">🚀 Enterprise AI</h1>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-1 hover:bg-white/10 rounded"
          >
            {isOpen ? "←" : "→"}
          </button>
        </div>
        <button
          onClick={startTour}
          className="w-full mb-3 px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all"
        >
          <Compass className="w-4 h-4" />
          Start Tour
        </button>
        <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-3 text-center">
          <div className="flex items-center justify-center gap-2 mb-1">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold">System Operational</span>
          </div>
          <p className="text-xs text-gray-300">All Systems Ready</p>
        </div>
      </div>

      {/* Metrics */}
      <div className="p-4 border-b border-slate-700/50 bg-slate-800/30">
        <h3 className="text-xs font-semibold text-slate-400 uppercase mb-3 tracking-wider">Real-Time Metrics</h3>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-slate-700/30 rounded-lg p-2.5 border border-slate-600/30">
            <div className="text-xs text-slate-400 mb-1">Uptime</div>
            <div className="text-sm font-bold text-green-400">99.9%</div>
          </div>
          <div className="bg-slate-700/30 rounded-lg p-2.5 border border-slate-600/30">
            <div className="text-xs text-slate-400 mb-1">Response</div>
            <div className="text-sm font-bold text-blue-400">1.2s</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        <h3 className="text-xs font-semibold text-slate-400 uppercase mb-3 tracking-wider">Navigation</h3>
        <div className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePath === item.path;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.path)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-purple-600/20 to-blue-600/20 text-white shadow-lg border border-purple-500/30"
                    : "text-slate-300 hover:bg-slate-700/50 hover:text-white"
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-purple-300' : ''}`} />
                <span className="text-sm font-medium">{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-700/50 mt-auto bg-slate-800/30">
        <div className="text-xs text-slate-400 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-purple-400 rounded-full"></span>
            <span>18+ Enterprise Features</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-400 rounded-full"></span>
            <span>Production Ready</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span>
            <span>Secure & Scalable</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

