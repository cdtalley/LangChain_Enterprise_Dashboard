"use client";

import { motion } from "framer-motion";
import { Sparkles, Zap, TrendingUp, Shield, Rocket } from "lucide-react";

export default function HeroSection() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white mb-12 border border-white/5 shadow-[var(--shadow-xl)]"
    >
      {/* Subtle grid */}
      <div className="absolute inset-0 opacity-[0.07]" style={{
        backgroundImage: `linear-gradient(rgba(255,255,255,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.08) 1px, transparent 1px)`,
        backgroundSize: '48px 48px'
      }} />
      
      <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
      
      <div className="relative z-10 px-8 py-16 md:py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="max-w-5xl mx-auto text-center"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-white/10 backdrop-blur-md rounded-full border border-white/20"
          >
            <Rocket className="w-4 h-4 text-indigo-300" />
            <span className="text-sm font-semibold">Production-Ready Enterprise Platform</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-5xl md:text-6xl lg:text-7xl font-extrabold mb-6 leading-tight tracking-tight"
          >
            <span className="bg-gradient-to-r from-white via-indigo-100 to-violet-200 bg-clip-text text-transparent">
              LangChain Enterprise
            </span>
            <br />
            <span className="text-white">AI Workbench</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="text-xl md:text-2xl text-slate-300 mb-4 font-medium max-w-3xl mx-auto"
          >
            Advanced LLM Orchestration & Multi-Agent Collaboration Platform
          </motion.p>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="text-lg text-slate-400 mb-10 max-w-2xl mx-auto"
          >
            Secure, scalable, and production-ready GenAI platform with local LLM support, 
            advanced RAG, and MLOps across the lifecycle
          </motion.p>
          
          {/* Feature Pills */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="flex flex-wrap items-center justify-center gap-3 mt-8"
          >
            {[
              { icon: Zap, text: "Real-Time Processing", color: "from-amber-400 to-orange-500" },
              { icon: Shield, text: "Enterprise Security", color: "from-emerald-400 to-teal-500" },
              { icon: TrendingUp, text: "Production MLOps", color: "from-cyan-400 to-blue-500" },
              { icon: Sparkles, text: "18+ Features", color: "from-violet-400 to-indigo-500" },
            ].map((item, idx) => {
              const Icon = item.icon;
              return (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8 + idx * 0.08 }}
                  whileHover={{ scale: 1.04, y: -2 }}
                  className={`flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r ${item.color} rounded-xl shadow-lg backdrop-blur-sm border border-white/20`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-semibold">{item.text}</span>
                </motion.div>
              );
            })}
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12 pt-8 border-t border-white/10"
          >
            {[
              { label: "Features", value: "18+" },
              { label: "Datasets", value: "5" },
              { label: "Uptime", value: "99.9%" },
              { label: "Response", value: "<1.2s" },
            ].map((stat, idx) => (
              <div key={idx} className="text-center">
                <div className="text-2xl md:text-3xl font-bold tracking-tight mb-0.5">{stat.value}</div>
                <div className="text-sm text-slate-400 font-medium">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </div>
      
      {/* Animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-gradient pointer-events-none"></div>
    </motion.div>
  );
}
