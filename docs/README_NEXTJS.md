# Enterprise LangChain AI Workbench (Next.js)

Next.js app for enterprise AI/ML: dashboards, data generation, and visualizations.

## Features

- Next.js 14 with App Router and TypeScript
- Tailwind CSS and Framer Motion
- Recharts for visualizations
- Demo data generator for multiple industries
- Dashboards: Finance, E-commerce, Marketing, HR analytics
- Responsive layout

## Tech Stack

- Next.js 14 (App Router), TypeScript, Tailwind CSS, Framer Motion, Recharts, Lucide React

## Installation

```bash
npm install
npm run dev   # http://localhost:3000
npm run build
npm start
```

## Usage

1. `npm run dev`
2. Open `http://localhost:3000`
3. Use sidebar: Enterprise Demo, Analytics Dashboard, Data Generator

## Available Datasets

- Healthcare: patient records, vitals, conditions
- Finance: transactions, fraud detection
- E-commerce: sales, products, orders
- Marketing: campaigns, conversions, ROI
- HR: employee data, performance, retention

## Components

- HeroSection, StatsGrid, FeatureCards, DashboardTabs
- EnterpriseDemo, AnalyticsDashboard, DataGenerator

## Deployment

**Vercel:** `vercel`

**Docker:** `docker build -t langchain-dashboard .` then `docker run -p 3000:3000 langchain-dashboard`

## Notes

- Demo data is generated client-side in TypeScript
- No backend required for core features
- Can add API routes for server-side data
