"use client";

import { Bot, Code, Zap, Database, Sparkles, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import { useData } from "@/lib/DataContext";
import DataTable from "@/components/DataTable";
import MetricCard from "@/components/MetricCard";

const patterns = [
  {
    name: "Multi-Agent Orchestration",
    description: "Coordinate multiple specialized agents",
    code: `from langchain.agents import initialize_agent
from langchain.tools import Tool

# Create specialized agents
researcher = create_research_agent()
coder = create_coding_agent()
analyst = create_analysis_agent()

# Orchestrate workflow
result = orchestrate_agents(query, [researcher, coder, analyst])`,
    icon: Bot,
    gradient: "from-purple-500 to-indigo-500",
  },
  {
    name: "Advanced RAG Pipeline",
    description: "Hybrid search with semantic + keyword",
    code: `from langchain.vectorstores import Chroma
from langchain.retrievers import BM25Retriever

# Hybrid retrieval
semantic_retriever = vectorstore.as_retriever()
keyword_retriever = BM25Retriever.from_documents(docs)

# Combine results
results = ensemble_retrieval(query, [semantic_retriever, keyword_retriever])`,
    icon: Database,
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    name: "Custom Tools & Chains",
    description: "Build reusable tool chains",
    code: `from langchain.tools import BaseTool
from langchain.chains import LLMChain

class CustomTool(BaseTool):
    name = "data_analyzer"
    description = "Analyzes datasets"
    
    def _run(self, query: str) -> str:
        # Custom logic
        return analyze_data(query)

# Use in chain
chain = LLMChain(llm=llm, tools=[CustomTool()])`,
    icon: Zap,
    gradient: "from-green-500 to-emerald-500",
  },
  {
    name: "Memory & Context",
    description: "Maintain conversation context",
    code: `from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)`,
    icon: Sparkles,
    gradient: "from-pink-500 to-rose-500",
  },
];

export default function LangChainPage() {
  const { financeData, ecommerceData } = useData();

  return (
    <div className="space-y-6" data-tour="langchain">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">⚡ LangChain Expertise</h1>
        <p className="text-gray-600">Advanced LangChain patterns and best practices</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard
          title="Available Datasets"
          value="5"
          icon={Database}
          gradient="from-purple-500 to-indigo-500"
        />
        <MetricCard
          title="Total Records"
          value={(financeData.length + ecommerceData.length).toLocaleString()}
          icon={TrendingUp}
        />
        <MetricCard
          title="Patterns"
          value={patterns.length}
          icon={Code}
          gradient="from-blue-500 to-cyan-500"
        />
      </div>

      {/* LangChain Patterns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {patterns.map((pattern, idx) => {
          const Icon = pattern.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all"
            >
              <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${pattern.gradient} flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-2">{pattern.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{pattern.description}</p>
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-xs font-mono whitespace-pre-wrap">
                  {pattern.code}
                </pre>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Implementation Examples */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Real-World Implementations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-bold mb-2">Multi-Agent System</h3>
            <p className="text-sm text-gray-600 mb-3">
              This dashboard uses LangChain agents for intelligent query routing and task execution.
            </p>
            <div className="bg-gray-50 rounded p-3 text-sm">
              <div className="font-semibold">Features:</div>
              <ul className="list-disc list-inside text-gray-600 mt-1">
                <li>Specialized agent roles</li>
                <li>Intelligent routing</li>
                <li>Collaborative workflows</li>
                <li>Tool integration</li>
              </ul>
            </div>
          </div>
          <div>
            <h3 className="font-bold mb-2">RAG Pipeline</h3>
            <p className="text-sm text-gray-600 mb-3">
              Advanced retrieval with hybrid search combining semantic and keyword matching.
            </p>
            <div className="bg-gray-50 rounded p-3 text-sm">
              <div className="font-semibold">Features:</div>
              <ul className="list-disc list-inside text-gray-600 mt-1">
                <li>Vector embeddings</li>
                <li>BM25 keyword search</li>
                <li>Result re-ranking</li>
                <li>Metadata filtering</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Data Integration Examples */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4">Dataset Integration Examples</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 className="font-bold mb-2">Finance Data Analysis</h3>
            <DataTable data={financeData.slice(0, 20)} title="Sample Finance Data" maxRows={5} />
          </div>
          <div>
            <h3 className="font-bold mb-2">E-commerce Data Analysis</h3>
            <DataTable data={ecommerceData.slice(0, 20)} title="Sample E-commerce Data" maxRows={5} />
          </div>
        </div>
      </div>

      {/* Best Practices */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6">
        <h2 className="text-xl font-bold mb-4">LangChain Best Practices</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg p-4">
            <div className="font-semibold mb-2">Do&apos;s</div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Use proper error handling</li>
              <li>• Implement retry logic</li>
              <li>• Cache embeddings</li>
              <li>• Monitor token usage</li>
              <li>• Use streaming for long responses</li>
            </ul>
          </div>
          <div className="bg-white rounded-lg p-4">
            <div className="font-semibold mb-2">❌ Don&apos;ts</div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Don&apos;t hardcode API keys</li>
              <li>• Avoid blocking operations</li>
              <li>• Don&apos;t ignore rate limits</li>
              <li>• Avoid large context windows</li>
              <li>• Don&apos;t skip validation</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
