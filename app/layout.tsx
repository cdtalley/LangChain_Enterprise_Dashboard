import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { DataProvider } from "@/lib/DataContext";
import { TourProvider } from "@/lib/TourContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Enterprise LangChain AI Workbench",
  description: "Advanced LLM Orchestration & Multi-Agent Collaboration Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <DataProvider>
          <TourProvider>{children}</TourProvider>
        </DataProvider>
      </body>
    </html>
  );
}
