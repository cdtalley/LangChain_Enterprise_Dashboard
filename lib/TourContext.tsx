"use client";

import { createContext, useContext, useState, ReactNode, useMemo, useCallback } from "react";
import Tour, { TourStep } from "@/components/Tour";
import { getTourSteps } from "@/lib/tour-steps";

interface TourContextType {
  startTour: () => void;
  stopTour: () => void;
  isTourActive: boolean;
  setNavigationHandler: (handler: (path: string) => void) => void;
}

const TourContext = createContext<TourContextType | undefined>(undefined);

// Store navigation handler outside component to avoid re-renders
let navigationHandler: ((path: string) => void) | null = null;

export function TourProvider({ children }: { children: ReactNode }) {
  const [isTourActive, setIsTourActive] = useState(false);
  
  const setNavigationHandler = useCallback((handler: (path: string) => void) => {
    navigationHandler = handler;
  }, []);

  const startTour = useCallback(() => {
    // Small delay to ensure DOM is ready
    setTimeout(() => {
      setIsTourActive(true);
    }, 100);
  }, []);

  const stopTour = useCallback(() => {
    setIsTourActive(false);
  }, []);

  const handleTourComplete = useCallback(() => {
    setIsTourActive(false);
  }, []);

  const handleTourSkip = useCallback(() => {
    setIsTourActive(false);
  }, []);

  // Get enhanced tour steps with navigation actions
  // Recreate steps when tour is active to ensure handler is current
  const enhancedSteps = useMemo((): TourStep[] => {
    const steps = getTourSteps();
    
    // Add navigation actions for specific steps
    return steps.map((step) => {
      const enhancedStep = { ...step };
      
      // Add navigation actions using the app's navigation handler
      switch (step.id) {
        case "multi-agent":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/multi-agent");
          };
          break;
        case "rag":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/rag");
          };
          break;
        case "tools":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/tools");
          };
          break;
        case "analytics":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/analytics");
          };
          break;
        case "demo":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/demo");
          };
          break;
        case "registry":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/registry");
          };
          break;
        case "ab-testing":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/ab-testing");
          };
          break;
        case "experiments":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/experiments");
          };
          break;
        case "monitoring":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/monitoring");
          };
          break;
        case "fine-tuning":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/fine-tuning");
          };
          break;
        case "datasets":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/datasets");
          };
          break;
        case "profiling":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/profiling");
          };
          break;
        case "statistics":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/statistics");
          };
          break;
        case "automl":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/automl");
          };
          break;
        case "time-series":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/time-series");
          };
          break;
        case "ensembling":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/ensembling");
          };
          break;
        case "langchain":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/langchain");
          };
          break;
        case "welcome":
        case "sidebar":
        case "welcome-page":
        case "complete":
          enhancedStep.action = () => {
            if (navigationHandler) navigationHandler("/");
          };
          break;
      }
      
      return enhancedStep;
    });
  }, [isTourActive]); // Recreate when tour becomes active

  return (
    <TourContext.Provider value={{ startTour, stopTour, isTourActive, setNavigationHandler }}>
      {children}
      {isTourActive && enhancedSteps.length > 0 && (
        <Tour
          steps={enhancedSteps}
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

