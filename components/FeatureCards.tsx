"use client";

import { motion } from "framer-motion";
import { Bot, Database, BarChart3, Zap, TestTube, FileText, Eye, GraduationCap } from "lucide-react";

const features = [
  {
    icon: Bot,
    title: "Multi-Agent AI System",
    description: "Specialized agents (Researcher, Coder, Analyst) with intelligent routing and collaborative workflows",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    icon: Database,
    title: "Advanced RAG",
    description: "Hybrid search combining semantic and keyword matching with smart chunking strategies",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    icon: GraduationCap,
    title: "LLM Fine-Tuning",
    description: "LoRA, QLoRA, and PEFT fine-tuning for production-ready model customization",
    gradient: "from-green-500 to-emerald-500",
  },
  {
    icon: BarChart3,
    title: "Model Registry",
    description: "Versioning, lifecycle management, and model comparison with performance tracking",
    gradient: "from-orange-500 to-red-500",
  },
  {
    icon: TestTube,
    title: "A/B Testing",
    description: "Statistical significance testing with sample size calculation and traffic splitting",
    gradient: "from-indigo-500 to-purple-500",
  },
  {
    icon: FileText,
    title: "Experiment Tracking",
    description: "MLflow-like tracking system with parameter logging and run comparison",
    gradient: "from-pink-500 to-rose-500",
  },
  {
    icon: Eye,
    title: "Model Monitoring",
    description: "Performance tracking, drift detection, and anomaly detection with real-time alerts",
    gradient: "from-teal-500 to-blue-500",
  },
  {
    icon: Zap,
    title: "Enterprise Features",
    description: "Complete MLOps platform from data to deployment with production-ready architecture",
    gradient: "from-yellow-500 to-orange-500",
  },
];

export default function FeatureCards() {
  return (
    <div className="mb-12">
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl font-bold text-center mb-8 text-gray-900"
      >
        🌟 Enterprise Features
      </motion.h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-2xl transition-all cursor-pointer group"
            >
              <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-bold mb-2 text-gray-900">{feature.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed">{feature.description}</p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

