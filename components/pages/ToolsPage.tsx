"use client";

import { useState } from "react";
import { Code, Globe, Database, Play, CheckCircle, XCircle, Lightbulb } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import DataTable from "@/components/DataTable";
import MetricCard from "@/components/MetricCard";

export default function ToolsPage() {
  const { financeData, ecommerceData } = useData();
  const [code, setCode] = useState(`import pandas as pd
import numpy as np

# Analyze finance data
df = pd.DataFrame(finance_data)
print(f"Total transactions: \{len(df)}")
print(f"Average amount: \${df['amount'].mean():.2f}")
print(f"Fraud rate: \{df['is_fraud'].mean() * 100:.2f}%")`);
  const [codeOutput, setCodeOutput] = useState<string>("");
  const [executing, setExecuting] = useState(false);
  const [selectedTool, setSelectedTool] = useState<"code" | "scrape" | "analyze">("code");

  const handleExecuteCode = () => {
    setExecuting(true);
    setTimeout(() => {
      // Simulate code execution
      const output = `Total transactions: ${financeData.length}
Average amount: $${(financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length).toFixed(2)}
Fraud rate: ${(financeData.filter(r => r.is_fraud === 1).length / financeData.length * 100).toFixed(2)}%`;
      setCodeOutput(output);
      setExecuting(false);
    }, 1500);
  };

  const handleAnalyzeData = () => {
    setExecuting(true);
    setTimeout(() => {
      const analysis = {
        finance: {
          total: financeData.length,
          avgAmount: financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length,
          fraudRate: financeData.filter(r => r.is_fraud === 1).length / financeData.length * 100,
        },
        ecommerce: {
          total: ecommerceData.length,
          avgOrder: ecommerceData.reduce((sum, r) => sum + r.total_amount, 0) / ecommerceData.length,
          returnRate: ecommerceData.filter(r => r.returned === 1).length / ecommerceData.length * 100,
        },
      };
      setCodeOutput(JSON.stringify(analysis, null, 2));
      setExecuting(false);
    }, 1000);
  };

  const exampleCodeSnippets = [
    {
      name: "Data Summary",
      code: `# Quick Data Summary
import pandas as pd

# Load your data
df = pd.DataFrame(finance_data)

# Basic statistics
print(f"Total records: \{len(df)}")
print(f"Average amount: \${df['amount'].mean():.2f}")
print(f"Max amount: \${df['amount'].max():.2f}")
print(f"Min amount: \${df['amount'].min():.2f}")
print(f"Fraud rate: \{df['is_fraud'].mean() * 100:.2f}%")`,
    },
    {
      name: "Group Analysis",
      code: `# Group by Category
import pandas as pd

df = pd.DataFrame(finance_data)
category_stats = df.groupby('category').agg(\{
    'amount': ['sum', 'mean', 'count']
\})
print(category_stats)`,
    },
    {
      name: "Time Series",
      code: `# Time Series Analysis
import pandas as pd
from datetime import datetime

df = pd.DataFrame(finance_data)
df['date'] = pd.to_datetime(df['date'])
daily = df.groupby(df['date'].dt.date)['amount'].sum()
print(daily.head())`,
    },
  ];

  const quickAnalyses = [
    {
      name: "Finance Summary",
      code: `# Finance Data Summary
total = len(finance_data)
avg = sum(r['amount'] for r in finance_data) / total
fraud = sum(r['is_fraud'] for r in finance_data) / total * 100
print(f"Total: \{total}, Avg: \${avg:.2f}, Fraud: \{fraud:.2f}%")`,
      execute: handleAnalyzeData,
    },
    {
      name: "E-commerce Analysis",
      code: `# E-commerce Analysis
total = len(ecommerce_data)
revenue = sum(r['total_amount'] for r in ecommerce_data)
avg_order = revenue / total
print(f"Total Orders: \{total}, Revenue: \${revenue:.2f}, Avg: \${avg_order:.2f}")`,
      execute: handleAnalyzeData,
    },
  ];

  return (
    <div className="space-y-6" data-tour="tools">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Tool Execution</h1>
        <p className="text-gray-600">Execute Python code, scrape websites, analyze data</p>
      </div>

      {/* Tool Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => setSelectedTool("code")}
          className={`p-6 rounded-xl transition-all text-left ${
            selectedTool === "code"
              ? "bg-gradient-to-br from-purple-500 to-blue-500 text-white shadow-lg"
              : "bg-white text-gray-700 shadow hover:shadow-md"
          }`}
        >
          <Code className={`w-8 h-8 mb-3 ${selectedTool === "code" ? "text-white" : "text-purple-600"}`} />
          <h3 className="font-bold mb-2">Code Execution</h3>
          <p className={`text-sm ${selectedTool === "code" ? "text-white opacity-90" : "text-gray-600"}`}>
            Run Python code in sandboxed environment
          </p>
        </button>
        <button
          onClick={() => setSelectedTool("scrape")}
          className={`p-6 rounded-xl transition-all text-left ${
            selectedTool === "scrape"
              ? "bg-gradient-to-br from-blue-500 to-cyan-500 text-white shadow-lg"
              : "bg-white text-gray-700 shadow hover:shadow-md"
          }`}
        >
          <Globe className={`w-8 h-8 mb-3 ${selectedTool === "scrape" ? "text-white" : "text-blue-600"}`} />
          <h3 className="font-bold mb-2">Web Scraping</h3>
          <p className={`text-sm ${selectedTool === "scrape" ? "text-white opacity-90" : "text-gray-600"}`}>
            Extract data from websites
          </p>
        </button>
        <button
          onClick={() => setSelectedTool("analyze")}
          className={`p-6 rounded-xl transition-all text-left ${
            selectedTool === "analyze"
              ? "bg-gradient-to-br from-green-500 to-emerald-500 text-white shadow-lg"
              : "bg-white text-gray-700 shadow hover:shadow-md"
          }`}
        >
          <Database className={`w-8 h-8 mb-3 ${selectedTool === "analyze" ? "text-white" : "text-green-600"}`} />
          <h3 className="font-bold mb-2">Data Analysis</h3>
          <p className={`text-sm ${selectedTool === "analyze" ? "text-white opacity-90" : "text-gray-600"}`}>
            Analyze datasets with pandas
          </p>
        </button>
      </div>

      {/* Code Execution */}
      {selectedTool === "code" && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold mb-4">Python Code Execution</h2>
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 mb-4">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb className="w-5 h-5 text-purple-600" />
                <h3 className="font-bold text-gray-900">Example Code Snippets:</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                {exampleCodeSnippets.map((snippet, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setCode(snippet.code);
                      // Auto-execute after loading
                      setTimeout(() => {
                        handleExecuteCode();
                      }, 300);
                    }}
                    className="text-left p-3 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300 text-sm"
                  >
                    <div className="font-semibold text-gray-900">{snippet.name}</div>
                    <div className="text-xs text-gray-500 mt-1">Click to run</div>
                  </button>
                ))}
              </div>
            </div>
            <div className="flex gap-2 mb-4">
              {quickAnalyses.map((analysis, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setCode(analysis.code);
                    analysis.execute();
                  }}
                  className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm"
                >
                  {analysis.name}
                </button>
              ))}
            </div>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg font-mono text-sm"
            placeholder="Enter Python code here..."
          />
          <button
            onClick={handleExecuteCode}
            disabled={executing}
            className="mt-4 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            {executing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Executing...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Execute Code
              </>
            )}
          </button>
          {codeOutput && (
            <div className="mt-4 p-4 bg-gray-900 text-green-400 rounded-lg font-mono text-sm">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-xs text-gray-400">Output:</span>
              </div>
              <pre className="whitespace-pre-wrap">{codeOutput}</pre>
            </div>
          )}
        </div>
      )}

      {/* Web Scraping */}
      {selectedTool === "scrape" && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">Web Scraping Tool</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">URL to Scrape</label>
              <input
                type="url"
                placeholder="https://example.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg"
              />
            </div>
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold flex items-center gap-2">
              <Globe className="w-5 h-5" />
              Scrape Website
            </button>
          </div>
        </div>
      )}

      {/* Data Analysis */}
      {selectedTool === "analyze" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <MetricCard
              title="Finance Records"
              value={financeData.length.toLocaleString()}
              icon={Database}
              gradient="from-pink-500 to-rose-500"
            />
            <MetricCard
              title="E-commerce Records"
              value={ecommerceData.length.toLocaleString()}
              icon={Database}
              gradient="from-blue-500 to-cyan-500"
            />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <DataTable data={financeData.slice(0, 100)} title="Finance Data" maxRows={10} />
            <DataTable data={ecommerceData.slice(0, 100)} title="E-commerce Data" maxRows={10} />
          </div>
        </div>
      )}
    </div>
  );
}
