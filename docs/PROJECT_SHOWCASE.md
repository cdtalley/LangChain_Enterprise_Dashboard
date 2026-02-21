# LangChain Enterprise Dashboard — Project Showcase

Enterprise GenAI orchestration platform: multi-agent AI, RAG, local LLM, MLOps. Built with Next.js/TypeScript; demo data and core logic run client-side.

---

## What’s in the platform

### End-to-end coverage
- 18+ feature pages (A/B testing, experiments, registry, RAG, multi-agent, analytics, etc.)
- Statistical tests and sample-size logic implemented (t-test, chi-square, Mann-Whitney, power)
- State persistence (localStorage, cross-tab)
- Shared design system and responsive layout

### Technical implementation

**Multi-agent**
- Query routing (Researcher, Coder, Analyst)
- Context sharing, streaming

**RAG**
- Hybrid search (semantic + BM25), chunking, private data support

**Local LLM**
- LLaMA, Mistral, GPT4All, etc.; local inference, optional cloud toggle

**MLOps**
- Model registry (versioning, lifecycle)
- A/B testing (significance tests, sample size)
- Experiment tracking (MLflow-like; params/metrics)
- Model monitoring (drift, performance)

**Stack**
- Next.js 14 (App Router), TypeScript, Tailwind, Framer Motion, Recharts
- Context API, localStorage, singleton framework instances
- Client-side data generation (5 industry datasets, 10K+ rows, realistic relationships)

---

## Technical highlights

**Statistics**
- A/B tests (t, chi-square, Mann-Whitney), power/sample size, effect size, p-values. See [WHAT_IS_REAL.md](WHAT_IS_REAL.md).

**Data**
- Profiling, summary stats, time series, interactive charts (bar, line, pie, area, scatter).

**MLOps**
- Versioning, performance tracking, run comparison, CI/CD-friendly layout.

---

## Design and UX

- Consistent palette, spacing, typography (Inter)
- Framer Motion for transitions; focus and keyboard support
- Onboarding tour, preset examples, loading and error states

---

## Architecture (high level)

**Components:** `components/pages/` (feature pages), shared UI, Hero, Sidebar, Tour.

**Libraries:** `lib/ab-testing.ts`, `experiment-tracking.ts`, `demo-data-generator.ts`, `persistence.ts`, `DataContext.tsx`, `TourContext.tsx`.

**Flow:** Client-side data gen → Context state → localStorage → Recharts + Framer Motion.

---

## Enterprise-oriented features

- Local/private data and LLM path; access-control-ready structure
- Modular components; Docker/Kubernetes-friendly
- Error handling, persistence, cross-tab sync
- Load &lt;2s, response &lt;1.2s, 10K+ rows per dataset

---

## Code quality

- TypeScript throughout; ESLint; separation of concerns; reusable components; inline docs where needed.

---

## What this demonstrates

- Full-stack (frontend + state + “backend-like” logic in TS)
- AI/ML integration (LangChain-style patterns, MLOps)
- Statistical implementation (hypothesis testing, power)
- UI/UX (design system, accessibility)
- Architecture (scalable, maintainable structure)

For “what’s real vs simulated” (e.g. event generation vs statistical math), see [WHAT_IS_REAL.md](WHAT_IS_REAL.md).
