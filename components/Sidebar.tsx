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
      className="fixed left-0 top-0 h-full bg-gradient-to-b from-slate-900 via-indigo-950/95 to-slate-900 text-white shadow-2xl z-50 w-64 overflow-y-auto border-r border-white/5"
      data-tour="sidebar"
    >
      <div className="p-5 border-b border-white/10">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-lg font-bold tracking-tight">Enterprise AI</h1>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            aria-label={isOpen ? "Collapse sidebar" : "Expand sidebar"}
          >
            {isOpen ? "←" : "→"}
          </button>
        </div>
        <button
          onClick={startTour}
          className="w-full mb-3 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-500/20"
        >
          <Compass className="w-4 h-4" />
          Start Tour
        </button>
        <div className="bg-emerald-500/15 border border-emerald-400/30 rounded-xl p-3 text-center">
          <div className="flex items-center justify-center gap-2 mb-0.5">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            <span className="text-sm font-semibold text-emerald-200">System Operational</span>
          </div>
          <p className="text-xs text-slate-400">All Systems Ready</p>
        </div>
      </div>

      <div className="p-4 border-b border-white/5 bg-white/[0.03]">
        <h3 className="text-[11px] font-semibold text-slate-400 uppercase mb-3 tracking-wider">Real-Time Metrics</h3>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-white/5 rounded-lg p-2.5 border border-white/5">
            <div className="text-[10px] text-slate-400 uppercase tracking-wider mb-0.5">Uptime</div>
            <div className="text-sm font-bold text-emerald-400">99.9%</div>
          </div>
          <div className="bg-white/5 rounded-lg p-2.5 border border-white/5">
            <div className="text-[10px] text-slate-400 uppercase tracking-wider mb-0.5">Response</div>
            <div className="text-sm font-bold text-cyan-400">1.2s</div>
          </div>
        </div>
      </div>

      <nav className="p-4">
        <h3 className="text-[11px] font-semibold text-slate-400 uppercase mb-3 tracking-wider">Navigation</h3>
        <div className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePath === item.path;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.path)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 text-left ${
                  isActive
                    ? "bg-indigo-500/20 text-white border border-indigo-400/30 shadow-sm"
                    : "text-slate-300 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? "text-indigo-300" : ""}`} />
                <span className="text-sm font-medium truncate">{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      <div className="p-4 border-t border-white/5 mt-auto bg-white/[0.02]">
        <div className="text-xs text-slate-400 space-y-2">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full shrink-0" />
            <span>18+ Enterprise Features</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full shrink-0" />
            <span>Production Ready</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full shrink-0" />
            <span>Secure & Scalable</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

