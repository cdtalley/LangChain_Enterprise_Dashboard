"use client";

import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
  className?: string;
}

export default function ChartCard({
  title,
  subtitle,
  children,
  className,
}: ChartCardProps) {
  return (
    <div
      className={cn(
        "chart-card overflow-hidden p-6",
        className
      )}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && (
            <h3 className="text-lg font-semibold tracking-tight text-[var(--foreground)]">
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="text-sm text-[var(--muted)] mt-0.5">{subtitle}</p>
          )}
        </div>
      )}
      <div className="relative min-h-[280px]">{children}</div>
    </div>
  );
}
