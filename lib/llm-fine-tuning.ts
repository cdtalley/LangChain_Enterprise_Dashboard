export enum FineTuningMethod {
  LORA = "lora",
  QLORA = "qlora",
  PEFT = "peft",
}

export enum FineTuningStatus {
  IDLE = "idle",
  PREPARING = "preparing",
  TRAINING = "training",
  VALIDATING = "validating",
  COMPLETED = "completed",
  FAILED = "failed",
}

export interface FineTuningConfig {
  method: FineTuningMethod;
  epochs: number;
  learningRate: number;
  batchSize: number;
  baseModel: string;
  trainingDataSize: number;
  validationDataSize: number;
}

export interface TrainingMetrics {
  epoch: number;
  loss: number;
  accuracy?: number;
  learningRate: number;
  timestamp: string;
}

export interface FineTuningJob {
  id: string;
  config: FineTuningConfig;
  status: FineTuningStatus;
  startTime?: string;
  endTime?: string;
  currentEpoch: number;
  metrics: TrainingMetrics[];
  finalLoss?: number;
  finalAccuracy?: number;
  error?: string;
}

class LLMFineTuningFramework {
  private jobs: Map<string, FineTuningJob> = new Map();
  private nextId = 1;
  private activeJobId: string | null = null;

  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage(): void {
    try {
      const stored = localStorage.getItem("llm_fine_tuning_jobs");
      if (stored) {
        const data = JSON.parse(stored);
        this.jobs = new Map(Object.entries(data.jobs || {}));
        this.nextId = data.nextId || 1;
        this.activeJobId = data.activeJobId || null;
      }
    } catch (e) {
      console.error("Failed to load fine-tuning jobs:", e);
    }
  }

  private saveToStorage(): void {
    try {
      const data = {
        jobs: Object.fromEntries(this.jobs),
        nextId: this.nextId,
        activeJobId: this.activeJobId,
      };
      localStorage.setItem("llm_fine_tuning_jobs", JSON.stringify(data));
    } catch (e) {
      console.error("Failed to save fine-tuning jobs:", e);
    }
  }

  createJob(config: FineTuningConfig): string {
    const id = `job-${this.nextId++}`;
    const job: FineTuningJob = {
      id,
      config,
      status: FineTuningStatus.IDLE,
      currentEpoch: 0,
      metrics: [],
    };
    this.jobs.set(id, job);
    this.saveToStorage();
    return id;
  }

  getAllJobs(): FineTuningJob[] {
    return Array.from(this.jobs.values()).sort(
      (a, b) => new Date(b.startTime || 0).getTime() - new Date(a.startTime || 0).getTime()
    );
  }

  getJob(id: string): FineTuningJob | undefined {
    return this.jobs.get(id);
  }

  async startTraining(jobId: string, onProgress?: (job: FineTuningJob) => void): Promise<void> {
    const job = this.jobs.get(jobId);
    if (!job) throw new Error("Job not found");
    if (this.activeJobId && this.activeJobId !== jobId) {
      throw new Error("Another training job is already running");
    }

    this.activeJobId = jobId;
    job.status = FineTuningStatus.PREPARING;
    job.startTime = new Date().toISOString();
    this.saveToStorage();
    if (onProgress) onProgress({ ...job });

    // Simulate preparation phase
    await this.delay(1000);
    job.status = FineTuningStatus.TRAINING;
    this.saveToStorage();
    if (onProgress) onProgress({ ...job });

    // Simulate training epochs
    for (let epoch = 1; epoch <= job.config.epochs; epoch++) {
      job.currentEpoch = epoch;
      
      // Simulate batch processing
      const batchesPerEpoch = Math.ceil(job.config.trainingDataSize / job.config.batchSize);
      for (let batch = 0; batch < batchesPerEpoch; batch++) {
        // Simulate training progress
        const progress = (batch + 1) / batchesPerEpoch;
        const baseLoss = 2.5 - (epoch - 1) * 0.15;
        const loss = baseLoss - progress * 0.1 + (Math.random() - 0.5) * 0.1;
        
        // Update metrics periodically
        if (batch % Math.max(1, Math.floor(batchesPerEpoch / 5)) === 0 || batch === batchesPerEpoch - 1) {
          const metric: TrainingMetrics = {
            epoch,
            loss: Math.max(0.1, loss),
            accuracy: job.config.method === FineTuningMethod.QLORA ? undefined : 0.5 + (epoch - 1) * 0.05 + Math.random() * 0.02,
            learningRate: job.config.learningRate,
            timestamp: new Date().toISOString(),
          };
          job.metrics.push(metric);
          this.saveToStorage();
          if (onProgress) onProgress({ ...job });
        }
        
        await this.delay(200); // Simulate batch processing time
      }
    }

    // Validation phase
    job.status = FineTuningStatus.VALIDATING;
    this.saveToStorage();
    if (onProgress) onProgress({ ...job });
    await this.delay(1500);

    // Finalize
    const finalMetric = job.metrics[job.metrics.length - 1];
    job.status = FineTuningStatus.COMPLETED;
    job.endTime = new Date().toISOString();
    job.finalLoss = finalMetric?.loss || 0.5;
    job.finalAccuracy = finalMetric?.accuracy || 0.85;
    this.activeJobId = null;
    this.saveToStorage();
    if (onProgress) onProgress({ ...job });
  }

  stopTraining(jobId: string): void {
    const job = this.jobs.get(jobId);
    if (job && job.status === FineTuningStatus.TRAINING) {
      job.status = FineTuningStatus.FAILED;
      job.endTime = new Date().toISOString();
      job.error = "Training stopped by user";
      this.activeJobId = null;
      this.saveToStorage();
    }
  }

  deleteJob(jobId: string): void {
    this.jobs.delete(jobId);
    if (this.activeJobId === jobId) {
      this.activeJobId = null;
    }
    this.saveToStorage();
  }

  getActiveJob(): FineTuningJob | null {
    return this.activeJobId ? this.jobs.get(this.activeJobId) || null : null;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Singleton instance
let frameworkInstance: LLMFineTuningFramework | null = null;

export function getFineTuningFramework(): LLMFineTuningFramework {
  if (!frameworkInstance) {
    frameworkInstance = new LLMFineTuningFramework();
  }
  return frameworkInstance;
}

export default LLMFineTuningFramework;
