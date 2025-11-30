"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import Tour, { TourStep } from "@/components/Tour";
import { getTourSteps } from "@/lib/tour-steps";
import { useRouter } from "next/navigation";

interface TourContextType {
  startTour: () => void;
  stopTour: () => void;
  isTourActive: boolean;
}

const TourContext = createContext<TourContextType | undefined>(undefined);

export function TourProvider({ children }: { children: ReactNode }) {
  const [isTourActive, setIsTourActive] = useState(false);
  const router = useRouter();

  const startTour = () => {
    setIsTourActive(true);
  };

  const stopTour = () => {
    setIsTourActive(false);
  };

  const handleTourComplete = () => {
    setIsTourActive(false);
  };

  const handleTourSkip = () => {
    setIsTourActive(false);
  };

  // Enhanced tour steps with navigation actions
  const getEnhancedSteps = (): TourStep[] => {
    const steps = getTourSteps();
    
    // Add navigation actions for specific steps
    return steps.map((step) => {
      const enhancedStep = { ...step };
      
      // Add navigation actions
      switch (step.id) {
        case "multi-agent":
          enhancedStep.action = () => router.push("/multi-agent");
          break;
        case "rag":
          enhancedStep.action = () => router.push("/rag");
          break;
        case "tools":
          enhancedStep.action = () => router.push("/tools");
          break;
        case "analytics":
          enhancedStep.action = () => router.push("/analytics");
          break;
        case "demo":
          enhancedStep.action = () => router.push("/demo");
          break;
        case "registry":
          enhancedStep.action = () => router.push("/registry");
          break;
        case "ab-testing":
          enhancedStep.action = () => router.push("/ab-testing");
          break;
        case "experiments":
          enhancedStep.action = () => router.push("/experiments");
          break;
        case "monitoring":
          enhancedStep.action = () => router.push("/monitoring");
          break;
        case "fine-tuning":
          enhancedStep.action = () => router.push("/fine-tuning");
          break;
        case "datasets":
          enhancedStep.action = () => router.push("/datasets");
          break;
        case "profiling":
          enhancedStep.action = () => router.push("/profiling");
          break;
        case "statistics":
          enhancedStep.action = () => router.push("/statistics");
          break;
        case "automl":
          enhancedStep.action = () => router.push("/automl");
          break;
        case "time-series":
          enhancedStep.action = () => router.push("/time-series");
          break;
        case "ensembling":
          enhancedStep.action = () => router.push("/ensembling");
          break;
        case "langchain":
          enhancedStep.action = () => router.push("/langchain");
          break;
        case "welcome":
        case "sidebar":
        case "welcome-page":
        case "complete":
          enhancedStep.action = () => router.push("/");
          break;
      }
      
      return enhancedStep;
    });
  };

  return (
    <TourContext.Provider value={{ startTour, stopTour, isTourActive }}>
      {children}
      {isTourActive && (
        <Tour
          steps={getEnhancedSteps()}
          onComplete={handleTourComplete}
          onSkip={handleTourSkip}
        />
      )}
    </TourContext.Provider>
  );
}

export function useTour() {
  const context = useContext(TourContext);
  if (context === undefined) {
    throw new Error("useTour must be used within a TourProvider");
  }
  return context;
}

