"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronRight, ChevronLeft, CheckCircle } from "lucide-react";

export interface TourStep {
  id: string;
  target: string; // CSS selector or element ID
  title: string;
  content: string;
  position?: "top" | "bottom" | "left" | "right" | "center";
  action?: () => void; // Optional action to perform before showing step
}

interface TourProps {
  steps: TourStep[];
  onComplete?: () => void;
  onSkip?: () => void;
}

export default function Tour({ steps, onComplete, onSkip }: TourProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const [targetElement, setTargetElement] = useState<HTMLElement | null>(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const [tooltipPosition, setTooltipPosition] = useState<"top" | "bottom" | "left" | "right" | "center">("bottom");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const findElement = useCallback((selector: string, retries = 10): Promise<HTMLElement | null> => {
    return new Promise((resolve) => {
      let attempts = 0;
      const tryFind = () => {
        attempts++;
        let element: HTMLElement | null = null;

        // Try different selector formats
        if (selector.startsWith("#")) {
          element = document.getElementById(selector.substring(1));
        } else if (selector.startsWith(".")) {
          element = document.querySelector(selector) as HTMLElement;
        } else if (selector.startsWith("[data-tour")) {
          // Handle data-tour attribute
          element = document.querySelector(selector) as HTMLElement;
        } else {
          // Try as data-tour attribute
          element = document.querySelector(`[data-tour="${selector}"]`) as HTMLElement;
          if (!element) {
            // Try as regular selector
            element = document.querySelector(selector) as HTMLElement;
          }
        }

        if (element) {
          resolve(element);
        } else if (attempts < retries) {
          setTimeout(tryFind, 200);
        } else {
          resolve(null);
        }
      };
      tryFind();
    });
  }, []);

  const updateTargetPosition = useCallback(async () => {
    const step = steps[currentStep];
    if (!step) return;

    // Execute action if provided (navigation)
    if (step.action) {
      step.action();
      // Wait longer for navigation to complete
      await new Promise(resolve => setTimeout(resolve, 600));
    }

    // Find element with retries
    const element = await findElement(step.target, 15);
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    if (element) {
      setTargetElement(element);
      
      // Wait a bit for layout to settle
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const rect = element.getBoundingClientRect();
      const scrollY = window.scrollY || window.pageYOffset;
      const scrollX = window.scrollX || window.pageXOffset;

      const stepPosition = step.position || "bottom";
      setTooltipPosition(stepPosition);
      
      let top = 0;
      let left = 0;

      switch (stepPosition) {
        case "top":
          top = rect.top + scrollY - 10;
          left = rect.left + scrollX + rect.width / 2;
          break;
        case "bottom":
          top = rect.bottom + scrollY + 20;
          left = rect.left + scrollX + rect.width / 2;
          break;
        case "left":
          top = rect.top + scrollY + rect.height / 2;
          left = rect.left + scrollX - 10;
          break;
        case "right":
          top = rect.top + scrollY + rect.height / 2;
          left = rect.right + scrollX + 20;
          break;
        case "center":
          top = viewportHeight / 2 + scrollY;
          left = viewportWidth / 2;
          break;
      }

      // Ensure tooltip stays on screen
      const tooltipWidth = 400; // max-w-md
      const tooltipHeight = 200; // approximate
      
      if (left < tooltipWidth / 2) {
        left = tooltipWidth / 2 + 20;
      } else if (left > viewportWidth - tooltipWidth / 2) {
        left = viewportWidth - tooltipWidth / 2 - 20;
      }
      
      if (top < tooltipHeight / 2) {
        top = tooltipHeight / 2 + 20;
      } else if (top > viewportHeight + scrollY - tooltipHeight / 2) {
        top = viewportHeight + scrollY - tooltipHeight / 2 - 20;
      }

      setPosition({ top, left });
      
      // Scroll element into view smoothly
      element.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    } else {
      // Center if element not found
      setPosition({
        top: viewportHeight / 2,
        left: viewportWidth / 2,
      });
      setTargetElement(null);
    }
  }, [currentStep, steps, findElement]);

  useEffect(() => {
    if (steps.length > 0 && isVisible) {
      // Clear any existing timeout
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      
      // Small delay to ensure DOM is ready
      timeoutRef.current = setTimeout(() => {
        updateTargetPosition();
      }, 100);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [currentStep, steps, isVisible, updateTargetPosition]);

  useEffect(() => {
    if (!isVisible) return;

    const handleResize = () => {
      updateTargetPosition();
    };
    
    const handleScroll = () => {
      updateTargetPosition();
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("scroll", handleScroll, true);
    
    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("scroll", handleScroll, true);
    };
  }, [isVisible, updateTargetPosition]);

  useEffect(() => {
    if (steps.length > 0) {
      setIsVisible(true);
    }
  }, [steps.length]);

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      completeTour();
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const completeTour = () => {
    setIsVisible(false);
    setCurrentStep(0);
    if (onComplete) onComplete();
  };

  const skipTour = () => {
    setIsVisible(false);
    setCurrentStep(0);
    if (onSkip) onSkip();
  };

  if (!isVisible || steps.length === 0) return null;

  const step = steps[currentStep];
  if (!step) return null;

  const progress = ((currentStep + 1) / steps.length) * 100;

  // Calculate highlight position
  const highlightStyle = targetElement
    ? (() => {
        const rect = targetElement.getBoundingClientRect();
        return {
          top: `${rect.top - 4}px`,
          left: `${rect.left - 4}px`,
          width: `${rect.width + 8}px`,
          height: `${rect.height + 8}px`,
        };
      })()
    : null;

  return (
    <>
      {/* Overlay */}
      <AnimatePresence>
        {isVisible && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 z-[9998]"
              onClick={skipTour}
            />
            
            {/* Highlight overlay with cutout */}
            {targetElement && highlightStyle && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed z-[9999] pointer-events-none border-2 border-purple-500 rounded-lg"
                style={{
                  ...highlightStyle,
                  boxShadow: "0 0 0 9999px rgba(0, 0, 0, 0.5)",
                }}
              />
            )}

            {/* Tour Tooltip */}
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="fixed z-[10000] bg-white rounded-xl shadow-2xl max-w-md p-6"
              style={{
                top: `${position.top}px`,
                left: `${position.left}px`,
                transform: "translate(-50%, 0)",
                maxWidth: "min(400px, 90vw)",
              }}
            >
              {/* Close button */}
              <button
                onClick={skipTour}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              {/* Progress bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
                  <span>Step {currentStep + 1} of {steps.length}</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>

              {/* Content */}
              <div className="mb-4 pr-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{step.title}</h3>
                <p className="text-gray-600 leading-relaxed text-sm">{step.content}</p>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between">
                <button
                  onClick={skipTour}
                  className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors text-sm"
                >
                  Skip Tour
                </button>
                <div className="flex gap-2">
                  {currentStep > 0 && (
                    <button
                      onClick={prevStep}
                      className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors flex items-center gap-2 text-sm"
                    >
                      <ChevronLeft className="w-4 h-4" />
                      Previous
                    </button>
                  )}
                  <button
                    onClick={nextStep}
                    className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all flex items-center gap-2 font-semibold text-sm"
                  >
                    {currentStep === steps.length - 1 ? (
                      <>
                        Complete
                        <CheckCircle className="w-4 h-4" />
                      </>
                    ) : (
                      <>
                        Next
                        <ChevronRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
