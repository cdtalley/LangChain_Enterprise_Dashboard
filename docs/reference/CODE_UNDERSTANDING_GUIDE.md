# Code Understanding Guide

**How each module works (personal reference)**

This guide walks through each module line-by-line to ensure you understand how everything connects.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Libraries (`lib/`)](#core-libraries)
3. [React Components](#react-components)
4. [Data Flow](#data-flow)
5. [Key Algorithms Explained](#key-algorithms-explained)

---

## Architecture Overview

### The Big Picture

```
User clicks button
    ↓
React Component (UI)
    ↓
Business Logic (lib/*.ts)
    ↓
Persistence Layer (persistence.ts)
    ↓
localStorage (Browser)
    ↓
DataContext (Global State)
    ↓
All Components Update (Reactive)
```

**Key Principle**: Separation of Concerns
- **Components** = UI only, no business logic
- **lib/** = Pure business logic, no UI
- **Context** = State management, no logic
- **Persistence** = Storage abstraction

---

## 📦 Core Libraries (`lib/`)

### 1. `lib/persistence.ts` - Storage Abstraction Layer

**Purpose**: Provides a clean API for saving/loading data to localStorage

```typescript
// What it does:
// - Abstracts localStorage operations
// - Handles errors gracefully
// - Provides type-safe loading

class PersistenceManager {
  // Save any data to localStorage
  static save(key: string, data: any): void {
    // Converts data to JSON string
    // Saves to localStorage
    // Handles errors if quota exceeded
  }

  // Load data with type safety
  static load<T>(key: string, defaultValue: T): T {
    // Gets JSON string from localStorage
    // Parses back to object
    // Returns defaultValue if not found
  }
}
```

**Why this exists**: 
- Centralizes storage logic
- Makes it easy to swap storage backends later
- Provides consistent error handling
- Type-safe with TypeScript generics

**Usage Example**:
```typescript
// Save
PersistenceManager.save("my_key", { name: "test" });

// Load with type safety
const data = PersistenceManager.load<{ name: string }>("my_key", { name: "" });
```

---

### 2. `lib/ab-testing.ts` - A/B Testing Framework

**Purpose**: Implements statistical A/B testing with hypothesis testing

#### **Core Concepts**

**Experiment**: A comparison between two versions (baseline vs treatment)

**Traffic Splitting**: Randomly assign users to groups
- Uses consistent hashing (same user always gets same group)
- `hashUserId()` converts user ID to 0-1 number
- If hash < trafficSplit → treatment, else → baseline

**Statistical Tests**:
- **t-test**: For continuous metrics (revenue, latency)
- **chi-square**: For binary metrics (conversion, clicks)
- **Mann-Whitney U**: For non-parametric data

#### **Step-by-Step Flow**

```typescript
// 1. CREATE EXPERIMENT
const expId = framework.createExperiment(config);
// - Generates unique ID: "exp-1", "exp-2", etc.
// - Sets status to DRAFT
// - Saves to localStorage

// 2. START EXPERIMENT
framework.startExperiment(expId);
// - Changes status to RUNNING
// - Records start time

// 3. RECORD EVENTS (as users interact)
framework.recordEvent(expId, userId, metricValue);
// - Hashes userId to determine variant (baseline/treatment)
// - Creates event with timestamp
// - Appends to experiment.events array
// - Saves to localStorage

// 4. ANALYZE RESULTS
const result = framework.analyzeExperiment(expId);
// - Splits events by variant
// - Calculates means for each group
// - Runs appropriate statistical test
// - Calculates p-value
// - Determines if significant (p < 0.05)
// - Calculates effect size and confidence interval
// - Generates recommendation
```

#### **Key Functions Explained**

**`hashUserId(userId: string)`**:
```typescript
// Purpose: Consistent hashing - same user always gets same variant
// Algorithm: Simple hash function
let hash = 0;
for (let i = 0; i < userId.length; i++) {
  hash = ((hash << 5) - hash) + userId.charCodeAt(i);
  hash = hash & hash; // Convert to 32bit integer
}
return Math.abs(hash) / 2147483647; // Normalize to 0-1
```

**`tTest(group1, group2)`**:
```typescript
// Purpose: Test if two groups have different means
// Steps:
// 1. Calculate mean and variance for each group
// 2. Calculate pooled standard deviation
// 3. Calculate standard error
// 4. Calculate t-statistic = (mean1 - mean2) / standardError
// 5. Convert t-statistic to p-value using normal distribution
```

**`chiSquareTest(group1, group2)`**:
```typescript
// Purpose: Test if two groups have different proportions
// Steps:
// 1. Count successes (value === 1) in each group
// 2. Calculate proportions: p1 = success1/total1, p2 = success2/total2
// 3. Calculate pooled proportion
// 4. Calculate z-score = (p1 - p2) / sqrt(pooled * (1-pooled) * (1/n1 + 1/n2))
// 5. Convert z-score to p-value
```

**`calculateSampleSize()`**:
```typescript
// Purpose: Determine how many samples needed for statistical power
// Formula: n = (z_alpha + z_beta)^2 * 2 * std^2 / effect_size^2
// Where:
// - z_alpha = 1.96 (for 95% confidence)
// - z_beta = 0.84 (for 80% power)
// - effect_size = |treatment_mean - baseline_mean| / std
```

#### **Data Structures**

```typescript
interface Experiment {
  id: string;                    // "exp-1"
  config: ExperimentConfig;       // Experiment settings
  status: ExperimentStatus;      // DRAFT, RUNNING, COMPLETED
  createdAt: string;             // ISO timestamp
  events: ExperimentEvent[];     // All recorded events
  result?: ExperimentResult;     // Analysis results
}

interface ExperimentEvent {
  experimentId: string;
  userId: string;
  variant: "baseline" | "treatment";
  metricValue: number;
  timestamp: string;
}

interface ExperimentResult {
  baselineMean: number;
  treatmentMean: number;
  pValue: number;
  isSignificant: boolean;
  effectSize: number;
  relativeLift: number;          // Percentage improvement
  recommendation: string;
  confidenceInterval: [number, number];
}
```

#### **Singleton Pattern**

```typescript
// Why singleton?
// - Ensures only one instance exists
// - Persists data across component re-renders
// - Loads from localStorage once on creation

let frameworkInstance: ABTestingFramework | null = null;

export function getABTestingFramework(): ABTestingFramework {
  if (!frameworkInstance) {
    frameworkInstance = new ABTestingFramework(); // Loads from localStorage
  }
  return frameworkInstance;
}
```

---

### 3. `lib/experiment-tracking.ts` - MLflow-like Tracking

**Purpose**: Track ML experiments (like MLflow)

#### **Core Concepts**

**Run**: A single experiment execution
- Has parameters (hyperparameters)
- Has metrics (accuracy, loss, etc.)
- Has metrics history (how metrics change over time)

**Experiment Name**: Groups related runs together
- Example: "sentiment-classifier" might have runs with different learning rates

#### **Step-by-Step Flow**

```typescript
// 1. START RUN
const runId = tracker.startRun("run-1", "sentiment-classifier", {
  learningRate: 0.001,
  batchSize: 32
});
// - Creates run with status "running"
// - Records start time
// - Saves to localStorage

// 2. LOG PARAMETERS
tracker.logParameter(runId, "epochs", 10);
// - Adds to run.parameters object
// - Saves to localStorage

// 3. LOG METRICS (during training)
tracker.logMetric(runId, "accuracy", 0.95, step: 1);
tracker.logMetric(runId, "accuracy", 0.96, step: 2);
// - Updates run.metrics (latest value)
// - Adds to run.metricsHistory (time series)
// - Saves to localStorage

// 4. END RUN
tracker.endRun(runId, "completed");
// - Sets status to "completed"
// - Records end time
// - Saves to localStorage
```

#### **Data Structure**

```typescript
interface ExperimentRun {
  id: string;                    // "run-1"
  name: string;                   // User-friendly name
  experimentName: string;          // Groups related runs
  status: "running" | "completed" | "failed";
  startTime: string;             // ISO timestamp
  endTime?: string;               // ISO timestamp
  parameters: Record<string, any>; // { learningRate: 0.001, ... }
  metrics: Record<string, number>; // { accuracy: 0.95, f1: 0.92 }
  metricsHistory: Array<{         // Time series of metrics
    step: number;
    metrics: Record<string, number>;
  }>;
  tags: Record<string, string>;   // Metadata
  artifacts: string[];            // File paths (not used in this version)
}
```

**Key Difference from A/B Testing**:
- A/B Testing: Compares two groups simultaneously
- Experiment Tracking: Tracks single experiment over time

---

### 4. `lib/demo-data-generator.ts` - Realistic Data Generation

**Purpose**: Generate realistic fake datasets for demos

#### **Core Concepts**

**Seeded Random**: Same seed = same sequence of random numbers
- Makes data reproducible
- Useful for demos and testing

**Probability Distributions**:
- **Normal**: Bell curve (heights, weights)
- **Log-normal**: Skewed right (prices, incomes)
- **Poisson**: Counts (page views, events)
- **Uniform**: Equal probability (categories)

**Correlated Features**: Features that depend on each other
- Example: Income → Spending (high income = high spending)

#### **Key Functions**

**`randomNormal(mean, std)`**:
```typescript
// Box-Muller transform: Converts uniform random to normal distribution
const u1 = this.random(); // 0-1
const u2 = this.random(); // 0-1
const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
return z0 * std + mean; // Scale and shift
```

**`randomLognormal(mean, std)`**:
```typescript
// Log-normal: exp(normal)
// Used for prices, incomes (always positive, skewed right)
return Math.exp(this.randomNormal(Math.log(mean), std));
```

**`randomPoisson(lambda)`**:
```typescript
// Poisson: Counts events in fixed interval
// lambda = average number of events
// Used for: page views, clicks, orders per day
```

**`weightedChoice(probabilities)`**:
```typescript
// Choose item based on probabilities
// Example: [0.25, 0.20, 0.15, ...] means first item 25% chance
```

#### **Data Generation Example: Finance**

```typescript
generateFinanceData(nRecords: number): FinanceRecord[] {
  const records = [];
  
  for (let i = 1; i <= nRecords; i++) {
    // Generate correlated features
    const creditScore = this.randomNormal(700, 50); // Normal distribution
    const income = this.randomLognormal(50000, 0.3); // Log-normal (skewed)
    
    // Correlate: Higher credit score → Lower fraud risk
    const fraudRisk = creditScore < 600 ? 0.15 : 0.02;
    const isFraud = this.random() < fraudRisk ? 1 : 0;
    
    // Correlate: Higher income → Higher transaction amounts
    const baseAmount = income * 0.1;
    const amount = baseAmount + this.randomNormal(0, baseAmount * 0.2);
    
    records.push({
      transaction_id: `TXN-${i}`,
      credit_score: Math.round(creditScore),
      amount: Math.round(amount * 100) / 100,
      is_fraud: isFraud,
      // ... more fields
    });
  }
  
  return records;
}
```

**Why This Matters**:
- Realistic data makes demos impressive
- Correlated features show understanding of real-world data
- Proper distributions demonstrate statistical knowledge

---

### 5. `lib/DataContext.tsx` - Global State Management

**Purpose**: Provides datasets to all components via React Context

#### **How React Context Works**

```typescript
// 1. CREATE CONTEXT
const DataContext = createContext<DataContextType | undefined>(undefined);

// 2. PROVIDER COMPONENT (wraps app)
export function DataProvider({ children }) {
  const [financeData, setFinanceData] = useState([]);
  // ... more state
  
  // Generate data on mount
  useEffect(() => {
    const generator = new DemoDataGenerator();
    setFinanceData(generator.generateFinanceData(3000));
    // ... generate other datasets
  }, []);
  
  return (
    <DataContext.Provider value={{ financeData, ... }}>
      {children}
    </DataContext.Provider>
  );
}

// 3. CUSTOM HOOK (use in components)
export function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error("useData must be used within DataProvider");
  }
  return context;
}
```

#### **Usage in Components**

```typescript
// In any component:
import { useData } from "@/lib/DataContext";

function MyComponent() {
  const { financeData, ecommerceData } = useData();
  
  // Use the data
  return <div>{financeData.length} records</div>;
}
```

**Why Context?**:
- Avoids prop drilling (passing data through many components)
- Single source of truth
- All components get same data
- Easy to refresh globally

---

## ⚛️ React Components

### 1. `app/page.tsx` - Main Router

**Purpose**: Routes between different pages

```typescript
export default function Home() {
  const [activePath, setActivePath] = useState("/");
  
  // Map paths to components
  const pageComponents: Record<string, React.ComponentType> = {
    "/": WelcomePage,
    "/ab-testing": ABTestingPage,
    "/experiments": ExperimentsPage,
    // ... more
  };
  
  const ActiveComponent = pageComponents[activePath] || WelcomePage;
  
  return (
    <div>
      <Sidebar activePath={activePath} onNavigate={setActivePath} />
      <main>
        <ActiveComponent />
      </main>
    </div>
  );
}
```

**How it works**:
1. User clicks sidebar link → `setActivePath("/ab-testing")`
2. `activePath` changes → React re-renders
3. `ActiveComponent` changes → Different page shows
4. Framer Motion animates transition

---

### 2. `components/pages/ABTestingPage.tsx` - A/B Testing UI

**Purpose**: UI for creating and analyzing A/B tests

#### **State Management**

```typescript
export default function ABTestingPage() {
  // Get singleton framework instance
  const [framework] = useState(() => getABTestingFramework());
  
  // Local state for experiments list
  const [experiments, setExperiments] = useState(
    framework.getAllExperiments()
  );
  
  // Form state
  const [formData, setFormData] = useState({ name: "", ... });
  
  // Refresh experiments when storage changes
  useEffect(() => {
    const refreshExperiments = () => {
      setExperiments(framework.getAllExperiments());
    };
    
    // Listen for cross-tab changes
    window.addEventListener("storage", (e) => {
      if (e.key === STORAGE_KEYS.AB_TESTING) {
        refreshExperiments();
      }
    });
    
    // Poll for same-tab changes
    const interval = setInterval(refreshExperiments, 1000);
    
    return () => {
      window.removeEventListener("storage", ...);
      clearInterval(interval);
    };
  }, [framework]);
}
```

#### **Creating an Experiment**

```typescript
const handleCreateExperiment = () => {
  const config: ExperimentConfig = {
    name: formData.name,
    description: formData.description,
    // ... more fields
  };
  
  // Create experiment
  const expId = framework.createExperiment(config);
  
  // Update local state
  setExperiments(framework.getAllExperiments());
  
  // Close form
  setShowCreateForm(false);
};
```

#### **Starting and Analyzing**

```typescript
const handleStartExperiment = (expId: string) => {
  framework.startExperiment(expId);
  
  // Simulate events (in real app, these come from users)
  for (let i = 0; i < 1000; i++) {
    const userId = `user-${i}`;
    const metricValue = Math.random() * 0.1 + 0.9; // 0.9-1.0
    framework.recordEvent(expId, userId, metricValue);
  }
  
  setExperiments(framework.getAllExperiments());
};

const handleAnalyze = (expId: string) => {
  const result = framework.analyzeExperiment(expId);
  // Result contains: pValue, isSignificant, recommendation, etc.
  setExperiments(framework.getAllExperiments());
};
```

#### **Example Loading (Quick Start)**

```typescript
const loadExample = (example) => {
  // Create experiment from template
  const config: ExperimentConfig = {
    name: example.name,
    // ... fill in from example
  };
  
  const expId = framework.createExperiment(config);
  setExperiments(framework.getAllExperiments());
  
  // Auto-start
  setTimeout(() => {
    handleStartExperiment(expId);
    // Auto-analyze after data loads
    setTimeout(() => {
      handleAnalyze(expId);
    }, 2000);
  }, 500);
};
```

---

## 🔄 Data Flow Examples

### Example 1: Creating an A/B Test

```
1. User fills form in ABTestingPage.tsx
   ↓
2. User clicks "Create Experiment"
   ↓
3. handleCreateExperiment() called
   ↓
4. framework.createExperiment(config)
   - Creates Experiment object
   - Saves to localStorage via PersistenceManager.save()
   - Updates framework.experiments Map
   ↓
5. setExperiments(framework.getAllExperiments())
   - Updates React state
   ↓
6. Component re-renders
   - Shows new experiment in list
   ↓
7. Other tabs detect storage change
   - storage event fires
   - refreshExperiments() called
   - Updates their UI too
```

### Example 2: Data Generation

```
1. App starts
   ↓
2. DataProvider mounts
   ↓
3. useEffect runs
   - Creates DemoDataGenerator
   - Calls generator.generateFinanceData(3000)
   ↓
4. generateFinanceData() executes
   - Loops 3000 times
   - Each iteration:
     * Generates correlated features
     * Creates FinanceRecord object
     * Adds to array
   ↓
5. setFinanceData(records)
   - Updates React state
   ↓
6. DataContext.Provider value updates
   ↓
7. All components using useData() re-render
   - They get new financeData
   - Display charts, tables, etc.
```

### Example 3: Analyzing Experiment

```
1. User clicks "Analyze" button
   ↓
2. handleAnalyze(expId) called
   ↓
3. framework.analyzeExperiment(expId)
   ↓
4. Gets experiment from Map
   ↓
5. Splits events by variant
   - baselineEvents = events.filter(variant === "baseline")
   - treatmentEvents = events.filter(variant === "treatment")
   ↓
6. Calculates means
   - baselineMean = mean(baselineValues)
   - treatmentMean = mean(treatmentValues)
   ↓
7. Runs statistical test
   - If CONTINUOUS → tTest()
   - If BINARY → chiSquareTest()
   - Else → mannWhitneyTest()
   ↓
8. Calculates p-value
   ↓
9. Determines significance
   - isSignificant = pValue < 0.05
   ↓
10. Calculates effect size
    - effectSize = treatmentMean - baselineMean
    - relativeLift = (effectSize / baselineMean) * 100
    ↓
11. Generates recommendation
    - If significant & positive → "Deploy treatment"
    - If significant & negative → "Keep baseline"
    - Else → "Continue experiment"
    ↓
12. Creates ExperimentResult object
    ↓
13. Saves to experiment.result
    ↓
14. PersistenceManager.save() → localStorage
    ↓
15. Component state updates
    ↓
16. UI shows results with charts
```

---

## 🧮 Key Algorithms Explained

### 1. Consistent Hashing (Traffic Splitting)

**Problem**: Same user should always get same variant

**Solution**: Hash user ID to 0-1 number

```typescript
hashUserId("user-123")
  → Hash function converts string to number
  → Normalize to 0-1 range
  → If < 0.5 → treatment, else → baseline
```

**Why it works**:
- Deterministic: Same input = same output
- Uniform distribution: Users evenly distributed
- Fast: O(n) where n = string length

### 2. t-Test (Statistical Significance)

**Problem**: Are two groups actually different, or just random variation?

**Solution**: Calculate probability (p-value) that difference is due to chance

```typescript
// Steps:
1. Calculate means: mean1, mean2
2. Calculate variances: var1, var2
3. Calculate pooled standard deviation
4. Calculate standard error
5. Calculate t-statistic = (mean1 - mean2) / standardError
6. Convert t-statistic to p-value
```

**Interpretation**:
- p < 0.05 → Significant (only 5% chance it's random)
- p >= 0.05 → Not significant (could be random)

### 3. Normal Distribution Generation (Box-Muller)

**Problem**: Generate normally distributed random numbers

**Solution**: Box-Muller transform

```typescript
// Convert two uniform random numbers (0-1) to one normal random number
u1 = random() // 0-1
u2 = random() // 0-1

z0 = sqrt(-2 * ln(u1)) * cos(2 * π * u2)
// z0 is standard normal (mean=0, std=1)

// Scale and shift
result = z0 * std + mean
```

**Why it works**: Mathematical transformation proven to produce normal distribution

### 4. Sample Size Calculation (Power Analysis)

**Problem**: How many samples needed to detect a difference?

**Solution**: Power analysis formula

```typescript
n = (z_alpha + z_beta)^2 * 2 * std^2 / effect_size^2

Where:
- z_alpha = 1.96 (for 95% confidence, alpha = 0.05)
- z_beta = 0.84 (for 80% power)
- effect_size = |treatment_mean - baseline_mean| / std
```

**Interpretation**:
- Larger effect size → Fewer samples needed
- Smaller effect size → More samples needed
- Higher power → More samples needed

---

## 🎓 Understanding Checklist

### Core Concepts
- [ ] Understand how React Context provides global state
- [ ] Understand how localStorage persistence works
- [ ] Understand singleton pattern for framework instances
- [ ] Understand separation of concerns (UI vs logic vs state)

### A/B Testing
- [ ] Understand traffic splitting with consistent hashing
- [ ] Understand when to use t-test vs chi-square vs Mann-Whitney
- [ ] Understand p-value interpretation
- [ ] Understand sample size calculation

### Data Generation
- [ ] Understand seeded random for reproducibility
- [ ] Understand different probability distributions
- [ ] Understand how to create correlated features
- [ ] Understand Box-Muller transform for normal distribution

### React Patterns
- [ ] Understand useEffect for side effects
- [ ] Understand useState for local state
- [ ] Understand custom hooks (useData)
- [ ] Understand event listeners and cleanup

### TypeScript
- [ ] Understand interfaces for type safety
- [ ] Understand generics (`load<T>`)
- [ ] Understand enums for constants
- [ ] Understand optional properties (`endTime?`)

---

## 🔍 Code Reading Tips

1. **Start with the data structures** (interfaces)
   - Understand what data looks like before reading logic

2. **Follow the flow**
   - Start from user action → component → logic → storage

3. **Read comments**
   - They explain "why", not just "what"

4. **Trace examples**
   - Pick a specific example and trace it through the code

5. **Understand patterns**
   - Once you understand one module, others follow similar patterns

---

## Common Questions Answered

**Q: Why singleton pattern?**
A: Ensures only one instance exists, loads from localStorage once, persists across re-renders.

**Q: Why localStorage instead of database?**
A: Client-side demo doesn't need backend. Easy to swap to database later via PersistenceManager abstraction.

**Q: Why separate persistence layer?**
A: Makes it easy to swap storage backends, centralizes error handling, provides clean API.

**Q: Why React Context?**
A: Avoids prop drilling, single source of truth, easy to refresh globally.

**Q: Why seeded random?**
A: Makes data reproducible for demos - same seed = same data every time.

---

**Remember**: Understanding comes from reading code, tracing examples, and asking "why" at each step. Take your time, and don't hesitate to experiment with the code!
