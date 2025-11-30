"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Download, Sparkles } from "lucide-react";
import DemoDataGenerator, { DatasetInfo } from "@/lib/demo-data-generator";

const generator = new DemoDataGenerator();

export default function DataGenerator() {
  const [selectedIndustry, setSelectedIndustry] = useState<string>("E-commerce");
  const [nRecords, setNRecords] = useState<number>(1000);
  const [generatedData, setGeneratedData] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  const availableDatasets = generator.getAvailableDatasets();

  const handleGenerate = () => {
    setLoading(true);
    setTimeout(() => {
      try {
        const data = generator.generateDataset(selectedIndustry, nRecords);
        setGeneratedData(data);
      } catch (error) {
        console.error("Error generating data:", error);
      } finally {
        setLoading(false);
      }
    }, 500);
  };

  const handleDownload = (format: string) => {
    if (!generatedData) return;

    let content = "";
    let mimeType = "";
    let filename = "";

    if (format === "csv") {
      // Convert to CSV
      const headers = Object.keys(generatedData[0]).join(",");
      const rows = generatedData.map((row) =>
        Object.values(row).map((val) => `"${val}"`).join(",")
      );
      content = [headers, ...rows].join("\n");
      mimeType = "text/csv";
      filename = `${selectedIndustry.toLowerCase()}_data.csv`;
    } else if (format === "json") {
      content = JSON.stringify(generatedData, null, 2);
      mimeType = "application/json";
      filename = `${selectedIndustry.toLowerCase()}_data.json`;
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Demo Data Generator</h2>
        <p className="text-gray-600">Generate realistic demo datasets from various industries</p>
      </div>

      {/* Generator Controls */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Industry
            </label>
            <select
              value={selectedIndustry}
              onChange={(e) => setSelectedIndustry(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              {Object.keys(availableDatasets).map((industry) => (
                <option key={industry} value={industry}>
                  {availableDatasets[industry].icon} {industry}
                </option>
              ))}
            </select>
            <p className="mt-1 text-xs text-gray-500">
              {availableDatasets[selectedIndustry]?.description}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Records
            </label>
            <input
              type="number"
              min={100}
              max={10000}
              step={100}
              value={nRecords}
              onChange={(e) => setNRecords(parseInt(e.target.value) || 1000)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          <div className="flex items-end">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Generate Dataset
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Generated Data Display */}
      {generatedData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-6 rounded-xl shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-bold text-gray-900">
                Generated {selectedIndustry} Dataset
              </h3>
              <p className="text-sm text-gray-600">
                {generatedData.length.toLocaleString()} records × {Object.keys(generatedData[0]).length} columns
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => handleDownload("csv")}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                CSV
              </button>
              <button
                onClick={() => handleDownload("json")}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                JSON
              </button>
            </div>
          </div>

          <div className="overflow-x-auto max-h-96 border border-gray-200 rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50 sticky top-0">
                <tr>
                  {Object.keys(generatedData[0]).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {generatedData.slice(0, 50).map((row, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    {Object.values(row).map((val: any, colIdx) => (
                      <td key={colIdx} className="px-4 py-3 text-sm text-gray-900">
                        {typeof val === "number" ? val.toLocaleString() : String(val)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {generatedData.length > 50 && (
            <p className="mt-2 text-sm text-gray-500 text-center">
              Showing first 50 of {generatedData.length.toLocaleString()} records
            </p>
          )}
        </motion.div>
      )}
    </div>
  );
}

