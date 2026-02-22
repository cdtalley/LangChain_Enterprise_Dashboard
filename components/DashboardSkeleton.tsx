"use client";

export default function DashboardSkeleton() {
  return (
    <div className="space-y-10 animate-pulse">
      {/* Hero placeholder */}
      <div className="rounded-2xl bg-slate-200/60 h-64 md:h-80" />

      {/* Stats row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="rounded-xl border border-[var(--border)] bg-white p-6 h-[140px]"
          >
            <div className="flex justify-between mb-4">
              <div className="w-11 h-11 rounded-xl bg-slate-200" />
              <div className="h-6 w-12 rounded-lg bg-slate-100" />
            </div>
            <div className="h-8 w-20 bg-slate-200 rounded mb-2" />
            <div className="h-4 w-28 bg-slate-100 rounded" />
          </div>
        ))}
      </div>

      {/* Executive summary block */}
      <div className="rounded-2xl border border-[var(--border)] bg-white/80 p-6 md:p-8">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-6 h-6 rounded bg-slate-200" />
          <div className="h-7 w-48 bg-slate-200 rounded" />
          <div className="h-5 w-16 rounded-full bg-slate-100" />
        </div>
        <div className="h-4 w-full max-w-2xl bg-slate-100 rounded mb-6" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="rounded-xl bg-gradient-to-br from-slate-100 to-slate-50 h-32"
            />
          ))}
        </div>
        <div className="pt-6 border-t border-[var(--border)]">
          <div className="h-5 w-64 bg-slate-100 rounded mb-4" />
          <div className="h-[200px] w-full bg-slate-100 rounded-xl" />
        </div>
      </div>
    </div>
  );
}
