"use client";

import { useState } from "react";
import { GraduationCap, Play, Settings, Lightbulb } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import MetricCard from "@/components/MetricCard";
import DataTable from "@/components/DataTable";

export default function FineTuningPage() {
  const { ecommerceData, financeData } = useData();
  const [selectedMethod, setSelectedMethod] = useState<"lora" | "qlora" | "peft">("lora");
  const [trainingConfig, setTrainingConfig] = useState({
    epochs: 10,
    learningRate: 0.0001,
    batchSize: 8,
    baseModel: "gpt-3.5-turbo",
  });

  const methods = [
    { id: "lora", name: "LoRA", description: "Low-Rank Adaptation - Efficient fine-tuning" },
    { id: "qlora", name: "QLoRA", description: "Quantized LoRA - Memory efficient" },
    { id: "peft", name: "PEFT", description: "Parameter-Efficient Fine-Tuning" },
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

  return (
    <div className="space-y-6" data-tour="fine-tuning">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🎓 LLM Fine-Tuning</h1>
        <p className="text-gray-600">LoRA, QLoRA, and PEFT fine-tuning for production-ready models</p>
      </div>

      {/* Method Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {methods.map((method) => (
          <button
            key={method.id}
            onClick={() => setSelectedMethod(method.id as any)}
            className={`p-6 rounded-xl transition-all text-left ${
              selectedMethod === method.id
                ? "bg-gradient-to-br from-purple-500 to-blue-500 text-white shadow-lg scale-105"
                : "bg-white text-gray-700 shadow hover:shadow-md"
            }`}
          >
            <GraduationCap className={`w-8 h-8 mb-3 ${selectedMethod === method.id ? "text-white" : "text-purple-600"}`} />
            <h3 className="font-bold text-lg mb-1">{method.name}</h3>
            <p className={`text-sm ${selectedMethod === method.id ? "text-white opacity-90" : "text-gray-600"}`}>
              {method.description}
            </p>
          </button>
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
            <button
              key={idx}
              onClick={() => loadPreset(preset)}
              className="text-left p-4 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300"
            >
              <div className="font-semibold text-gray-900 mb-1">{preset.name}</div>
              <div className="text-sm text-gray-600 mb-2">{preset.description}</div>
              <div className="text-xs text-gray-500">
                Epochs: {preset.epochs} • LR: {preset.learningRate} • Batch: {preset.batchSize}
              </div>
            </button>
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
              onChange={(e) => setTrainingConfig({ ...trainingConfig, epochs: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Learning Rate</label>
            <input
              type="number"
              step="0.0001"
              value={trainingConfig.learningRate}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, learningRate: parseFloat(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Batch Size</label>
            <input
              type="number"
              value={trainingConfig.batchSize}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, batchSize: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Base Model</label>
            <select
              value={trainingConfig.baseModel}
              onChange={(e) => setTrainingConfig({ ...trainingConfig, baseModel: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
            >
              <option>gpt-3.5-turbo</option>
              <option>gpt-4</option>
              <option>llama-2-7b</option>
              <option>llama-2-13b</option>
            </select>
          </div>
        </div>
        <button className="mt-4 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 hover:from-purple-700 hover:to-blue-700 transition-all">
          <Play className="w-5 h-5" />
          Start Fine-Tuning
        </button>
      </div>

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
