/**
 * Persistence layer for app state using localStorage
 */

const STORAGE_KEYS = {
  AB_TESTING: "ab_testing_experiments",
  EXPERIMENT_TRACKING: "experiment_tracking_runs",
  MODEL_REGISTRY: "model_registry_models",
} as const;

export class PersistenceManager {
  static save(key: string, data: any): void {
    try {
      if (typeof window !== "undefined") {
        localStorage.setItem(key, JSON.stringify(data));
      }
    } catch (error) {
      console.error(`Failed to save to localStorage:`, error);
    }
  }

  static load<T>(key: string, defaultValue: T): T {
    try {
      if (typeof window !== "undefined") {
        const item = localStorage.getItem(key);
        if (item) {
          return JSON.parse(item) as T;
        }
      }
    } catch (error) {
      console.error(`Failed to load from localStorage:`, error);
    }
    return defaultValue;
  }

  static remove(key: string): void {
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem(key);
      }
    } catch (error) {
      console.error(`Failed to remove from localStorage:`, error);
    }
  }

  static clear(): void {
    try {
      if (typeof window !== "undefined") {
        Object.values(STORAGE_KEYS).forEach(key => {
          localStorage.removeItem(key);
        });
      }
    } catch (error) {
      console.error(`Failed to clear localStorage:`, error);
    }
  }
}

export { STORAGE_KEYS };

