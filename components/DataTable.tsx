"use client";

import { useState } from "react";
import { Download, ChevronLeft, ChevronRight, Database, Search } from "lucide-react";
import { cn } from "@/lib/utils";

const HUMANIZED_COLUMNS: Record<string, string> = {
  order_date: "Order date",
  total_amount: "Total amount",
  is_fraud: "Fraud flag",
  amount: "Amount",
  date: "Date",
  category: "Category",
  product: "Product",
  region: "Region",
  returned: "Returned",
  channel: "Channel",
  spend: "Spend",
  revenue: "Revenue",
  roas: "ROAS",
  salary: "Salary",
};

function humanizeColumn(key: string): string {
  const lower = key.toLowerCase();
  if (HUMANIZED_COLUMNS[lower]) return HUMANIZED_COLUMNS[lower];
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

interface DataTableProps {
  data: any[];
  title?: string;
  maxRows?: number;
}

export default function DataTable({ data, title, maxRows = 10 }: DataTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");

  const columns = data?.[0] ? Object.keys(data[0]) : [];
  const filteredData =
    !data || data.length === 0
      ? []
      : data.filter((row) =>
          Object.values(row).some((val) =>
            String(val).toLowerCase().includes(searchTerm.toLowerCase())
          )
        );

  const totalPages = Math.ceil(filteredData.length / maxRows);
  const startIdx = (currentPage - 1) * maxRows;
  const endIdx = startIdx + maxRows;
  const paginatedData = filteredData.slice(startIdx, endIdx);

  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-white shadow-[var(--shadow-md)] p-8 text-center">
        <div className="inline-flex w-12 h-12 rounded-xl bg-slate-100 items-center justify-center mb-3">
          <Database className="w-6 h-6 text-[var(--muted)]" />
        </div>
        <p className="text-[var(--foreground)] font-medium">No data available</p>
        <p className="text-sm text-[var(--muted)] mt-1">This dataset is empty or still loading.</p>
      </div>
    );
  }

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

  const isEmptyFiltered = filteredData.length === 0 && searchTerm !== "";

  return (
    <div className="rounded-xl border border-[var(--border)] bg-white shadow-[var(--shadow-md)] overflow-hidden">
      <div className="p-4 border-b border-[var(--border)] flex flex-wrap items-center justify-between gap-3">
        {title && (
          <h3 className="text-base font-semibold text-[var(--foreground)]">{title}</h3>
        )}
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--muted)]" />
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              className="pl-8 pr-3 py-2 border border-[var(--border)] rounded-xl text-sm w-40 focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/20 focus:border-[var(--primary)]"
              aria-label="Search table"
            />
          </div>
          <button
            type="button"
            onClick={() => handleExport("csv")}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium bg-[var(--primary)] text-white hover:opacity-90 transition-opacity"
          >
            <Download className="w-4 h-4" />
            CSV
          </button>
          <button
            type="button"
            onClick={() => handleExport("json")}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium border border-[var(--border)] text-[var(--foreground)] hover:bg-slate-50 transition-colors"
          >
            <Download className="w-4 h-4" />
            JSON
          </button>
        </div>
      </div>
      {isEmptyFiltered ? (
        <div className="p-8 text-center">
          <p className="text-[var(--muted)]">No rows match &quot;{searchTerm}&quot;</p>
          <button
            type="button"
            onClick={() => setSearchTerm("")}
            className="mt-2 text-sm font-medium text-[var(--primary)] hover:underline"
          >
            Clear search
          </button>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[var(--border)]">
              <thead className="bg-slate-50/80">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col}
                      className="px-4 py-3 text-left text-xs font-semibold text-[var(--muted)] uppercase tracking-wider"
                    >
                      {humanizeColumn(col)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-[var(--border)]">
                {paginatedData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                    {columns.map((col) => (
                      <td key={col} className="px-4 py-3 text-sm text-[var(--foreground)]">
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
            <div className="p-4 border-t border-[var(--border)] flex flex-wrap items-center justify-between gap-3">
              <div className="text-sm text-[var(--muted)]">
                Showing {startIdx + 1}–{Math.min(endIdx, filteredData.length)} of {filteredData.length}
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className={cn(
                    "p-2 rounded-lg border border-[var(--border)] transition-colors",
                    currentPage === 1 ? "opacity-50 cursor-not-allowed" : "hover:bg-slate-50"
                  )}
                  aria-label="Previous page"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="text-sm text-[var(--muted)] min-w-[4rem] text-center">
                  {currentPage} / {totalPages}
                </span>
                <button
                  type="button"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className={cn(
                    "p-2 rounded-lg border border-[var(--border)] transition-colors",
                    currentPage === totalPages ? "opacity-50 cursor-not-allowed" : "hover:bg-slate-50"
                  )}
                  aria-label="Next page"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

