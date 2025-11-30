"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import DemoDataGenerator from "./demo-data-generator";

interface DataContextType {
  financeData: any[];
  ecommerceData: any[];
  marketingData: any[];
  hrData: any[];
  healthcareData: any[];
  isLoading: boolean;
  refreshData: () => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: ReactNode }) {
  const [financeData, setFinanceData] = useState<any[]>([]);
  const [ecommerceData, setEcommerceData] = useState<any[]>([]);
  const [marketingData, setMarketingData] = useState<any[]>([]);
  const [hrData, setHrData] = useState<any[]>([]);
  const [healthcareData, setHealthcareData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const generator = new DemoDataGenerator();

  const loadData = () => {
    setIsLoading(true);
    // Generate larger, more impressive datasets
    setTimeout(() => {
      setFinanceData(generator.generateFinanceData(3000));
      setEcommerceData(generator.generateEcommerceData(2500));
      setMarketingData(generator.generateMarketingData(2000));
      setHrData(generator.generateHRData(2000));
      setHealthcareData(generator.generateHealthcareData(1500));
      setIsLoading(false);
    }, 500);
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <DataContext.Provider
      value={{
        financeData,
        ecommerceData,
        marketingData,
        hrData,
        healthcareData,
        isLoading,
        refreshData: loadData,
      }}
    >
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error("useData must be used within DataProvider");
  }
  return context;
}

