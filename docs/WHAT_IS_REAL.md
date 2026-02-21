# What's Real vs Simulated

*Drake Talley*

## Fully Implemented

### 1. A/B testing – statistical tests  
**Location**: `lib/ab-testing.ts`

- **t-Test** (250–267): pooled std dev, t-statistic, p-value via normal CDF  
- **Chi-square** (269–284): proportions for binary metrics, z-score → p-value  
- **Mann-Whitney U** (286–311): ranks, U statistic, p-value  
- **Sample size calculator** (222–238): power, effect size  
- **Normal CDF** (313–329): error-function approximation used in p-values  

All of the above use real formulas; p-values come from the data. Create an experiment, run analysis, inspect p-values in the console.

---

### 2. Data generation  
**Location**: `lib/demo-data-generator.ts`

- **Box-Muller** (122–127): uniform → normal via `sqrt(-2*ln(u1))*cos(2π*u2)`  
- **Log-normal** (129–131): `exp(normal(log(mean), std))`  
- **Poisson** (133–142): count data, exponential decay  
- **Correlated features**: e.g. income→spending, credit→fraud risk  

Same seed ⇒ same output.

---

### 3. Persistence (localStorage)  
**Location**: `lib/persistence.ts`

- get/set with `localStorage`; JSON serialize/parse. Data survives reloads and new sessions.  
- DevTools → Application → Local Storage to inspect.

---

### 4. Experiment tracking  
**Location**: `lib/experiment-tracking.ts`

Runs: create, update, delete. Parameters and metrics (with history) and start/end times are stored and persisted.

---

### 5. State management  
**Location**: `lib/DataContext.tsx`

React Context, real state updates, data generation on mount. `useData()` gives components access.

---

## Partially Simulated (UI / demo only)

### A/B testing – event source  
**Location**: `components/pages/ABTestingPage.tsx` (~200–250)

"Start Experiment" fabricates user events. Those events live in real structures; the stats (t-test, chi-square, etc.) run on them and are real. In production you’d plug in real events.

---

### AutoML – training progress  
**Location**: `components/pages/AutoMLPage.tsx`

Progress bar and “training steps” are simulated. Model metrics (accuracy, F1, best-model choice) and state are real. No actual model training in the browser without a backend.

---

### Multi-agent  
**Location**: `components/pages/MultiAgentPage.tsx`

Agent text and “reasoning” are simulated. Real LLM would require API + backend.

---

### RAG  
**Location**: `components/pages/RAGPage.tsx`

Search/semantic results are simulated. Real RAG would need embeddings + vector store.

---

## What would need a backend

- Real ML training (GPU/server)  
- Live LLM calls (API keys, backend)  
- Vector DB + embeddings for RAG  
- Production event pipelines  
- Shared DB instead of localStorage for multi-user  

---

## How to verify

**A/B math** – console:

```javascript
const framework = getABTestingFramework();
const expId = framework.createExperiment({
  name: "Test",
  metricType: MetricType.CONTINUOUS,
  // ... config
});
for (let i = 0; i < 100; i++) {
  framework.recordEvent(expId, `user-${i}`, 0.9 + Math.random() * 0.1);
}
const result = framework.analyzeExperiment(expId);
console.log(result.pValue, result.isSignificant);
```

**Data gen** – same seed ⇒ same data:

```javascript
const gen1 = new DemoDataGenerator(42);
const gen2 = new DemoDataGenerator(42);
const data1 = gen1.generateFinanceData(10);
const data2 = gen2.generateFinanceData(10);
console.log(data1[0].amount === data2[0].amount); // true
```

**Persistence** – create an experiment, check `localStorage.getItem("ab_testing_experiments")`, reload.
