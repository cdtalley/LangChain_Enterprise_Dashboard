"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HelpCircle, X, Play, ChevronRight } from "lucide-react";

interface Step {
  number: number;
  title: string;
  description: string;
  action?: () => void;
  actionLabel?: string;
}

interface HelpGuideProps {
  title: string;
  description: string;
  steps: Step[];
  defaultOpen?: boolean;
}

export default function HelpGuide({ title, description, steps, defaultOpen = false }: HelpGuideProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const handleStepAction = (step: Step) => {
    if (step.action) {
      step.action();
      setCompletedSteps(new Set([...completedSteps, step.number]));
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between hover:bg-blue-100/50 transition-colors rounded-xl"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <HelpCircle className="w-5 h-5 text-blue-600" />
          </div>
          <div className="text-left">
            <h3 className="font-bold text-gray-900">{title}</h3>
            <p className="text-sm text-gray-600">{description}</p>
          </div>
        </div>
        <ChevronRight
          className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? "rotate-90" : ""}`}
        />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-4 pt-0 space-y-3">
              {steps.map((step) => (
                <motion.div
                  key={step.number}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: step.number * 0.1 }}
                  className={`flex items-start gap-4 p-3 rounded-lg ${
                    completedSteps.has(step.number)
                      ? "bg-green-50 border border-green-200"
                      : "bg-white border border-gray-200"
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                      completedSteps.has(step.number)
                        ? "bg-green-500 text-white"
                        : "bg-blue-500 text-white"
                    }`}
                  >
                    {completedSteps.has(step.number) ? "✓" : step.number}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-1">{step.title}</h4>
                    <p className="text-sm text-gray-600 mb-2">{step.description}</p>
                    {step.action && (
                      <button
                        onClick={() => handleStepAction(step)}
                        className="flex items-center gap-2 px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Play className="w-3 h-3" />
                        {step.actionLabel || "Try it"}
                      </button>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
