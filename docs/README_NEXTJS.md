# 🚀 Enterprise LangChain AI Workbench - Next.js Edition

A stunning, modern Next.js application showcasing enterprise AI/ML capabilities with beautiful visualizations and interactive dashboards.

## ✨ Features

- **Modern Next.js 14** with App Router and TypeScript
- **Beautiful UI** with Tailwind CSS and Framer Motion animations
- **Interactive Visualizations** using Recharts
- **Demo Data Generator** - Generate realistic datasets for multiple industries
- **Enterprise Dashboards** - Finance, E-commerce, Marketing, HR analytics
- **Responsive Design** - Works perfectly on all devices

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: Lucide React

## 📦 Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🎯 Usage

1. **Start the app**: `npm run dev`
2. **Open browser**: Navigate to `http://localhost:3000`
3. **Explore dashboards**: 
   - Enterprise Demo: View pre-loaded datasets with visualizations
   - Analytics Dashboard: Interactive data analysis
   - Data Generator: Create custom datasets

## 📊 Available Datasets

- **Healthcare**: Patient records, vitals, conditions
- **Finance**: Transactions, fraud detection
- **E-commerce**: Sales, products, orders
- **Marketing**: Campaigns, conversions, ROI
- **HR**: Employee data, performance, retention

## 🎨 Key Components

- `HeroSection`: Stunning hero with gradient animations
- `StatsGrid`: Real-time metrics display
- `FeatureCards`: Feature showcase with hover effects
- `EnterpriseDemo`: Multi-dataset dashboard with charts
- `AnalyticsDashboard`: Data visualization and insights
- `DataGenerator`: Custom dataset creation tool

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Docker
```bash
docker build -t langchain-dashboard .
docker run -p 3000:3000 langchain-dashboard
```

## 📝 Notes

- All demo data is generated client-side using TypeScript
- No backend required for basic functionality
- Can be extended with API routes for server-side data generation
- Fully responsive and mobile-friendly

## 🔮 Future Enhancements

- [ ] API routes for server-side data generation
- [ ] Real-time data updates
- [ ] Export to Excel/Parquet formats
- [ ] Advanced filtering and search
- [ ] User authentication
- [ ] Data persistence

