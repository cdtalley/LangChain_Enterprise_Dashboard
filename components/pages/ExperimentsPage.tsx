"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FileText, Plus, Play, CheckCircle, XCircle, TrendingUp } from "lucide-react";
import { getExperimentTracker } from "@/lib/experiment-tracking";
import { STORAGE_KEYS } from "@/lib/persistence";
import MetricCard from "@/components/MetricCard";
import HelpGuide from "@/components/HelpGuide";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export default function ExperimentsPage() {
  const [tracker] = useState(() => getExperimentTracker());
  const [runs, setRuns] = useState(tracker.getAllRuns());
  
  // Refresh runs when component mounts or when storage changes
  useEffect(() => {
    const refreshRuns = () => {
      setRuns(tracker.getAllRuns());
    };
    
    // Refresh on mount
    refreshRuns();
    
    // Listen for storage changes (cross-tab sync)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === STORAGE_KEYS.EXPERIMENT_TRACKING) {
        refreshRuns();
      }
    };
    
    window.addEventListener("storage", handleStorageChange);
    
    // Poll for changes (in case of same-tab updates)
    const interval = setInterval(refreshRuns, 1000);
    
    return () => {
      window.removeEventListener("storage", handleStorageChange);
      clearInterval(interval);
    };
  }, [tracker]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedRun, setSelectedRun] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    experimentName: "default",
    parameters: "learning_rate=0.001\nepochs=10\nbatch_size=32",
  });

  const handleCreateRun = () => {
    if (!formData.name) return;

    const params: Record<string, any> = {};
    formData.parameters.split("\n").forEach(line => {
      const [key, value] = line.split("=");
      if (key && value) {
        params[key.trim()] = isNaN(parseFloat(value)) ? value.trim() : parseFloat(value);
      }
    });

    const runId = tracker.startRun(formData.name, formData.experimentName, params);
    
    // Simulate metrics over time
    let step = 0;
    const interval = setInterval(() => {
      tracker.logMetric(runId, "accuracy", 0.7 + Math.random() * 0.2, step);
      tracker.logMetric(runId, "loss", 0.5 - Math.random() * 0.3, step);
      step++;
      
      if (step >= 10) {
        clearInterval(interval);
        tracker.endRun(runId, "completed");
      }
      
      setRuns(tracker.getAllRuns());
    }, 500);

    setRuns(tracker.getAllRuns());
    setShowCreateForm(false);
    setSelectedRun(runId);
  };

  const selectedRunData = selectedRun ? tracker.getRun(selectedRun) : null;

  return (
    <div className="space-y-6" data-tour="experiments">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">📝 Experiment Tracking</h1>
          <p className="text-gray-600">MLflow-like tracking system with parameter logging and run comparison</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all"
        >
          <Plus className="w-5 h-5" />
          New Experiment Run
        </button>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use Experiment Tracking"
        description="Track ML experiments like MLflow - log parameters, metrics, and compare runs"
        steps={[
          {
            number: 1,
            title: "Create a New Run",
            description: "Click 'New Experiment Run' to start tracking. Give it a name and experiment group.",
            action: () => {
              setShowCreateForm(true);
            },
            actionLabel: "Create Run"
          },
          {
            number: 2,
            title: "Set Parameters",
            description: "Enter your hyperparameters in key=value format (one per line). Example: learning_rate=0.001",
          },
          {
            number: 3,
            title: "Monitor Metrics",
            description: "Once started, metrics are logged automatically. Watch accuracy and loss update in real-time.",
          },
          {
            number: 4,
            title: "Compare Runs",
            description: "Click on any run to see detailed metrics, parameters, and performance charts.",
          },
          {
            number: 5,
            title: "Review History",
            description: "All runs are saved automatically. Use the metrics summary cards to see overall status.",
          }
        ]}
      />

      {/* Metrics Summary */}
      {runs.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard
            title="Total Runs"
            value={runs.length}
            icon={FileText}
            gradient="from-purple-500 to-indigo-500"
          />
          <MetricCard
            title="Completed"
            value={runs.filter(r => r.status === "completed").length}
            icon={CheckCircle}
            gradient="from-green-500 to-emerald-500"
          />
          <MetricCard
            title="Running"
            value={runs.filter(r => r.status === "running").length}
            icon={Play}
            gradient="from-blue-500 to-cyan-500"
          />
          <MetricCard
            title="Failed"
            value={runs.filter(r => r.status === "failed").length}
            icon={XCircle}
            gradient="from-red-500 to-orange-500"
          />
        </div>
      )}

      {/* Create Form */}
      {showCreateForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-xl font-bold mb-4">Create New Experiment Run</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Run Name *
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="e.g., run-2024-01-15"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experiment Name
              </label>
              <input
                type="text"
                value={formData.experimentName}
                onChange={(e) => setFormData({ ...formData, experimentName: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Parameters (one per line: key=value)
              </label>
              <textarea
                value={formData.parameters}
                onChange={(e) => setFormData({ ...formData, parameters: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                rows={5}
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleCreateRun}
                className="px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700"
              >
                Start Run
              </button>
              <button
                onClick={() => setShowCreateForm(false)}
                className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200"
              >
                Cancel
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Runs List */}
      <div className="space-y-4">
        {runs.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-gray-900 mb-2">No Experiment Runs</h3>
            <p className="text-gray-600 mb-4">Start tracking your ML experiments</p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold"
            >
              Create Run
            </button>
          </div>
        ) : (
          runs.map((run) => (
            <motion.div
              key={run.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-all"
              onClick={() => setSelectedRun(run.id)}
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold">{run.name}</h3>
                  <p className="text-sm text-gray-600">{run.experimentName}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`px-3 py-1 rounded text-sm font-semibold ${
                      run.status === "completed"
                        ? "bg-green-100 text-green-700"
                        : run.status === "running"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {run.status}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <div className="text-sm text-gray-600">Start Time</div>
                  <div className="font-semibold">{run.startTime.toLocaleString()}</div>
                </div>
                {run.endTime && (
                  <div>
                    <div className="text-sm text-gray-600">End Time</div>
                    <div className="font-semibold">{run.endTime.toLocaleString()}</div>
                  </div>
                )}
                <div>
                  <div className="text-sm text-gray-600">Parameters</div>
                  <div className="font-semibold">{Object.keys(run.parameters).length}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Metrics</div>
                  <div className="font-semibold">{Object.keys(run.metrics).length}</div>
                </div>
              </div>

              {Object.keys(run.metrics).length > 0 && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {Object.entries(run.metrics).slice(0, 4).map(([key, value]) => (
                    <div key={key} className="bg-gray-50 rounded p-2">
                      <div className="text-xs text-gray-600">{key}</div>
                      <div className="font-bold">{typeof value === "number" ? value.toFixed(4) : value}</div>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          ))
        )}
      </div>

      {/* Run Details */}
      {selectedRunData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-2xl font-bold mb-4">Run Details: {selectedRunData.name}</h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold mb-3">Parameters</h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                {Object.entries(selectedRunData.parameters).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="font-semibold">{key}:</span>
                    <span>{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-bold mb-3">Metrics</h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                {Object.entries(selectedRunData.metrics).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="font-semibold">{key}:</span>
                    <span>{typeof value === "number" ? value.toFixed(4) : value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {selectedRunData.metricsHistory.length > 0 && (
            <div className="mt-6">
              <h3 className="font-bold mb-3">Metrics Over Time</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={selectedRunData.metricsHistory.map(h => ({
                    step: h.step,
                    ...h.metrics,
                  }))}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="step" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {selectedRunData.metricsHistory.length > 0 &&
                   Object.keys(selectedRunData.metricsHistory[0].metrics).map((metric, idx) => (
                     <Line
                       key={metric}
                       type="monotone"
                       dataKey={metric}
                       stroke={["#667eea", "#764ba2", "#f093fb", "#4facfe"][idx % 4]}
                       name={metric}
                     />
                   ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
