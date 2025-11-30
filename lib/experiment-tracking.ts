/**
 * Experiment Tracking - MLflow-like tracking system
 */

import { PersistenceManager, STORAGE_KEYS } from "./persistence";

export interface ExperimentRun {
  id: string;
  name: string;
  experimentName: string;
  status: "running" | "completed" | "failed";
  startTime: string; // ISO string
  endTime?: string; // ISO string
  parameters: Record<string, any>;
  metrics: Record<string, number>;
  metricsHistory: Array<{ step: number; metrics: Record<string, number> }>;
  tags: Record<string, string>;
  artifacts: string[];
}

class ExperimentTracker {
  private runs: Map<string, ExperimentRun> = new Map();
  private nextId = 1;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    try {
      const saved = PersistenceManager.load<ExperimentRun[]>(STORAGE_KEYS.EXPERIMENT_TRACKING, []);
      saved.forEach(run => {
        this.runs.set(run.id, run);
        // Update nextId
        const idNum = parseInt(run.id.replace("run-", ""));
        if (idNum >= this.nextId) {
          this.nextId = idNum + 1;
        }
      });
    } catch (error) {
      console.error("Failed to load runs from storage:", error);
    }
  }

  private saveToStorage(): void {
    const runs = Array.from(this.runs.values());
    PersistenceManager.save(STORAGE_KEYS.EXPERIMENT_TRACKING, runs);
  }

  startRun(name: string, experimentName: string, parameters: Record<string, any> = {}): string {
    const id = `run-${this.nextId++}`;
    const run: ExperimentRun = {
      id,
      name,
      experimentName,
      status: "running",
      startTime: new Date().toISOString(),
      parameters,
      metrics: {},
      metricsHistory: [],
      tags: {},
      artifacts: [],
    };
    this.runs.set(id, run);
    this.saveToStorage();
    return id;
  }

  logParameter(runId: string, key: string, value: any): void {
    const run = this.runs.get(runId);
    if (run) {
      run.parameters[key] = value;
      this.saveToStorage();
    }
  }

  logMetric(runId: string, key: string, value: number, step?: number): void {
    const run = this.runs.get(runId);
    if (run) {
      run.metrics[key] = value;
      if (step !== undefined) {
        const historyEntry = run.metricsHistory.find(h => h.step === step);
        if (historyEntry) {
          historyEntry.metrics[key] = value;
        } else {
          run.metricsHistory.push({ step, metrics: { [key]: value } });
        }
        run.metricsHistory.sort((a, b) => a.step - b.step);
      }
      this.saveToStorage();
    }
  }

  logTag(runId: string, key: string, value: string): void {
    const run = this.runs.get(runId);
    if (run) {
      run.tags[key] = value;
      this.saveToStorage();
    }
  }

  endRun(runId: string, status: "completed" | "failed" = "completed"): void {
    const run = this.runs.get(runId);
    if (run) {
      run.status = status;
      run.endTime = new Date().toISOString();
      this.saveToStorage();
    }
  }

  getRun(runId: string): ExperimentRun | undefined {
    return this.runs.get(runId);
  }

  getAllRuns(): ExperimentRun[] {
    return Array.from(this.runs.values());
  }

  getRunsByExperiment(experimentName: string): ExperimentRun[] {
    return Array.from(this.runs.values()).filter(r => r.experimentName === experimentName);
  }

  deleteRun(runId: string): void {
    this.runs.delete(runId);
    this.saveToStorage();
  }
}

// Singleton instance for persistence
let trackerInstance: ExperimentTracker | null = null;

export function getExperimentTracker(): ExperimentTracker {
  if (!trackerInstance) {
    trackerInstance = new ExperimentTracker();
  }
  return trackerInstance;
}

export default ExperimentTracker;
