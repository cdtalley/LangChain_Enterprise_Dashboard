"use client";

import { useState } from "react";
import { Download, ChevronLeft, ChevronRight } from "lucide-react";

interface DataTableProps {
  data: any[];
  title?: string;
  maxRows?: number;
}

export default function DataTable({ data, title, maxRows = 10 }: DataTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <p className="text-gray-500 text-center">No data available</p>
      </div>
    );
  }

  const filteredData = data.filter((row) =>
    Object.values(row).some((val) =>
      String(val).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const totalPages = Math.ceil(filteredData.length / maxRows);
  const startIdx = (currentPage - 1) * maxRows;
  const endIdx = startIdx + maxRows;
  const paginatedData = filteredData.slice(startIdx, endIdx);

  const columns = Object.keys(data[0]);

  const handleExport = (format: "csv" | "json") => {
    let content = "";
    let mimeType = "";
    let filename = `${title || "data"}.${format}`;

    if (format === "csv") {
      const headers = columns.join(",");
      const rows = filteredData.map((row) =>
        columns.map((col) => `"${row[col]}"`).join(",")
      );
      content = [headers, ...rows].join("\n");
      mimeType = "text/csv";
    } else {
      content = JSON.stringify(filteredData, null, 2);
      mimeType = "application/json";
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
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {(title || searchTerm !== "") && (
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          {title && <h3 className="font-bold text-gray-900">{title}</h3>}
          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              className="px-3 py-1 border border-gray-300 rounded-lg text-sm"
            />
            <button
              onClick={() => handleExport("csv")}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm flex items-center gap-1"
            >
              <Download className="w-4 h-4" />
              CSV
            </button>
            <button
              onClick={() => handleExport("json")}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm flex items-center gap-1"
            >
              <Download className="w-4 h-4" />
              JSON
            </button>
          </div>
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {col.replace(/_/g, " ")}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((row, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                {columns.map((col) => (
                  <td key={col} className="px-4 py-3 text-sm text-gray-900">
                    {typeof row[col] === "number"
                      ? row[col].toLocaleString()
                      : String(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="p-4 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Showing {startIdx + 1} to {Math.min(endIdx, filteredData.length)} of{" "}
            {filteredData.length} entries
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-gray-300 rounded-lg disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-sm text-gray-600">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-gray-300 rounded-lg disabled:opacity-50"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

