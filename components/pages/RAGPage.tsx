"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Upload, Search, FileText, Database, Sparkles, CheckCircle, Lightbulb } from "lucide-react";
import { useData } from "@/lib/DataContext";
import DataTable from "@/components/DataTable";
import MetricCard from "@/components/MetricCard";
import HelpGuide from "@/components/HelpGuide";

const exampleQueries = [
  "What are the top selling products?",
  "Show me transactions above $1000",
  "What's the fraud rate in our data?",
  "Which region has the highest revenue?",
];

export default function RAGPage() {
  const { financeData, ecommerceData } = useData();
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);
  const [documents] = useState([
    { id: 1, name: "Finance Dataset", type: "CSV", records: financeData.length, uploaded: new Date() },
    { id: 2, name: "E-commerce Dataset", type: "CSV", records: ecommerceData.length, uploaded: new Date() },
  ]);
  const [selectedStrategy, setSelectedStrategy] = useState<"semantic" | "keyword" | "hybrid">("hybrid");

  const handleSearch = () => {
    if (!query.trim()) return;
    setSearching(true);
    
    setTimeout(() => {
      // Simulate search results
      const matchingFinance = financeData.filter(r => 
        Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
      );
      const matchingEcommerce = ecommerceData.filter(r => 
        Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
      );

      const results = [
        {
          id: 1,
          document: "Finance Dataset",
          chunk: `Found ${matchingFinance.length} matching records in finance data. Key insights:\n• Average amount: $${(matchingFinance.reduce((sum, r) => sum + r.amount, 0) / matchingFinance.length || 0).toFixed(2)}\n• Fraud cases: ${matchingFinance.filter(r => r.is_fraud === 1).length}\n• Top category: ${matchingFinance.length > 0 ? Object.entries(matchingFinance.reduce((acc: any, r) => { acc[r.category] = (acc[r.category] || 0) + 1; return acc; }, {})).sort((a: any, b: any) => b[1] - a[1])[0]?.[0] : 'N/A'}`,
          score: 0.95,
          strategy: selectedStrategy,
          matches: matchingFinance.length,
        },
        {
          id: 2,
          document: "E-commerce Dataset",
          chunk: `Found ${matchingEcommerce.length} matching records in e-commerce data. Key insights:\n• Total revenue: $${(matchingEcommerce.reduce((sum, r) => sum + r.total_amount, 0) / 1000).toFixed(1)}K\n• Return rate: ${(matchingEcommerce.filter(r => r.returned === 1).length / matchingEcommerce.length * 100 || 0).toFixed(2)}%\n• Top product: ${matchingEcommerce.length > 0 ? Object.entries(matchingEcommerce.reduce((acc: any, r) => { acc[r.product] = (acc[r.product] || 0) + 1; return acc; }, {})).sort((a: any, b: any) => b[1] - a[1])[0]?.[0] : 'N/A'}`,
          score: 0.87,
          strategy: selectedStrategy,
          matches: matchingEcommerce.length,
        },
      ];
      setSearchResults(results);
      setSearching(false);
    }, 800);
  };

  const matchingFinance = financeData.filter(r => 
    Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
  ).length;

  const matchingEcommerce = ecommerceData.filter(r => 
    Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
  ).length;

  return (
    <div className="space-y-6" data-tour="rag">
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Advanced RAG</h1>
        <p className="text-gray-600">Hybrid search combining semantic and keyword matching</p>
      </div>

      {/* Help Guide */}
      <HelpGuide
        title="How to Use RAG Search"
        description="Learn how to query your documents effectively"
        steps={[
          {
            number: 1,
            title: "Review Available Documents",
            description: "Check the Document Library section to see what datasets are indexed and ready for search.",
            action: () => {
              const element = Array.from(document.querySelectorAll('h2')).find(el => el.textContent?.includes('Document Library'));
              element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            actionLabel: "View Documents"
          },
          {
            number: 2,
            title: "Choose Search Strategy",
            description: "Select Semantic (meaning-based), Keyword (exact match), or Hybrid (best of both). Hybrid is recommended for most queries.",
            action: () => {
              setSelectedStrategy("hybrid");
              const element = Array.from(document.querySelectorAll('label')).find(el => el.textContent?.includes('Search Strategy'));
              element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            actionLabel: "Set to Hybrid"
          },
          {
            number: 3,
            title: "Try Example Queries",
            description: "Click any example query below to see how RAG works, or type your own question.",
            action: () => {
              const firstExample = exampleQueries[0];
              setQuery(firstExample);
              setTimeout(() => handleSearch(), 100);
            },
            actionLabel: "Try Example"
          },
          {
            number: 4,
            title: "Review Search Results",
            description: "Results show matching documents with relevance scores, key insights, and data previews.",
          },
          {
            number: 5,
            title: "Refine Your Query",
            description: "Try different search strategies or rephrase your query to find more specific information.",
          }
        ]}
      />

      {/* Example Queries */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="w-5 h-5 text-purple-600" />
          <h3 className="font-bold text-gray-900">Try These Example Queries:</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {exampleQueries.map((example, idx) => (
            <button
              key={idx}
              onClick={() => {
                setQuery(example);
                setTimeout(() => handleSearch(), 100);
              }}
              className="px-4 py-2 bg-white rounded-lg hover:shadow-md transition-all border border-gray-200 hover:border-purple-300 text-sm"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Document Management */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Database className="w-6 h-6 text-purple-600" />
            <h2 className="text-xl font-bold">Document Library</h2>
          </div>
          <button className="px-4 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Upload Document
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {documents.map((doc) => (
            <div key={doc.id} className="border border-gray-200 rounded-lg p-4 hover:border-purple-500 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-blue-600" />
                  <span className="font-semibold">{doc.name}</span>
                </div>
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>
              <div className="text-sm text-gray-600">
                <div>Type: {doc.type}</div>
                <div>Records: {doc.records.toLocaleString()}</div>
                <div>Uploaded: {doc.uploaded.toLocaleDateString()}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Search Interface */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">Search Strategy</label>
          <div className="flex gap-2">
            {[
              { id: "semantic", label: "Semantic", icon: Sparkles },
              { id: "keyword", label: "Keyword", icon: Search },
              { id: "hybrid", label: "Hybrid", icon: Database },
            ].map((strategy) => {
              const Icon = strategy.icon;
              return (
                <button
                  key={strategy.id}
                  onClick={() => setSelectedStrategy(strategy.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                    selectedStrategy === strategy.id
                      ? "bg-purple-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {strategy.label}
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
            placeholder="Query your documents..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
          />
          <button
            onClick={handleSearch}
            disabled={searching}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            {searching ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Searching...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                Search
              </>
            )}
          </button>
        </div>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Search Results</h2>
            <div className="flex gap-4">
              <MetricCard
                title="Finance Matches"
                value={matchingFinance}
                gradient="from-pink-500 to-rose-500"
              />
              <MetricCard
                title="E-commerce Matches"
                value={matchingEcommerce}
                gradient="from-blue-500 to-cyan-500"
              />
            </div>
          </div>
          {searchResults.map((result) => (
            <div key={result.id} className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-purple-600" />
                  <span className="font-semibold">{result.document}</span>
                  <span className="text-xs text-gray-500">({result.matches} matches)</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Score: {(result.score * 100).toFixed(0)}%</span>
                  <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">
                    {result.strategy}
                  </span>
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="whitespace-pre-wrap text-gray-700 text-sm">{result.chunk}</pre>
              </div>
            </div>
          ))}
        </motion.div>
      )}

      {/* Data Preview */}
      {query && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DataTable
            data={financeData.filter(r => 
              Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
            ).slice(0, 50)}
            title="Finance Search Results"
            maxRows={5}
          />
          <DataTable
            data={ecommerceData.filter(r => 
              Object.values(r).some(v => String(v).toLowerCase().includes(query.toLowerCase()))
            ).slice(0, 50)}
            title="E-commerce Search Results"
            maxRows={5}
          />
        </div>
      )}

      {/* Strategy Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <FileText className="w-8 h-8 text-green-600 mb-3" />
          <h3 className="font-bold mb-2">Semantic Search</h3>
          <p className="text-sm text-gray-600 mb-3">Vector-based similarity search using embeddings</p>
          <div className="text-xs text-gray-500">
            • Uses cosine similarity<br />
            • Understands context and meaning<br />
            • Best for conceptual queries
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-6">
          <Search className="w-8 h-8 text-blue-600 mb-3" />
          <h3 className="font-bold mb-2">Keyword Search</h3>
          <p className="text-sm text-gray-600 mb-3">BM25 keyword matching algorithm</p>
          <div className="text-xs text-gray-500">
            • Fast exact matching<br />
            • Term frequency weighting<br />
            • Best for specific terms
          </div>
        </div>
      </div>
    </div>
  );
}
