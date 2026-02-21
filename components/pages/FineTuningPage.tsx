"use client";

import { useState, useEffect, useCallback } from "react";
import { GraduationCap, Play, Settings, Lightbulb, Pause, CheckCircle, XCircle, Activity, TrendingDown, TrendingUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import HelpGuide from "@/components/HelpGuide";
import { 
  getFineTuningFramework, 
  FineTuningMethod, 
  FineTuningStatus,
  FineTuningConfig,
  FineTuningJob 
} from "@/lib/llm-fine-tuning";
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

export default function FineTuningPage() {
  const { ecommerceData, financeData } = useData();
  const framework = getFineTuningFramework();
  const [selectedMethod, setSelectedMethod] = useState<FineTuningMethod>(FineTuningMethod.LORA);
  const [trainingConfig, setTrainingConfig] = useState({
    epochs: 10,
    learningRate: 0.0001,
    batchSize: 8,
    baseModel: "gpt-3.5-turbo",
  });
  const [jobs, setJobs] = useState<FineTuningJob[]>(framework.getAllJobs());
  const [activeJob, setActiveJob] = useState<FineTuningJob | null>(framework.getActiveJob());
  const [isTraining, setIsTraining] = useState(false);

  // Refresh jobs periodically when training
  useEffect(() => {
    if (isTraining || activeJob) {
      const interval = setInterval(() => {
        const updatedJobs = framework.getAllJobs();
        setJobs(updatedJobs);
        const currentActive = framework.getActiveJob();
        setActiveJob(currentActive);
        if (!currentActive || currentActive.status === FineTuningStatus.COMPLETED || currentActive.status === FineTuningStatus.FAILED) {
          setIsTraining(false);
        }
      }, 500);
      return () => clearInterval(interval);
    }
  }, [isTraining, activeJob, framework]);

  const methods = [
    { id: FineTuningMethod.LORA, name: "LoRA", description: "Low-Rank Adaptation - Efficient fine-tuning", color: "from-purple-500 to-indigo-500" },
    { id: FineTuningMethod.QLORA, name: "QLoRA", description: "Quantized LoRA - Memory efficient", color: "from-blue-500 to-cyan-500" },
    { id: FineTuningMethod.PEFT, name: "PEFT", description: "Parameter-Efficient Fine-Tuning", color: "from-green-500 to-emerald-500" },
  ];

  const presetConfigs = [
    {
      name: "Quick Fine-Tune",
      epochs: 5,
      learningRate: 0.0001,
      batchSize: 8,
      baseModel: "gpt-3.5-turbo",
      description: "Fast training for quick experiments",
    },
    {
      name: "Production Fine-Tune",
      epochs: 10,
      learningRate: 0.00005,
      batchSize: 16,
      baseModel: "gpt-4",
      description: "Thorough training for production",
    },
    {
      name: "Memory Efficient",
      epochs: 8,
      learningRate: 0.0001,
      batchSize: 4,
      baseModel: "llama-2-7b",
      description: "Optimized for limited memory",
    },
  ];

  const loadPreset = (preset: typeof presetConfigs[0]) => {
    setTrainingConfig({
      epochs: preset.epochs,
      learningRate: preset.learningRate,
      batchSize: preset.batchSize,
      baseModel: preset.baseModel,
    });
  };

  const handleStartTraining = useCallback(async () => {
    if (isTraining || activeJob) {
      alert("A training job is already running. Please wait for it to complete or stop it first.");
      return;
    }

    const config: FineTuningConfig = {
      method: selectedMethod,
      epochs: trainingConfig.epochs,
      learningRate: trainingConfig.learningRate,
      batchSize: trainingConfig.batchSize,
      baseModel: trainingConfig.baseModel,
      trainingDataSize: ecommerceData.length,
      validationDataSize: financeData.length,
    };

    const jobId = framework.createJob(config);
    setIsTraining(true);
    setJobs(framework.getAllJobs());
    setActiveJob(framework.getJob(jobId)!);

    try {
      await framework.startTraining(jobId, (updatedJob) => {
        setActiveJob({ ...updatedJob });
        setJobs(framework.getAllJobs());
      });
    } catch (error: any) {
      console.error("Training error:", error);
      const job = framework.getJob(jobId);
      if (job) {
        job.status = FineTuningStatus.FAILED;
        job.error = error.message || "Training failed";
        setActiveJob({ ...job });
        setJobs(framework.getAllJobs());
      }
      setIsTraining(false);
    }
  }, [selectedMethod, trainingConfig, ecommerceData.length, financeData.length, framework, isTraining, activeJob]);

  const handleStopTraining = () => {
    if (activeJob) {
      framework.stopTraining(activeJob.id);
      setActiveJob(null);
      setIsTraining(false);
      setJobs(framework.getAllJobs());
    }
  };

  const getStatusColor = (status: FineTuningStatus) => {
    switch (status) {
      case FineTuningStatus.COMPLETED:
        return "bg-green-100 text-green-700";
      case FineTuningStatus.TRAINING:
      case FineTuningStatus.PREPARING:
      case FineTuningStatus.VALIDATING:
        return "bg-blue-100 text-blue-700";
      case FineTuningStatus.FAILED:
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  const getProgress = (job: FineTuningJob) => {
    if (job.status === FineTuningStatus.COMPLETED) return 100;
    if (job.status === FineTuningStatus.IDLE) return 0;
    if (job.status === FineTuningStatus.PREPARING) return 5;
    if (job.status === FineTuningStatus.VALIDATING) return 95;
    return (job.currentEpoch / job.config.epochs) * 90;
  };

  const currentJob = activeJob || (jobs.length > 0 ? jobs[0] : null);

  return (
    <div className="space-y-6" data-tour="fine-tuning">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🎓 LLM Fine-Tuning</h1>
        <p className="text-gray-600">LoRA, QLoRA, and PEFT fine-tuning for production-ready models</p>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use Fine-Tuning"
        description="Learn how to fine-tune LLMs with parameter-efficient methods"
        steps={[
          {
            number: 1,
            title: "Choose Fine-Tuning Method",
            description: "Select LoRA (efficient), QLoRA (memory-efficient), or PEFT (parameter-efficient). Each has different trade-offs.",
          },
          {
            number: 2,
            title: "Load a Preset or Configure Manually",
            description: "Use a preset configuration for quick start, or customize epochs, learning rate, batch size, and base model.",
            action: () => {
              loadPreset(presetConfigs[0]);
            },
            actionLabel: "Load Quick Preset"
          },
          {
            number: 3,
            title: "Start Training",
            description: "Click 'Start Fine-Tuning' to begin. Watch real-time progress, loss curves, and metrics update as training progresses.",
            action: () => {
              if (!isTraining && !activeJob) {
                handleStartTraining();
              }
            },
            actionLabel: "Start Training"
          },
          {
            number: 4,
            title: "Monitor Progress",
            description: "Track training progress with live metrics, loss curves, and epoch-by-epoch updates. Training runs automatically.",
          },
          {
            number: 5,
            title: "Review Results",
            description: "After completion, view final metrics, loss curves, and model performance. Jobs are saved for later review.",
          }
        ]}
      />

      {/* Method Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {methods.map((method) => (
          <motion.button
            key={method.id}
            onClick={() => setSelectedMethod(method.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`p-6 rounded-xl transition-all text-left ${
              selectedMethod === method.id
                ? `bg-gradient-to-br ${method.color} text-white shadow-lg`
                : "bg-white text-gray-700 shadow hover:shadow-md"
            }`}
          >
            <GraduationCap className={`w-8 h-8 mb-3 ${selectedMethod === method.id ? "text-white" : "text-purple-600"}`} />
            <h3 className="font-bold text-lg mb-1">{method.name}</h3>
            <p className={`text-sm ${selectedMethod === method.id ? "text-white opacity-90" : "text-gray-600"}`}>
              {method.description}
            </p>
          </motion.button>
        ))}
      </div>

      {/* Preset Configurations */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-5 h-5 text-purple-600" />
          <h3 className="font-bold text-gray-900">Preset Configurations:</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {presetConfigs.map((preset, idx) => (
            <motion.button
              key={idx}
              onClick={() => loadPreset(preset)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="text-left p-4 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300"
            >
              <div className="font-semibold text-gray-900 mb-1">{preset.name}</div>
              <div className="text-sm text-gray-600 mb-2">{preset.description}</div>
              <div className="text-xs text-gray-500">
                Epochs: {preset.epochs} • LR: {preset.learningRate} • Batch: {preset.batchSize}
              </div>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Training Configuration */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <Settings className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold">Training Configuration</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Epochs</label>
            <input
              type="number"
              value={trainingConfig.epochs}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, epochs: parseInt(e.target.value) || 1 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              disabled={isTraining}
              min="1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Learning Rate</label>
            <input
              type="number"
              step="0.0001"
              value={trainingConfig.learningRate}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, learningRate: parseFloat(e.target.value) || 0.0001 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              disabled={isTraining}
              min="0.0001"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Batch Size</label>
            <input
              type="number"
              value={trainingConfig.batchSize}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, batchSize: parseInt(e.target.value) || 1 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              disabled={isTraining}
              min="1"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Base Model</label>
            <select
              value={trainingConfig.baseModel}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, baseModel: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              disabled={isTraining}
            >
              <option>gpt-3.5-turbo</option>
              <option>gpt-4</option>
              <option>llama-2-7b</option>
              <option>llama-2-13b</option>
            </select>
          </div>
        </div>
        <div className="mt-4 flex gap-3">
          <motion.button
            onClick={handleStartTraining}
            disabled={isTraining}
            whileHover={!isTraining ? { scale: 1.02 } : {}}
            whileTap={!isTraining ? { scale: 0.98 } : {}}
            className={`px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-all ${
              isTraining
                ? "bg-gray-400 text-white cursor-not-allowed"
                : "bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700"
            }`}
          >
            {isTraining ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Training...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Start Fine-Tuning
              </>
            )}
          </motion.button>
          {isTraining && activeJob && (
            <motion.button
              onClick={handleStopTraining}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-3 bg-red-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:bg-red-700 transition-all"
            >
              <Pause className="w-5 h-5" />
              Stop Training
            </motion.button>
          )}
        </div>
      </div>

      {/* Active Training Progress */}
      <AnimatePresence>
        {activeJob && (activeJob.status === FineTuningStatus.TRAINING || 
                      activeJob.status === FineTuningStatus.PREPARING || 
                      activeJob.status === FineTuningStatus.VALIDATING) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-lg p-6 border-2 border-purple-200"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Activity className="w-6 h-6 text-purple-600 animate-pulse" />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-gray-900">Training in Progress</h3>
                  <p className="text-sm text-gray-600">
                    {activeJob.config.method.toUpperCase()} • {activeJob.config.baseModel}
                  </p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded text-sm font-semibold ${getStatusColor(activeJob.status)}`}>
                {activeJob.status}
              </span>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                <span>Epoch {activeJob.currentEpoch} of {activeJob.config.epochs}</span>
                <span>{Math.round(getProgress(activeJob))}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <motion.div
                  className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${getProgress(activeJob)}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>

            {/* Real-time Metrics */}
            {activeJob.metrics.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <MetricCard
                  title="Current Loss"
                  value={activeJob.metrics[activeJob.metrics.length - 1]?.loss.toFixed(4) || "0.0000"}
                  gradient="from-red-500 to-orange-500"
                  icon={TrendingDown}
                />
                {activeJob.metrics[activeJob.metrics.length - 1]?.accuracy !== undefined && (
                  <MetricCard
                    title="Accuracy"
                    value={`${((activeJob.metrics[activeJob.metrics.length - 1]?.accuracy || 0) * 100).toFixed(2)}%`}
                    gradient="from-green-500 to-emerald-500"
                    icon={TrendingUp}
                  />
                )}
                <MetricCard
                  title="Learning Rate"
                  value={activeJob.config.learningRate.toFixed(6)}
                  gradient="from-blue-500 to-cyan-500"
                />
                <MetricCard
                  title="Batch Size"
                  value={activeJob.config.batchSize.toString()}
                  gradient="from-purple-500 to-indigo-500"
                />
              </div>
            )}

            {/* Loss Curve */}
            {activeJob.metrics.length > 1 && (
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-bold mb-4">Training Loss Curve</h4>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={activeJob.metrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="epoch" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="loss" 
                      stroke="#8b5cf6" 
                      strokeWidth={2}
                      dot={{ fill: "#8b5cf6", r: 4 }}
                      name="Loss"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Completed Jobs */}
      {jobs.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Training History</h2>
          {jobs.map((job) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold">{job.config.method.toUpperCase()} - {job.config.baseModel}</h3>
                  <p className="text-sm text-gray-600">
                    {job.startTime && new Date(job.startTime).toLocaleString()}
                    {job.endTime && ` • Completed: ${new Date(job.endTime).toLocaleString()}`}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded text-sm font-semibold ${getStatusColor(job.status)}`}>
                    {job.status === FineTuningStatus.COMPLETED && <CheckCircle className="w-4 h-4 inline mr-1" />}
                    {job.status === FineTuningStatus.FAILED && <XCircle className="w-4 h-4 inline mr-1" />}
                    {job.status}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <div className="text-sm text-gray-600">Epochs</div>
                  <div className="font-bold">{job.config.epochs}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Final Loss</div>
                  <div className="font-bold">{job.finalLoss?.toFixed(4) || "N/A"}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Final Accuracy</div>
                  <div className="font-bold">{job.finalAccuracy ? `${(job.finalAccuracy * 100).toFixed(2)}%` : "N/A"}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Training Data</div>
                  <div className="font-bold">{job.config.trainingDataSize.toLocaleString()} samples</div>
                </div>
              </div>

              {job.metrics.length > 1 && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-bold mb-4">Training Metrics</h4>
                  <ResponsiveContainer width="100%" height={200}>
                    <LineChart data={job.metrics}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="epoch" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="loss" 
                        stroke="#8b5cf6" 
                        strokeWidth={2}
                        dot={{ fill: "#8b5cf6", r: 3 }}
                        name="Loss"
                      />
                      {job.metrics.some(m => m.accuracy !== undefined) && (
                        <Line 
                          type="monotone" 
                          dataKey="accuracy" 
                          stroke="#10b981" 
                          strokeWidth={2}
                          dot={{ fill: "#10b981", r: 3 }}
                          name="Accuracy"
                        />
                      )}
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              {job.error && (
                <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-700">Error: {job.error}</p>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}

      {/* Training Data Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-bold mb-4">Training Data Preview</h3>
          <DataTable data={ecommerceData.slice(0, 50)} title="E-commerce Training Data" maxRows={5} />
        </div>
        <div>
          <h3 className="text-lg font-bold mb-4">Validation Data Preview</h3>
          <DataTable data={financeData.slice(0, 50)} title="Finance Validation Data" maxRows={5} />
        </div>
      </div>
    </div>
  );
}
