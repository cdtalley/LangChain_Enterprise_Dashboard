"use client";

import { motion } from "framer-motion";
import { Bot, Database, BarChart3, Zap, TestTube, FileText, Eye, GraduationCap, Shield, Cpu, Network, Layers } from "lucide-react";

const features = [
  {
    icon: Bot,
    title: "Multi-Agent AI System",
    description: "Intelligent agent routing with specialized roles (Researcher, Coder, Analyst). Collaborative workflows with context sharing and task delegation.",
    gradient: "from-purple-500 to-pink-500",
    badge: "Advanced",
  },
  {
    icon: Database,
    title: "Advanced RAG Pipeline",
    description: "Hybrid semantic + keyword search with vector embeddings, BM25 retrieval, and intelligent re-ranking. Supports private data sources.",
    gradient: "from-blue-500 to-cyan-500",
    badge: "Production",
  },
  {
    icon: Cpu,
    title: "Local LLM Support",
    description: "Run LLaMA, Mistral, GPT4All locally for secure, cost-efficient inference. Toggle between local and cloud models seamlessly.",
    gradient: "from-green-500 to-emerald-500",
    badge: "Secure",
  },
  {
    icon: GraduationCap,
    title: "LLM Fine-Tuning",
    description: "LoRA, QLoRA, and PEFT fine-tuning workflows. Production-ready model customization with parameter-efficient methods.",
    gradient: "from-orange-500 to-red-500",
    badge: "MLOps",
  },
  {
    icon: BarChart3,
    title: "Model Registry",
    description: "Enterprise-grade versioning, lifecycle management, and model comparison. Track performance metrics and deployment history.",
    gradient: "from-indigo-500 to-purple-500",
    badge: "Enterprise",
  },
  {
    icon: TestTube,
    title: "A/B Testing Framework",
    description: "Statistical significance testing with t-test, chi-square, Mann-Whitney. Sample size calculation and traffic splitting.",
    gradient: "from-pink-500 to-rose-500",
    badge: "Analytics",
  },
  {
    icon: FileText,
    title: "Experiment Tracking",
    description: "MLflow-like tracking system with parameter logging, metric history, and run comparison. Full experiment lifecycle management.",
    gradient: "from-teal-500 to-blue-500",
    badge: "MLOps",
  },
  {
    icon: Eye,
    title: "Model Monitoring",
    description: "Real-time performance tracking, drift detection, and anomaly alerts. Production monitoring with automated alerting.",
    gradient: "from-yellow-500 to-orange-500",
    badge: "Monitoring",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "Private data processing, secure model deployment, and access controls. GDPR-compliant architecture for sensitive data.",
    gradient: "from-slate-500 to-gray-600",
    badge: "Security",
  },
  {
    icon: Network,
    title: "Modular Architecture",
    description: "Plug-and-play components for enterprise scalability. Microservices-ready with Docker deployment and Kubernetes support.",
    gradient: "from-violet-500 to-purple-500",
    badge: "Architecture",
  },
  {
    icon: Layers,
    title: "Full MLOps Stack",
    description: "Complete pipeline from data ingestion to model deployment. Automated workflows with CI/CD integration.",
    gradient: "from-cyan-500 to-blue-500",
    badge: "MLOps",
  },
  {
    icon: Zap,
    title: "Real-Time Analytics",
    description: "Live dashboards with interactive visualizations. Real-time data processing and streaming analytics capabilities.",
    gradient: "from-amber-500 to-yellow-500",
    badge: "Analytics",
  },
];

export default function FeatureCards() {
  return (
    <div className="mb-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Enterprise-Grade Capabilities
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Production-ready features designed for secure, scalable GenAI deployments
        </p>
      </motion.div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ y: -6, scale: 1.02 }}
              className="group relative bg-white rounded-xl shadow-md border border-gray-200 p-6 hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden"
            >
              {/* Gradient border on hover */}
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300 rounded-xl`}></div>
              
              {/* Top accent line */}
              <div className={`absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r ${feature.gradient} transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300`}></div>
              
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <span className="px-2.5 py-1 text-xs font-semibold text-gray-700 bg-gray-100 rounded-md">
                    {feature.badge}
                  </span>
                </div>
                
                <h3 className="text-lg font-bold mb-2 text-gray-900 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-300">
                  {feature.title}
                </h3>
                <p className="text-sm text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
