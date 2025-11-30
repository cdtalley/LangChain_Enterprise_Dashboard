"use client";

import { motion } from "framer-motion";
import { Sparkles, Zap, TrendingUp } from "lucide-react";

export default function HeroSection() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative overflow-hidden bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700 text-white"
    >
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
      <div className="container mx-auto px-4 py-20 relative z-10">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 animate-pulse" />
            <h1 className="text-5xl md:text-6xl font-bold mb-4">
              Enterprise LangChain AI Workbench
            </h1>
            <Sparkles className="w-8 h-8 animate-pulse" />
          </div>
          <p className="text-xl md:text-2xl mb-6 text-blue-100">
            Advanced LLM Orchestration & Multi-Agent Collaboration Platform
          </p>
          <p className="text-lg mb-8 text-blue-200">
            Production-Ready Multi-Agent AI System • Advanced MLOps • Real-Time Analytics
          </p>
          
          <div className="flex flex-wrap items-center justify-center gap-4 mt-8">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full"
            >
              <Zap className="w-5 h-5" />
              <span>Real-Time Processing</span>
            </motion.div>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full"
            >
              <TrendingUp className="w-5 h-5" />
              <span>AI-Powered</span>
            </motion.div>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full"
            >
              <Sparkles className="w-5 h-5" />
              <span>Enterprise-Grade</span>
            </motion.div>
          </div>
        </motion.div>
      </div>
      
      {/* Animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-gradient"></div>
    </motion.div>
  );
}

