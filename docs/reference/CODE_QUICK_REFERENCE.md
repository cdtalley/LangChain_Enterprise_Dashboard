# 🔖 Code Quick Reference

**Personal cheat sheet for understanding code structure**

---

## 📁 File Structure

```
lib/
├── persistence.ts          → localStorage abstraction
├── ab-testing.ts          → A/B testing framework
├── experiment-tracking.ts → MLflow-like tracking
├── demo-data-generator.ts → Data generation
├── DataContext.tsx        → Global state provider
└── TourContext.tsx        → Interactive tour

components/
├── pages/
│   ├── ABTestingPage.tsx  → A/B testing UI
│   ├── ExperimentsPage.tsx → Experiment tracking UI
│   └── ... (16 more)
└── shared/
    ├── DataTable.tsx      → Reusable table
    └── MetricCard.tsx     → Reusable metric display

app/
├── layout.tsx            → Root layout (wraps with providers)
└── page.tsx              → Main router
```

---

## 🔑 Key Patterns

### Singleton Pattern
```typescript
let instance: Class | null = null;
export function getInstance() {
  if (!instance) instance = new Class();
  return instance;
}
```
**Used in**: `ab-testing.ts`, `experiment-tracking.ts`

### React Context Pattern
```typescript
const Context = createContext<T | undefined>(undefined);
export function Provider({ children }) {
  const [state, setState] = useState();
  return <Context.Provider value={{ state }}>{children}</Context.Provider>;
}
export function useHook() {
  const ctx = useContext(Context);
  if (!ctx) throw new Error("Must be in Provider");
  return ctx;
}
```
**Used in**: `DataContext.tsx`, `TourContext.tsx`

### Persistence Pattern
```typescript
class Manager {
  constructor() {
    this.loadFromStorage(); // Load on creation
  }
  private saveToStorage() {
    PersistenceManager.save(KEY, data);
  }
  private loadFromStorage() {
    const data = PersistenceManager.load(KEY, []);
    // Restore state
  }
}
```
**Used in**: `ab-testing.ts`, `experiment-tracking.ts`

---

## 📊 Data Structures

### Experiment (A/B Testing)
```typescript
{
  id: "exp-1",
  config: {
    name: "Test",
    metricType: MetricType.CONTINUOUS,
    trafficSplit: 0.5,
    significanceLevel: 0.05
  },
  status: ExperimentStatus.RUNNING,
  events: [
    { userId: "user-1", variant: "baseline", metricValue: 0.95 }
  ],
  result: {
    pValue: 0.03,
    isSignificant: true,
    recommendation: "Deploy treatment"
  }
}
```

### Run (Experiment Tracking)
```typescript
{
  id: "run-1",
  experimentName: "sentiment-classifier",
  status: "running",
  parameters: { learningRate: 0.001 },
  metrics: { accuracy: 0.95 },
  metricsHistory: [
    { step: 1, metrics: { accuracy: 0.90 } },
    { step: 2, metrics: { accuracy: 0.95 } }
  ]
}
```

---

## 🔢 Key Functions

### A/B Testing
- `createExperiment(config)` → Creates experiment, returns ID
- `startExperiment(id)` → Changes status to RUNNING
- `recordEvent(id, userId, value)` → Records user event
- `analyzeExperiment(id)` → Runs statistical test, returns result
- `calculateSampleSize()` → Power analysis

### Experiment Tracking
- `startRun(name, expName, params)` → Creates run, returns ID
- `logParameter(id, key, value)` → Logs hyperparameter
- `logMetric(id, key, value, step?)` → Logs metric (with optional step)
- `endRun(id, status)` → Ends run

### Data Generation
- `generateFinanceData(n)` → Returns FinanceRecord[]
- `generateEcommerceData(n)` → Returns EcommerceRecord[]
- `generateMarketingData(n)` → Returns MarketingRecord[]
- `generateHRData(n)` → Returns HRRecord[]
- `generateHealthcareData(n)` → Returns HealthcareRecord[]

### Persistence
- `PersistenceManager.save(key, data)` → Saves to localStorage
- `PersistenceManager.load<T>(key, default)` → Loads from localStorage
- `PersistenceManager.remove(key)` → Removes from localStorage

---

## 🧮 Statistical Tests

### t-Test (Continuous Metrics)
```typescript
// When: Comparing means of two groups
// Example: Revenue, latency, accuracy
tTest(baselineValues, treatmentValues) → pValue
```

### Chi-Square Test (Binary Metrics)
```typescript
// When: Comparing proportions
// Example: Conversion rate, click rate
chiSquareTest(baselineValues, treatmentValues) → pValue
```

### Mann-Whitney U (Non-Parametric)
```typescript
// When: Data not normally distributed
// Example: Counts, rankings
mannWhitneyTest(group1, group2) → pValue
```

### Sample Size Calculation
```typescript
// Formula: n = (z_alpha + z_beta)^2 * 2 * std^2 / effect_size^2
calculateSampleSize(baselineMean, expectedLift) → n
```

---

## 🎯 Common Code Patterns

### Component with Framework
```typescript
export default function MyPage() {
  const [framework] = useState(() => getFramework());
  const [items, setItems] = useState(framework.getAll());
  
  useEffect(() => {
    const refresh = () => setItems(framework.getAll());
    refresh();
    const interval = setInterval(refresh, 1000);
    return () => clearInterval(interval);
  }, [framework]);
  
  return <div>{/* UI */}</div>;
}
```

### Using Data Context
```typescript
import { useData } from "@/lib/DataContext";

function MyComponent() {
  const { financeData, ecommerceData } = useData();
  return <div>{financeData.length} records</div>;
}
```

### Creating and Saving
```typescript
// Pattern: Create → Update state → Save happens automatically
const id = framework.create(config);
setItems(framework.getAll()); // Refresh local state
// Framework saves to localStorage automatically
```

---

## 🔍 Debugging Tips

### Check localStorage
```javascript
// In browser console:
localStorage.getItem("ab_testing_experiments")
JSON.parse(localStorage.getItem("ab_testing_experiments"))
```

### Check Framework State
```typescript
const framework = getABTestingFramework();
console.log(framework.getAllExperiments());
```

### Check Context State
```typescript
const { financeData } = useData();
console.log(financeData.length, financeData[0]);
```

---

## 📝 Type Definitions Quick Look

### Enums
```typescript
ExperimentStatus: DRAFT | RUNNING | PAUSED | COMPLETED | STOPPED
MetricType: CONTINUOUS | BINARY | COUNT
```

### Key Interfaces
```typescript
ExperimentConfig    → Experiment settings
ExperimentEvent     → Single user event
ExperimentResult    → Analysis results
ExperimentRun        → ML experiment run
FinanceRecord       → Finance data row
EcommerceRecord     → E-commerce data row
```

---

## 🚀 Common Workflows

### Create A/B Test
1. User fills form → `handleCreateExperiment()`
2. `framework.createExperiment(config)` → returns ID
3. `setExperiments(framework.getAllExperiments())` → refresh UI
4. User clicks "Start" → `framework.startExperiment(id)`
5. Events recorded → `framework.recordEvent(id, userId, value)`
6. User clicks "Analyze" → `framework.analyzeExperiment(id)`
7. Results shown → `experiment.result` displayed

### Track ML Experiment
1. User clicks "Start Run" → `tracker.startRun(name, expName, params)`
2. During training → `tracker.logMetric(runId, "accuracy", 0.95, step: 1)`
3. User clicks "End Run" → `tracker.endRun(runId, "completed")`
4. Results shown → `run.metrics` and `run.metricsHistory` displayed

### Generate Data
1. App starts → `DataProvider` mounts
2. `useEffect` runs → `generator.generateFinanceData(3000)`
3. Data generated → `setFinanceData(records)`
4. Context updates → All components using `useData()` get new data

---

## 💡 Key Insights

1. **Everything saves automatically** - Framework methods call `saveToStorage()` internally
2. **State updates are reactive** - React re-renders when state changes
3. **Cross-tab sync** - `storage` event listener updates UI when localStorage changes
4. **Singleton ensures persistence** - Same instance across re-renders
5. **Type safety everywhere** - TypeScript catches errors at compile time

---

**Use this while reading code to quickly understand what's happening!**
