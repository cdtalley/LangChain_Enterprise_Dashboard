"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { TestTube, Plus, Play, Pause, TrendingUp, BarChart3, Calculator, Lightbulb } from "lucide-react";
import { getABTestingFramework } from "@/lib/ab-testing";
import { ExperimentStatus, MetricType, ExperimentConfig } from "@/lib/ab-testing";
import { STORAGE_KEYS } from "@/lib/persistence";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import HelpGuide from "@/components/HelpGuide";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export default function ABTestingPage() {
  const [framework] = useState(() => getABTestingFramework());
  const [experiments, setExperiments] = useState(framework.getAllExperiments());
  
  // Refresh experiments when component mounts or when storage changes
  useEffect(() => {
    const refreshExperiments = () => {
      setExperiments(framework.getAllExperiments());
    };
    
    // Refresh on mount
    refreshExperiments();
    
    // Listen for storage changes (cross-tab sync)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === STORAGE_KEYS.AB_TESTING) {
        refreshExperiments();
      }
    };
    
    window.addEventListener("storage", handleStorageChange);
    
    // Poll for changes (in case of same-tab updates)
    const interval = setInterval(refreshExperiments, 1000);
    
    return () => {
      window.removeEventListener("storage", handleStorageChange);
      clearInterval(interval);
    };
  }, [framework]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedExperiment, setSelectedExperiment] = useState<string | null>(null);
  const { financeData, ecommerceData } = useData();

  // Form state
  const [formData, setFormData] = useState<Partial<ExperimentConfig>>({
    name: "",
    description: "",
    hypothesis: "",
    metricName: "accuracy",
    metricType: MetricType.CONTINUOUS,
    baselineModel: "model-v1",
    treatmentModel: "model-v2",
    trafficSplit: 0.5,
    minSampleSize: 1000,
    maxDurationDays: 7,
    significanceLevel: 0.05,
    power: 0.80,
  });

  const [sampleSizeBaseline, setSampleSizeBaseline] = useState(0.85);
  const [sampleSizeLift, setSampleSizeLift] = useState(0.05);

  const exampleExperiments = [
    {
      name: "Model Accuracy Test",
      description: "Compare accuracy between model v1 and v2",
      hypothesis: "Model v2 will improve accuracy by 5%",
      metricType: MetricType.CONTINUOUS,
      baselineModel: "model-v1",
      treatmentModel: "model-v2",
    },
    {
      name: "Conversion Rate Test",
      description: "Test new checkout flow conversion",
      hypothesis: "New checkout flow increases conversion by 10%",
      metricType: MetricType.BINARY,
      baselineModel: "checkout-v1",
      treatmentModel: "checkout-v2",
    },
    {
      name: "Response Time Test",
      description: "Compare API response times",
      hypothesis: "Optimized API reduces response time by 20%",
      metricType: MetricType.CONTINUOUS,
      baselineModel: "api-v1",
      treatmentModel: "api-v2",
    },
  ];

  const loadExample = (example: typeof exampleExperiments[0]) => {
    const config: ExperimentConfig = {
      name: example.name,
      description: example.description,
      hypothesis: example.hypothesis,
      metricName: example.metricType === MetricType.BINARY ? "conversion_rate" : "accuracy",
      metricType: example.metricType,
      baselineModel: example.baselineModel,
      treatmentModel: example.treatmentModel,
      trafficSplit: 0.5,
      minSampleSize: 1000,
      maxDurationDays: 7,
      significanceLevel: 0.05,
      power: 0.80,
    };
    
    // Create experiment immediately
    const expId = framework.createExperiment(config);
    setExperiments(framework.getAllExperiments());
    setShowCreateForm(false);
    setSelectedExperiment(expId);
    
    // Auto-start the experiment and simulate data
    setTimeout(() => {
      handleStartExperiment(expId);
      // Auto-analyze after data is loaded
      setTimeout(() => {
        handleAnalyze(expId);
      }, 2000);
    }, 500);
  };

  const handleCreateExperiment = () => {
    if (!formData.name || !formData.description) return;

    const config: ExperimentConfig = {
      name: formData.name!,
      description: formData.description!,
      hypothesis: formData.hypothesis || "",
      metricName: formData.metricName || "accuracy",
      metricType: formData.metricType || MetricType.CONTINUOUS,
      baselineModel: formData.baselineModel || "model-v1",
      treatmentModel: formData.treatmentModel || "model-v2",
      trafficSplit: formData.trafficSplit || 0.5,
      minSampleSize: formData.minSampleSize || 1000,
      maxDurationDays: formData.maxDurationDays || 7,
      significanceLevel: formData.significanceLevel || 0.05,
      power: formData.power || 0.80,
    };

    const expId = framework.createExperiment(config);
    setExperiments(framework.getAllExperiments());
    setShowCreateForm(false);
    setSelectedExperiment(expId);
  };

  const handleStartExperiment = (expId: string) => {
    framework.startExperiment(expId);
    setExperiments(framework.getAllExperiments());
    
    // Simulate events using real data (async to not block UI)
    setTimeout(() => {
      const exp = framework.getExperiment(expId);
      if (exp && exp.config.metricType === MetricType.CONTINUOUS) {
        // Use finance data for continuous metrics
        financeData.slice(0, 500).forEach((record, idx) => {
          framework.recordEvent(expId, `user-${idx}`, record.amount);
        });
      } else if (exp && exp.config.metricType === MetricType.BINARY) {
        // Use ecommerce data for binary metrics
        ecommerceData.slice(0, 500).forEach((record, idx) => {
          framework.recordEvent(expId, `user-${idx}`, record.returned);
        });
      }
      setExperiments(framework.getAllExperiments());
    }, 100);
  };

  const handleStopExperiment = (expId: string) => {
    framework.stopExperiment(expId);
    setExperiments(framework.getAllExperiments());
  };

  const handleAnalyze = (expId: string) => {
    const result = framework.analyzeExperiment(expId);
    setExperiments(framework.getAllExperiments());
  };

  const calculatedSampleSize = framework.calculateSampleSize(
    sampleSizeBaseline,
    sampleSizeLift,
    0.05,
    0.80
  );

  const selectedExp = selectedExperiment ? framework.getExperiment(selectedExperiment) : null;

  return (
    <div className="space-y-6" data-tour="ab-testing">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🧪 A/B Testing</h1>
          <p className="text-gray-600">Statistical significance testing with sample size calculation</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all"
        >
          <Plus className="w-5 h-5" />
          Create Experiment
        </button>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use A/B Testing"
        description="Follow these steps to create and run your first experiment"
        steps={[
          {
            number: 1,
            title: "Calculate Sample Size",
            description: "Use the calculator below to determine how many samples you need. Enter your baseline metric and expected improvement percentage.",
            action: () => {
              const element = Array.from(document.querySelectorAll('h2')).find(el => el.textContent?.includes('Sample Size'));
              element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            actionLabel: "Go to Calculator"
          },
          {
            number: 2,
            title: "Choose a Template or Create Custom",
            description: "Click a Quick Start template below to auto-fill an experiment, or click 'Create Experiment' to build your own.",
            action: () => {
              setShowCreateForm(true);
            },
            actionLabel: "Create Experiment"
          },
          {
            number: 3,
            title: "Start Your Experiment",
            description: "Once created, click the Play button on your experiment card to begin collecting data. If you don't have an experiment yet, use a template above first.",
            action: () => {
              if (experiments.length > 0) {
                const firstExp = experiments[0];
                if (firstExp.status === ExperimentStatus.DRAFT) {
                  handleStartExperiment(firstExp.id);
                  setSelectedExperiment(firstExp.id);
                } else {
                  // Scroll to experiments list
                  setTimeout(() => {
                    const element = document.querySelector('[data-tour="ab-testing"]');
                    element?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }, 100);
                }
              } else {
                // No experiments - suggest using template
                loadExample(exampleExperiments[0]);
              }
            },
            actionLabel: experiments.length > 0 ? "Start Experiment" : "Load Template First"
          },
          {
            number: 4,
            title: "Analyze Results",
            description: "After collecting enough data, click 'Analyze' to see statistical significance, p-values, and recommendations.",
            action: () => {
              const runningExp = experiments.find(e => e.status === ExperimentStatus.RUNNING);
              if (runningExp) {
                handleAnalyze(runningExp.id);
                setSelectedExperiment(runningExp.id);
              }
            },
            actionLabel: "Analyze Results"
          },
          {
            number: 5,
            title: "Review Recommendations",
            description: "Check the recommendation section to see if your treatment outperformed the baseline with statistical significance.",
          }
        ]}
      />

      {/* Example Experiments */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-5 h-5 text-purple-600" />
          <h3 className="font-bold text-gray-900">Quick Start Templates:</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {exampleExperiments.map((example, idx) => (
            <button
              key={idx}
              onClick={() => loadExample(example)}
              className="text-left p-4 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300"
            >
              <div className="font-semibold text-gray-900 mb-1">{example.name}</div>
              <div className="text-sm text-gray-600 mb-2">{example.description}</div>
              <div className="text-xs text-purple-600">Click to load →</div>
            </button>
          ))}
        </div>
      </div>

      {/* Sample Size Calculator */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <Calculator className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold">Sample Size Calculator</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Baseline Mean
            </label>
            <input
              type="number"
              value={sampleSizeBaseline}
              onChange={(e) => setSampleSizeBaseline(parseFloat(e.target.value))}
              step="0.01"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Expected Lift (%)
            </label>
            <input
              type="number"
              value={sampleSizeLift * 100}
              onChange={(e) => setSampleSizeLift(parseFloat(e.target.value) / 100)}
              step="1"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div className="flex items-end">
            <div className="w-full">
              <div className="text-sm text-gray-600 mb-1">Required Sample Size</div>
              <div className="text-2xl font-bold text-purple-600">
                {calculatedSampleSize.toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Create Experiment Form */}
      {showCreateForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-xl font-bold mb-4">Create New Experiment</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experiment Name *
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="e.g., model-v2-test"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Metric Type
              </label>
              <select
                value={formData.metricType}
                onChange={(e) => setFormData({ ...formData, metricType: e.target.value as MetricType })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value={MetricType.CONTINUOUS}>Continuous</option>
                <option value={MetricType.BINARY}>Binary</option>
                <option value={MetricType.COUNT}>Count</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                rows={2}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hypothesis
              </label>
              <input
                type="text"
                value={formData.hypothesis}
                onChange={(e) => setFormData({ ...formData, hypothesis: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="Treatment will improve accuracy by 5%"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Baseline Model
              </label>
              <input
                type="text"
                value={formData.baselineModel}
                onChange={(e) => setFormData({ ...formData, baselineModel: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Treatment Model
              </label>
              <input
                type="text"
                value={formData.treatmentModel}
                onChange={(e) => setFormData({ ...formData, treatmentModel: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Traffic Split: {(formData.trafficSplit || 0) * 100}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={(formData.trafficSplit || 0) * 100}
                onChange={(e) => setFormData({ ...formData, trafficSplit: parseFloat(e.target.value) / 100 })}
                className="w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Sample Size
              </label>
              <input
                type="number"
                value={formData.minSampleSize}
                onChange={(e) => setFormData({ ...formData, minSampleSize: parseInt(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            <button
              onClick={handleCreateExperiment}
              className="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700"
            >
              Create Experiment
            </button>
            <button
              onClick={() => setShowCreateForm(false)}
              className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200"
            >
              Cancel
            </button>
          </div>
        </motion.div>
      )}

      {/* Experiments List */}
      <div className="space-y-4">
        {experiments.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <TestTube className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-gray-900 mb-2">No Experiments</h3>
            <p className="text-gray-600 mb-4">Create your first A/B test experiment</p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold"
            >
              Create Experiment
            </button>
          </div>
        ) : (
          experiments.map((exp) => {
            const result = exp.result;
            return (
              <motion.div
                key={exp.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold">{exp.config.name}</h3>
                    <p className="text-sm text-gray-600">{exp.config.description}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-3 py-1 rounded text-sm font-semibold ${
                        exp.status === ExperimentStatus.RUNNING
                          ? "bg-green-100 text-green-700"
                          : exp.status === ExperimentStatus.COMPLETED
                          ? "bg-blue-100 text-blue-700"
                          : "bg-gray-100 text-gray-700"
                      }`}
                    >
                      {exp.status}
                    </span>
                    {exp.status === ExperimentStatus.DRAFT && (
                      <button
                        onClick={() => {
                          handleStartExperiment(exp.id);
                          setSelectedExperiment(exp.id);
                        }}
                        className="p-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    )}
                    {exp.status === ExperimentStatus.RUNNING && (
                      <>
                        <button
                          onClick={() => handleAnalyze(exp.id)}
                          className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 text-sm font-semibold"
                        >
                          Analyze
                        </button>
                        <button
                          onClick={() => handleStopExperiment(exp.id)}
                          className="p-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
                        >
                          <Pause className="w-4 h-4" />
                        </button>
                      </>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Baseline</div>
                    <div className="font-bold">{exp.config.baselineModel}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Treatment</div>
                    <div className="font-bold">{exp.config.treatmentModel}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Events</div>
                    <div className="font-bold">{exp.events.length.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Traffic Split</div>
                    <div className="font-bold">{(exp.config.trafficSplit * 100).toFixed(0)}%</div>
                  </div>
                </div>

                {result && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                      <MetricCard
                        title="Baseline Mean"
                        value={result.baselineMean.toFixed(3)}
                        gradient="from-blue-500 to-cyan-500"
                      />
                      <MetricCard
                        title="Treatment Mean"
                        value={result.treatmentMean.toFixed(3)}
                        gradient="from-green-500 to-emerald-500"
                      />
                      <MetricCard
                        title="P-Value"
                        value={result.pValue.toFixed(4)}
                        gradient={result.isSignificant ? "from-green-500 to-emerald-500" : "from-gray-500 to-gray-600"}
                      />
                      <MetricCard
                        title="Lift"
                        value={`${result.relativeLift > 0 ? "+" : ""}${result.relativeLift.toFixed(2)}%`}
                        gradient={result.relativeLift > 0 ? "from-green-500 to-emerald-500" : "from-red-500 to-orange-500"}
                        trend={result.relativeLift > 0 ? "up" : "down"}
                      />
                    </div>

                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <div className="flex items-center gap-2 mb-2">
                        <BarChart3 className="w-5 h-5 text-purple-600" />
                        <span className="font-semibold">Recommendation:</span>
                      </div>
                      <p className="text-gray-700">{result.recommendation}</p>
                      <div className="mt-2 text-sm text-gray-600">
                        Confidence Interval: [{result.confidenceInterval[0].toFixed(3)}, {result.confidenceInterval[1].toFixed(3)}]
                      </div>
                    </div>

                    {/* Results Chart */}
                    <div className="bg-white rounded-lg p-4">
                      <h4 className="font-bold mb-4">Results Comparison</h4>
                      <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={[
                          { name: "Baseline", value: result.baselineMean, count: result.baselineCount },
                          { name: "Treatment", value: result.treatmentMean, count: result.treatmentCount },
                        ]}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="value" fill="#667eea" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {exp.events.length > 0 && !result && (
                  <div className="mt-4">
                    <div className="text-sm text-gray-600 mb-2">
                      Collecting data... {exp.events.length} / {exp.config.minSampleSize} events
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full transition-all"
                        style={{ width: `${Math.min(100, (exp.events.length / exp.config.minSampleSize) * 100)}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
}
