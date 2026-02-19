"use client";

import { useState, useEffect } from "react";
import { Sparkles, Play, TrendingUp, CheckCircle, Clock, Zap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  LineChart,
  Line,
} from "recharts";

interface ModelResult {
  name: string;
  accuracy: number;
  trainingTime: string;
  f1Score: number;
  precision: number;
  recall: number;
  status: "pending" | "training" | "completed";
}

interface TrainingStep {
  step: string;
  status: "pending" | "running" | "completed";
  message: string;
  timestamp: Date;
}

export default function AutoMLPage() {
  const { ecommerceData, financeData } = useData();
  const [isTraining, setIsTraining] = useState(false);
  const [selectedDataset, setSelectedDataset] = useState<"ecommerce" | "finance">("ecommerce");
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState<string>("");
  const [trainingSteps, setTrainingSteps] = useState<TrainingStep[]>([]);
  const [models, setModels] = useState<ModelResult[]>([
    { name: "Random Forest", accuracy: 0, trainingTime: "0s", f1Score: 0, precision: 0, recall: 0, status: "pending" },
    { name: "XGBoost", accuracy: 0, trainingTime: "0s", f1Score: 0, precision: 0, recall: 0, status: "pending" },
    { name: "LightGBM", accuracy: 0, trainingTime: "0s", f1Score: 0, precision: 0, recall: 0, status: "pending" },
    { name: "Neural Network", accuracy: 0, trainingTime: "0s", f1Score: 0, precision: 0, recall: 0, status: "pending" },
  ]);
  const [bestModel, setBestModel] = useState<ModelResult | null>(null);

  const addStep = (step: string, message: string, status: TrainingStep["status"] = "running") => {
    setTrainingSteps(prev => [...prev, { step, message, status, timestamp: new Date() }]);
    setCurrentStep(step);
  };

  const updateStepStatus = (step: string, status: TrainingStep["status"]) => {
    setTrainingSteps(prev => 
      prev.map(s => s.step === step ? { ...s, status } : s)
    );
  };

  const simulateModelTraining = async (modelIndex: number): Promise<ModelResult> => {
    const modelNames = ["Random Forest", "XGBoost", "LightGBM", "Neural Network"];
    const baseAccuracies = [0.92, 0.96, 0.95, 0.93];
    const baseTimes = [2.3, 3.1, 1.8, 12.4];
    
    const modelName = modelNames[modelIndex];
    const baseAccuracy = baseAccuracies[modelIndex];
    const baseTime = baseTimes[modelIndex];
    
    // Add some randomness
    const accuracy = baseAccuracy + (Math.random() * 0.04 - 0.02);
    const f1Score = accuracy - 0.01 + Math.random() * 0.02;
    const precision = accuracy - 0.005 + Math.random() * 0.01;
    const recall = accuracy - 0.005 + Math.random() * 0.01;
    
    // Simulate training time
    const trainingTime = (baseTime + Math.random() * 0.5).toFixed(1);
    
    addStep(`Training ${modelName}`, `Initializing ${modelName}...`);
    await new Promise(resolve => setTimeout(resolve, 500));
    
    addStep(`Training ${modelName}`, `Feature engineering and preprocessing...`);
    await new Promise(resolve => setTimeout(resolve, 800));
    
    addStep(`Training ${modelName}`, `Training model with cross-validation...`);
    await new Promise(resolve => setTimeout(resolve, baseTime * 200));
    
    addStep(`Training ${modelName}`, `Evaluating model performance...`);
    await new Promise(resolve => setTimeout(resolve, 300));
    
    updateStepStatus(`Training ${modelName}`, "completed");
    
    return {
      name: modelName,
      accuracy: Math.round(accuracy * 1000) / 10,
      trainingTime: `${trainingTime}s`,
      f1Score: Math.round(f1Score * 1000) / 10,
      precision: Math.round(precision * 1000) / 10,
      recall: Math.round(recall * 1000) / 10,
      status: "completed",
    };
  };

  const handleTrain = async () => {
    setIsTraining(true);
    setTrainingProgress(0);
    setTrainingSteps([]);
    setCurrentStep("");
    setBestModel(null);
    
    // Reset models
    setModels(prev => prev.map(m => ({ ...m, accuracy: 0, f1Score: 0, precision: 0, recall: 0, status: "pending" })));
    
    try {
      // Step 1: Data Loading
      addStep("Data Loading", `Loading ${selectedDataset === "ecommerce" ? "E-commerce" : "Finance"} dataset...`);
      await new Promise(resolve => setTimeout(resolve, 800));
      updateStepStatus("Data Loading", "completed");
      setTrainingProgress(10);
      
      // Step 2: Data Preprocessing
      addStep("Data Preprocessing", "Cleaning and preprocessing data...");
      await new Promise(resolve => setTimeout(resolve, 1000));
      updateStepStatus("Data Preprocessing", "completed");
      setTrainingProgress(20);
      
      // Step 3: Feature Engineering
      addStep("Feature Engineering", "Creating features and handling missing values...");
      await new Promise(resolve => setTimeout(resolve, 1200));
      updateStepStatus("Feature Engineering", "completed");
      setTrainingProgress(30);
      
      // Step 4: Train each model
      const trainedModels: ModelResult[] = [];
      for (let i = 0; i < models.length; i++) {
        setModels(prev => prev.map((m, idx) => 
          idx === i ? { ...m, status: "training" } : m
        ));
        
        const trained = await simulateModelTraining(i);
        trainedModels.push(trained);
        
        setModels(prev => prev.map((m, idx) => 
          idx === i ? trained : m
        ));
        
        setTrainingProgress(30 + ((i + 1) / models.length) * 50);
      }
      
      // Step 5: Model Comparison
      addStep("Model Comparison", "Comparing model performance...");
      await new Promise(resolve => setTimeout(resolve, 500));
      updateStepStatus("Model Comparison", "completed");
      setTrainingProgress(85);
      
      // Step 6: Select Best Model
      addStep("Selecting Best Model", "Identifying best performing model...");
      await new Promise(resolve => setTimeout(resolve, 500));
      const best = trainedModels.reduce((best, current) => 
        current.accuracy > best.accuracy ? current : best
      );
      setBestModel(best);
      updateStepStatus("Selecting Best Model", "completed");
      setTrainingProgress(95);
      
      // Step 7: Complete
      addStep("Training Complete", `Best model: ${best.name} with ${best.accuracy}% accuracy`);
      await new Promise(resolve => setTimeout(resolve, 300));
      setTrainingProgress(100);
      
    } catch (error) {
      console.error("Training error:", error);
      addStep("Error", "Training failed. Please try again.");
    } finally {
      setIsTraining(false);
      setCurrentStep("");
    }
  };

  const selectedData = selectedDataset === "ecommerce" ? ecommerceData : financeData;
  const dataSize = selectedData.length;

  return (
    <div className="space-y-6" data-tour="automl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🤖 AutoML</h1>
          <p className="text-gray-600">Automated machine learning pipeline with model comparison</p>
        </div>
        <button
          onClick={handleTrain}
          disabled={isTraining}
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 shadow-lg hover:shadow-xl"
        >
          {isTraining ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Training...
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              Start AutoML Pipeline
            </>
          )}
        </button>
      </div>

      {/* Training Progress */}
      {isTraining && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6 border border-purple-200"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Training Progress</h2>
            <span className="text-sm font-semibold text-purple-600">{trainingProgress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
            <motion.div
              className="bg-gradient-to-r from-purple-600 to-blue-600 h-3 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${trainingProgress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
          {currentStep && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Clock className="w-4 h-4 animate-spin" />
              <span>{currentStep}</span>
            </div>
          )}
        </motion.div>
      )}

      {/* Training Steps Log */}
      {trainingSteps.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-xl shadow-lg p-6 max-h-64 overflow-y-auto"
        >
          <h2 className="text-xl font-bold mb-4">Training Log</h2>
          <div className="space-y-2">
            <AnimatePresence>
              {trainingSteps.map((step, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-3 text-sm"
                >
                  {step.status === "completed" ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : step.status === "running" ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600"></div>
                  ) : (
                    <Clock className="w-4 h-4 text-gray-400" />
                  )}
                  <span className={step.status === "completed" ? "text-gray-600" : step.status === "running" ? "text-purple-600 font-medium" : "text-gray-400"}>
                    {step.message}
                  </span>
                  <span className="text-xs text-gray-400 ml-auto">
                    {step.timestamp.toLocaleTimeString()}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      {/* Dataset Selection */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Select Training Dataset</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => setSelectedDataset("ecommerce")}
            disabled={isTraining}
            className={`border-2 rounded-lg p-6 text-center transition-all ${
              selectedDataset === "ecommerce"
                ? "border-purple-500 bg-purple-50"
                : "border-gray-300 hover:border-purple-300"
            } ${isTraining ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          >
            <h3 className="font-bold mb-2">E-commerce Data</h3>
            <p className="text-sm text-gray-600">{ecommerceData.length.toLocaleString()} records</p>
            {selectedDataset === "ecommerce" && (
              <CheckCircle className="w-5 h-5 text-purple-600 mx-auto mt-2" />
            )}
          </button>
          <button
            onClick={() => setSelectedDataset("finance")}
            disabled={isTraining}
            className={`border-2 rounded-lg p-6 text-center transition-all ${
              selectedDataset === "finance"
                ? "border-purple-500 bg-purple-50"
                : "border-gray-300 hover:border-purple-300"
            } ${isTraining ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
          >
            <h3 className="font-bold mb-2">Finance Data</h3>
            <p className="text-sm text-gray-600">{financeData.length.toLocaleString()} records</p>
            {selectedDataset === "finance" && (
              <CheckCircle className="w-5 h-5 text-purple-600 mx-auto mt-2" />
            )}
          </button>
        </div>
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Records:</span>
              <span className="font-semibold ml-2">{dataSize.toLocaleString()}</span>
            </div>
            <div>
              <span className="text-gray-600">Features:</span>
              <span className="font-semibold ml-2">
                {selectedData.length > 0 ? Object.keys(selectedData[0]).length : 0}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Status:</span>
              <span className="font-semibold ml-2 text-green-600">Ready</span>
            </div>
          </div>
        </div>
      </div>

      {/* Best Model Highlight */}
      {bestModel && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl shadow-lg p-6 text-white"
        >
          <div className="flex items-center gap-3 mb-4">
            <Zap className="w-6 h-6" />
            <h2 className="text-2xl font-bold">Best Model Selected</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-sm opacity-90">Model</div>
              <div className="text-xl font-bold">{bestModel.name}</div>
            </div>
            <div>
              <div className="text-sm opacity-90">Accuracy</div>
              <div className="text-xl font-bold">{bestModel.accuracy}%</div>
            </div>
            <div>
              <div className="text-sm opacity-90">F1 Score</div>
              <div className="text-xl font-bold">{bestModel.f1Score}%</div>
            </div>
            <div>
              <div className="text-sm opacity-90">Training Time</div>
              <div className="text-xl font-bold">{bestModel.trainingTime}</div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Model Results */}
      {models.some(m => m.accuracy > 0) && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Model Comparison</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={models}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#667eea" name="Accuracy %" />
            </BarChart>
          </ResponsiveContainer>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
            {models.map((model, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`bg-gray-50 rounded-lg p-4 border-2 ${
                  bestModel?.name === model.name ? "border-purple-500 bg-purple-50" : "border-gray-200"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="font-bold">{model.name}</div>
                  {bestModel?.name === model.name && (
                    <CheckCircle className="w-5 h-5 text-purple-600" />
                  )}
                </div>
                <div className="text-2xl font-bold text-purple-600 mb-1">{model.accuracy}%</div>
                <div className="text-xs text-gray-600 space-y-1">
                  <div>F1: {model.f1Score}%</div>
                  <div>Precision: {model.precision}%</div>
                  <div>Recall: {model.recall}%</div>
                  <div className="mt-2 pt-2 border-t border-gray-200">
                    Training: {model.trainingTime}
                  </div>
                </div>
                {model.status === "training" && (
                  <div className="mt-2 flex items-center gap-2 text-xs text-purple-600">
                    <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-purple-600"></div>
                    Training...
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Data Preview */}
      <DataTable data={selectedData.slice(0, 100)} title="Training Data Preview" maxRows={5} />
    </div>
  );
}
