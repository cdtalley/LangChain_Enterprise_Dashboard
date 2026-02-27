# LangChain Enterprise AI Workbench

Enterprise GenAI orchestration platform: multi-agent AI, RAG, local LLM support, MLOps tooling. Next.js/TypeScript frontend; demo data and core logic run client-side.

![Next.js](https://img.shields.io/badge/Next.js-14.2-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Live:** [GitHub Pages](https://cdtalley.github.io/LangChain_Enterprise_Dashboard/)

---

## Key Features

### Multi-Agent AI
- Agent routing (Researcher, Coder, Analyst) with task delegation
- Context sharing and coordinated execution
- Streaming responses

### RAG Pipeline
- Hybrid search (semantic + keyword/BM25)
- Chunking and metadata filtering
- Private data support

### Local LLM
- LLaMA, Mistral, GPT4All, etc.
- Local inference; optional cloud toggle
- On-prem option for sensitive data

### LLM Fine-Tuning
- LoRA, QLoRA, PEFT
- Pipeline from data to deployment

### MLOps
- Model registry (versioning, lifecycle)
- A/B testing (t-test, chi-square, Mann-Whitney; sample size)
- Experiment tracking (MLflow-like; params/metrics)
- Model monitoring (drift, performance)

### Analytics
- Dashboards (Recharts)
- Data profiling
- Statistical tests, time series

---

## Stack

- **Frontend**: Next.js 14 (App Router), TypeScript 5.3, React 18.3, Tailwind, Framer Motion, Recharts
- **Data**: Client-side generation, localStorage persistence, cross-tab sync
- **No backend required** for core demo features

---

## Quick Start

**Prerequisites:** Node.js 18+, npm or yarn

```bash
git clone <repository-url>
cd LangChain_Enterprise_Dashboard
npm install
npm run dev
```

App: `http://localhost:3000`

**Build:** `npm run build` then `npm start`

---

## Docs

- **Features**: Multi-agent (`/multi-agent`), RAG (`/rag`), A/B testing (`/ab-testing`), Experiments (`/experiments`), Registry (`/registry`)
- **What’s real vs simulated**: [docs/WHAT_IS_REAL.md](docs/WHAT_IS_REAL.md)
- **Full index**: [docs/README.md](docs/README.md)

---

## Use Cases

- Enterprise GenAI apps (secure, scalable)
- R&D and prototyping
- Data analysis and dashboards
- MLOps lifecycle
- Local/private LLM deployment

---

## Project Structure

```
├── app/                 # Next.js app
├── components/          # React + page components
├── lib/                 # ab-testing, experiment-tracking, demo-data-generator, persistence
└── public/
```

---

## License

MIT — see LICENSE.

---

## Author

**Drake Talley**
