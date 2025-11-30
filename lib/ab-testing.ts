/**
 * A/B Testing Framework - TypeScript Port
 * Statistical significance testing with sample size calculation
 */

import { PersistenceManager, STORAGE_KEYS } from "./persistence";

export enum ExperimentStatus {
  DRAFT = "draft",
  RUNNING = "running",
  PAUSED = "paused",
  COMPLETED = "completed",
  STOPPED = "stopped",
}

export enum MetricType {
  CONTINUOUS = "continuous",
  BINARY = "binary",
  COUNT = "count",
}

export interface ExperimentConfig {
  name: string;
  description: string;
  hypothesis: string;
  metricName: string;
  metricType: MetricType;
  baselineModel: string;
  treatmentModel: string;
  trafficSplit: number; // 0.0-1.0
  minSampleSize: number;
  maxDurationDays: number;
  significanceLevel: number;
  power?: number;
}

export interface ExperimentEvent {
  experimentId: string;
  userId: string;
  variant: "baseline" | "treatment";
  metricValue: number;
  timestamp: string; // ISO string for serialization
}

export interface ExperimentResult {
  experimentId: string;
  baselineMean: number;
  treatmentMean: number;
  baselineCount: number;
  treatmentCount: number;
  pValue: number;
  isSignificant: boolean;
  effectSize: number;
  relativeLift: number;
  recommendation: string;
  confidenceInterval: [number, number];
}

export interface Experiment {
  id: string;
  config: ExperimentConfig;
  status: ExperimentStatus;
  createdAt: string; // ISO string
  startedAt?: string; // ISO string
  completedAt?: string; // ISO string
  events: ExperimentEvent[];
  result?: ExperimentResult;
}

class ABTestingFramework {
  private experiments: Map<string, Experiment> = new Map();
  private nextId = 1;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    try {
      const saved = PersistenceManager.load<Experiment[]>(STORAGE_KEYS.AB_TESTING, []);
      saved.forEach(exp => {
        this.experiments.set(exp.id, exp);
        // Update nextId to avoid conflicts
        const idNum = parseInt(exp.id.replace("exp-", ""));
        if (idNum >= this.nextId) {
          this.nextId = idNum + 1;
        }
      });
    } catch (error) {
      console.error("Failed to load experiments from storage:", error);
    }
  }

  private saveToStorage(): void {
    const experiments = Array.from(this.experiments.values());
    PersistenceManager.save(STORAGE_KEYS.AB_TESTING, experiments);
  }

  createExperiment(config: ExperimentConfig): string {
    const id = `exp-${this.nextId++}`;
    const experiment: Experiment = {
      id,
      config,
      status: ExperimentStatus.DRAFT,
      createdAt: new Date().toISOString(),
      events: [],
    };
    this.experiments.set(id, experiment);
    this.saveToStorage();
    return id;
  }

  startExperiment(experimentId: string): void {
    const exp = this.experiments.get(experimentId);
    if (exp) {
      exp.status = ExperimentStatus.RUNNING;
      exp.startedAt = new Date().toISOString();
      this.saveToStorage();
    }
  }

  recordEvent(experimentId: string, userId: string, metricValue: number): void {
    const exp = this.experiments.get(experimentId);
    if (!exp || exp.status !== ExperimentStatus.RUNNING) return;

    // Consistent hashing for traffic splitting
    const hash = this.hashUserId(userId);
    const variant = hash < exp.config.trafficSplit ? "treatment" : "baseline";

    const event: ExperimentEvent = {
      experimentId,
      userId,
      variant,
      metricValue,
      timestamp: new Date().toISOString(),
    };

    exp.events.push(event);
    this.saveToStorage();
  }

  private hashUserId(userId: string): number {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = ((hash << 5) - hash) + userId.charCodeAt(i);
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash) / 2147483647; // Normalize to 0-1
  }

  analyzeExperiment(experimentId: string): ExperimentResult | null {
    const exp = this.experiments.get(experimentId);
    if (!exp || exp.events.length === 0) return null;

    const baselineEvents = exp.events.filter(e => e.variant === "baseline");
    const treatmentEvents = exp.events.filter(e => e.variant === "treatment");

    if (baselineEvents.length === 0 || treatmentEvents.length === 0) return null;

    const baselineValues = baselineEvents.map(e => e.metricValue);
    const treatmentValues = treatmentEvents.map(e => e.metricValue);

    const baselineMean = this.mean(baselineValues);
    const treatmentMean = this.mean(treatmentValues);

    let pValue = 1.0;
    let isSignificant = false;

    // Statistical test based on metric type
    if (exp.config.metricType === MetricType.CONTINUOUS) {
      pValue = this.tTest(baselineValues, treatmentValues);
    } else if (exp.config.metricType === MetricType.BINARY) {
      pValue = this.chiSquareTest(baselineValues, treatmentValues);
    } else {
      pValue = this.mannWhitneyTest(baselineValues, treatmentValues);
    }

    isSignificant = pValue < exp.config.significanceLevel;

    const effectSize = treatmentMean - baselineMean;
    const relativeLift = baselineMean !== 0 ? (effectSize / baselineMean) * 100 : 0;

    const stdError = Math.sqrt(
      (this.variance(baselineValues) / baselineValues.length) +
      (this.variance(treatmentValues) / treatmentValues.length)
    );
    const zScore = 1.96; // 95% confidence
    const margin = zScore * stdError;
    const confidenceInterval: [number, number] = [
      effectSize - margin,
      effectSize + margin,
    ];

    let recommendation = "Continue experiment";
    if (isSignificant && effectSize > 0) {
      recommendation = "Treatment is significantly better - Consider deploying";
    } else if (isSignificant && effectSize < 0) {
      recommendation = "Baseline is significantly better - Stop experiment";
    } else if (exp.events.length >= exp.config.minSampleSize) {
      recommendation = "No significant difference - Consider stopping";
    }

    const result: ExperimentResult = {
      experimentId,
      baselineMean,
      treatmentMean,
      baselineCount: baselineValues.length,
      treatmentCount: treatmentValues.length,
      pValue,
      isSignificant,
      effectSize,
      relativeLift,
      recommendation,
      confidenceInterval,
    };

    exp.result = result;
    this.saveToStorage();
    return result;
  }

  calculateSampleSize(
    baselineMean: number,
    expectedLift: number,
    significanceLevel: number = 0.05,
    power: number = 0.80
  ): number {
    const treatmentMean = baselineMean * (1 + expectedLift);
    const pooledStd = baselineMean * 0.1; // Assume 10% std dev

    const zAlpha = 1.96; // For alpha = 0.05
    const zBeta = 0.84; // For power = 0.80

    const effectSize = Math.abs(treatmentMean - baselineMean) / pooledStd;
    const n = Math.pow(zAlpha + zBeta, 2) * 2 * Math.pow(pooledStd, 2) / Math.pow(effectSize, 2);

    return Math.ceil(n);
  }

  private mean(values: number[]): number {
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  }

  private variance(values: number[]): number {
    const m = this.mean(values);
    const squaredDiffs = values.map(val => Math.pow(val - m, 2));
    return this.mean(squaredDiffs);
  }

  private tTest(group1: number[], group2: number[]): number {
    // Simplified t-test implementation
    const mean1 = this.mean(group1);
    const mean2 = this.mean(group2);
    const var1 = this.variance(group1);
    const var2 = this.variance(group2);
    const n1 = group1.length;
    const n2 = group2.length;

    const pooledStd = Math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2));
    const standardError = pooledStd * Math.sqrt(1 / n1 + 1 / n2);
    const tStatistic = (mean1 - mean2) / standardError;

    // Approximate p-value (simplified - in production use proper t-distribution)
    const pValue = 2 * (1 - this.normalCDF(Math.abs(tStatistic)));

    return Math.max(0, Math.min(1, pValue));
  }

  private chiSquareTest(group1: number[], group2: number[]): number {
    // Chi-square test for proportions
    const success1 = group1.filter(v => v === 1).length;
    const success2 = group2.filter(v => v === 1).length;
    const total1 = group1.length;
    const total2 = group2.length;

    const p1 = success1 / total1;
    const p2 = success2 / total2;
    const pPooled = (success1 + success2) / (total1 + total2);

    const z = (p1 - p2) / Math.sqrt(pPooled * (1 - pPooled) * (1 / total1 + 1 / total2));
    const pValue = 2 * (1 - this.normalCDF(Math.abs(z)));

    return Math.max(0, Math.min(1, pValue));
  }

  private mannWhitneyTest(group1: number[], group2: number[]): number {
    // Simplified Mann-Whitney U test
    const combined = [...group1.map((v, i) => ({ value: v, group: 1, index: i })),
                      ...group2.map((v, i) => ({ value: v, group: 2, index: i }))];
    combined.sort((a, b) => a.value - b.value);

    let rankSum1 = 0;
    combined.forEach((item, idx) => {
      if (item.group === 1) {
        rankSum1 += idx + 1;
      }
    });

    const n1 = group1.length;
    const n2 = group2.length;
    const u1 = rankSum1 - (n1 * (n1 + 1)) / 2;
    const u2 = n1 * n2 - u1;
    const u = Math.min(u1, u2);

    const meanU = (n1 * n2) / 2;
    const stdU = Math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12);
    const z = (u - meanU) / stdU;

    const pValue = 2 * (1 - this.normalCDF(Math.abs(z)));
    return Math.max(0, Math.min(1, pValue));
  }

  private normalCDF(x: number): number {
    // Approximation of standard normal CDF
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2.0);

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

    return 0.5 * (1.0 + sign * y);
  }

  getExperiment(experimentId: string): Experiment | undefined {
    return this.experiments.get(experimentId);
  }

  getAllExperiments(): Experiment[] {
    return Array.from(this.experiments.values());
  }

  stopExperiment(experimentId: string): void {
    const exp = this.experiments.get(experimentId);
    if (exp) {
      exp.status = ExperimentStatus.COMPLETED;
      exp.completedAt = new Date().toISOString();
      this.saveToStorage();
    }
  }

  deleteExperiment(experimentId: string): void {
    this.experiments.delete(experimentId);
    this.saveToStorage();
  }
}

// Singleton instance for persistence
let frameworkInstance: ABTestingFramework | null = null;

export function getABTestingFramework(): ABTestingFramework {
  if (!frameworkInstance) {
    frameworkInstance = new ABTestingFramework();
  }
  return frameworkInstance;
}

export default ABTestingFramework;

