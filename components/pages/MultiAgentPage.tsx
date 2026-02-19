"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Bot, Send, Sparkles, Code, TrendingUp, CheckCircle, Clock, Lightbulb } from "lucide-react";
import { useData } from "@/lib/DataContext";
import DataTable from "@/components/DataTable";
import MetricCard from "@/components/MetricCard";
import HelpGuide from "@/components/HelpGuide";

const exampleQueries = [
  {
    text: "What's the average transaction amount in our finance data?",
    agent: "analyst",
    description: "Data analysis query",
  },
  {
    text: "Research best practices for LLM fine-tuning",
    agent: "researcher",
    description: "Research query",
  },
  {
    text: "Write Python code to calculate fraud rate",
    agent: "coder",
    description: "Code generation query",
  },
  {
    text: "Analyze e-commerce revenue trends and provide insights",
    agent: "analyst",
    description: "Business analysis",
  },
];

export default function MultiAgentPage() {
  const { financeData, ecommerceData } = useData();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<"auto" | "researcher" | "coder" | "analyst">("auto");

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    
    // Simulate intelligent routing
    let agent = selectedAgent;
    if (agent === "auto") {
      if (query.toLowerCase().includes("research") || query.toLowerCase().includes("find") || query.toLowerCase().includes("best practices")) {
        agent = "researcher";
      } else if (query.toLowerCase().includes("code") || query.toLowerCase().includes("python") || query.toLowerCase().includes("write")) {
        agent = "coder";
      } else {
        agent = "analyst";
      }
    }

    setTimeout(() => {
      const avgAmount = financeData.reduce((sum, r) => sum + r.amount, 0) / financeData.length;
      const totalRevenue = ecommerceData.reduce((sum, r) => sum + r.total_amount, 0);
      const fraudRate = (financeData.filter(r => r.is_fraud === 1).length / financeData.length * 100).toFixed(2);

      const responses: Record<string, any> = {
        researcher: {
          agent: "Researcher",
          response: `I've researched your query "${query}" and found relevant information from ${financeData.length + ecommerceData.length} data sources.\n\nKey findings:\n• Current best practices emphasize parameter-efficient fine-tuning (LoRA/QLoRA)\n• Recommended learning rates: 1e-4 to 5e-4\n• Batch sizes: 4-16 depending on model size\n• Evaluation metrics should include both accuracy and latency\n\nSources: ${financeData.length + ecommerceData.length} internal datasets, 5 external research papers`,
          sources: financeData.length + ecommerceData.length,
          confidence: 0.92,
          processingTime: "1.2s",
        },
        coder: {
          agent: "Coder",
          response: `Here's a Python solution for "${query}":\n\n\`\`\`python\nimport pandas as pd\n\n# Calculate fraud rate\nfraud_count = df[df['is_fraud'] == 1].shape[0]\ntotal_count = df.shape[0]\nfraud_rate = (fraud_count / total_count) * 100\n\nprint(f"Fraud Rate: {fraud_rate:.2f}%")\nprint(f"Total Transactions: {total_count}")\nprint(f"Fraudulent: {fraud_count}")\n\`\`\`\n\nThis code calculates the fraud rate from transaction data.`,
          sources: 3,
          confidence: 0.88,
          processingTime: "0.8s",
        },
        analyst: {
          agent: "Analyst",
          response: `Based on analysis of ${financeData.length} finance records and ${ecommerceData.length} e-commerce records:\n\n📊 Key Insights:\n• Average transaction amount: $${avgAmount.toFixed(2)}\n• Total e-commerce revenue: $${(totalRevenue / 1000).toFixed(1)}K\n• Fraud rate: ${fraudRate}%\n• Top product category: Electronics\n• Peak transaction time: 2-4 PM\n\n💡 Recommendations:\n1. Monitor transactions above $${(avgAmount * 2).toFixed(2)} for fraud\n2. Focus marketing on high-performing product categories\n3. Optimize inventory for peak hours`,
          sources: 2,
          confidence: 0.95,
          processingTime: "1.5s",
        },
      };

      setResults([responses[agent]]);
      setLoading(false);
    }, 1500);
  };

  const handleExampleClick = (example: typeof exampleQueries[0]) => {
    setQuery(example.text);
    if (example.agent !== "auto") {
      setSelectedAgent(example.agent as any);
    }
    // Auto-submit after a short delay
    setTimeout(() => {
      handleSubmit();
    }, 300);
  };

  const agents = [
    {
      id: "researcher",
      name: "Researcher Agent",
      icon: Sparkles,
      description: "Gathers information from multiple sources",
      color: "from-blue-500 to-cyan-500",
      capabilities: ["Web search", "Data collection", "Source verification"],
    },
    {
      id: "coder",
      name: "Coder Agent",
      icon: Code,
      description: "Executes code and performs analysis",
      color: "from-green-500 to-emerald-500",
      capabilities: ["Python execution", "Data processing", "Code generation"],
    },
    {
      id: "analyst",
      name: "Analyst Agent",
      icon: TrendingUp,
      description: "Synthesizes insights and recommendations",
      color: "from-purple-500 to-indigo-500",
      capabilities: ["Data analysis", "Trend identification", "Report generation"],
    },
  ];

  return (
    <div className="space-y-6" data-tour="multi-agent">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🤖 Multi-Agent System</h1>
        <p className="text-gray-600">Specialized agents with intelligent routing and collaborative workflows</p>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use Multi-Agent System"
        description="Learn how to leverage specialized AI agents for different tasks"
        steps={[
          {
            number: 1,
            title: "Choose Your Agent",
            description: "Select Auto for intelligent routing, or pick a specific agent: Researcher (information gathering), Coder (code generation), or Analyst (data insights).",
            action: () => {
              setSelectedAgent("auto");
            },
            actionLabel: "Set to Auto"
          },
          {
            number: 2,
            title: "Try Example Queries",
            description: "Click any example below to see how different agents handle different types of queries.",
            action: () => {
              handleExampleClick(exampleQueries[0]);
            },
            actionLabel: "Try Example"
          },
          {
            number: 3,
            title: "Submit Your Query",
            description: "Type your question or task in the input field and click Send. The system will route it to the best agent automatically.",
            action: () => {
              if (!query) {
                setQuery("What's the average transaction amount?");
              }
              document.querySelector('input[placeholder*="Ask a question"]')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            actionLabel: "Focus Input"
          },
          {
            number: 4,
            title: "Review Agent Response",
            description: "Each response includes sources used, confidence level, processing time, and detailed results.",
          },
          {
            number: 5,
            title: "Explore Agent Capabilities",
            description: "Check the agent cards below to understand what each agent specializes in.",
          }
        ]}
      />

      {/* Example Queries */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-5 h-5 text-purple-600" />
          <h3 className="font-bold text-gray-900">Try These Examples:</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {exampleQueries.map((example, idx) => (
            <button
              key={idx}
              onClick={() => handleExampleClick(example)}
              className="text-left p-4 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300"
            >
              <div className="text-sm font-semibold text-gray-900 mb-1">{example.text}</div>
              <div className="text-xs text-gray-500">{example.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Agent Selection */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Select Agent</label>
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setSelectedAgent("auto")}
              className={`px-4 py-2 rounded-lg transition-all ${
                selectedAgent === "auto"
                  ? "bg-purple-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              🤖 Auto (Intelligent Routing)
            </button>
            {agents.map((agent) => {
              const Icon = agent.icon;
              return (
                <button
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent.id as any)}
                  className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
                    selectedAgent === agent.id
                      ? `bg-gradient-to-r ${agent.color} text-white`
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {agent.name.split(" ")[0]}
                </button>
              );
            })}
          </div>
        </div>
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question or assign a task..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            onKeyPress={(e) => e.key === "Enter" && handleSubmit()}
          />
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Processing...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Send
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-4">
          {results.map((result, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Bot className="w-6 h-6 text-purple-600" />
                  <div>
                    <h3 className="font-bold text-gray-900">{result.agent} Agent</h3>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <CheckCircle className="w-4 h-4" />
                        {result.sources} sources
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {result.processingTime}
                      </span>
                      <span>Confidence: {(result.confidence * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="whitespace-pre-wrap text-gray-700">{result.response}</pre>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Agent Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {agents.map((agent) => {
          const Icon = agent.icon;
          return (
            <motion.div
              key={agent.id}
              whileHover={{ y: -4 }}
              className={`bg-gradient-to-br ${agent.color} text-white rounded-xl shadow-lg p-6`}
            >
              <Icon className="w-8 h-8 mb-3" />
              <h3 className="font-bold text-lg mb-2">{agent.name}</h3>
              <p className="text-sm opacity-90 mb-3">{agent.description}</p>
              <div className="space-y-1">
                {agent.capabilities.map((cap, idx) => (
                  <div key={idx} className="text-xs opacity-75">• {cap}</div>
                ))}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Data Integration */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Available Data Sources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard
            title="Finance Data"
            value={financeData.length.toLocaleString()}
            subtitle="transactions"
            gradient="from-pink-500 to-rose-500"
          />
          <MetricCard
            title="E-commerce Data"
            value={ecommerceData.length.toLocaleString()}
            subtitle="orders"
            gradient="from-blue-500 to-cyan-500"
          />
        </div>
        <div className="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DataTable data={financeData.slice(0, 50)} title="Finance Data Sample" maxRows={5} />
          <DataTable data={ecommerceData.slice(0, 50)} title="E-commerce Data Sample" maxRows={5} />
        </div>
      </div>
    </div>
  );
}
