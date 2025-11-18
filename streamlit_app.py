import os
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from typing import Dict, Any
import tempfile
from agents import MultiAgentSystem
from advanced_rag import AdvancedRAGSystem
from model_registry import ModelRegistryManager, ModelType, ModelStage
from ab_testing import ABTestingFramework, ExperimentConfig, MetricType, ExperimentStatus
from experiment_tracking import ExperimentTracking
from model_monitoring import ModelMonitoring

st.set_page_config(
    page_title="Enterprise LangChain AI Workbench", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 1rem;
}
.section-header {
    font-size: 1.5rem;
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #3498db;
}
.agent-result {
    background-color: #e8f4fd;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #2196F3;
}
.tool-result {
    background-color: #f0f8e8;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.markdown("""
# 🚀 Enterprise LangChain AI Workbench

**Advanced LLM Orchestration Platform (Local LLM Mode)**

### Features:
- 🤖 **Multi-Agent Collaboration**
- 📊 **Advanced RAG with Hybrid Search**
- 🔧 **Custom Tool Integration**
- 📈 **Real-time Analytics**
- 🧠 **Intelligent Query Routing**

### Links:
- [LangChain](https://python.langchain.com/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- [Streamlit](https://streamlit.io/)
""")

st.sidebar.markdown("---")

# Remove OpenAI API key input
# openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
serpapi_key = st.sidebar.text_input("🔍 SerpAPI Key (Optional)", type="password")

# Initialize systems (no OpenAI key required)
if 'multi_agent' not in st.session_state:
    st.session_state['multi_agent'] = MultiAgentSystem()
if 'advanced_rag' not in st.session_state:
    st.session_state['advanced_rag'] = AdvancedRAGSystem()

# Clear state button
if st.sidebar.button("🗑️ Clear All State"):
    for key in list(st.session_state.keys()):
        if key not in ['multi_agent', 'advanced_rag']:
            del st.session_state[key]
    st.rerun()

# --- Main App ---
st.markdown('<h1 class="main-header">🤖 Enterprise LangChain AI Workbench</h1>', unsafe_allow_html=True)
st.caption("**Advanced LLM Orchestration & Multi-Agent Collaboration Platform**")

# --- Tab Navigation ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🤖 Multi-Agent System", 
    "📊 Advanced RAG", 
    "🔧 Tool Execution", 
    "📈 Analytics Dashboard",
    "🎯 Enterprise Demo",
    "📦 Model Registry",
    "🧪 A/B Testing",
    "📝 Experiment Tracking",
    "🔍 Model Monitoring"
])

# --- Multi-Agent System Tab ---
with tab1:
    st.markdown('<h2 class="section-header">Multi-Agent Collaboration System</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Agent Task Assignment")
        
        # Agent selection
        available_agents = st.session_state['multi_agent'].get_agent_list()
        selected_agent = st.selectbox(
            "Choose an agent:",
            ["Auto-Route"] + available_agents,
            help="Auto-Route will intelligently select the best agent for your task"
        )
        
        # Task input
        task = st.text_area(
            "Describe your task:",
            placeholder="e.g., Research the latest trends in AI, analyze this dataset, write Python code to solve a problem",
            height=100
        )
        
        col_execute, col_collaborate = st.columns(2)
        
        with col_execute:
            if st.button("🚀 Execute Task", type="primary") and task:
                with st.spinner("Agent working..."):
                    if selected_agent == "Auto-Route":
                        # Use enhanced intelligent routing
                        agent_to_use = st.session_state['multi_agent'].intelligent_agent_routing(task)
                        st.info(f"🎯 Auto-routed to: **{agent_to_use.title()} Agent**")
                        
                        # Show routing confidence and alternatives
                        with st.expander("🔍 Routing Details"):
                            capabilities = st.session_state['multi_agent'].get_agent_capabilities()
                            st.write(f"**Selected Agent:** {agent_to_use.title()}")
                            st.write(f"**Description:** {capabilities[agent_to_use]['description']}")
                            st.write(f"**Strengths:** {', '.join(capabilities[agent_to_use]['strengths'])}")
                    else:
                        agent_to_use = selected_agent
                    
                    result = st.session_state['multi_agent'].run_agent(agent_to_use, task)
                    
                    st.markdown(f'<div class="agent-result"><strong>{agent_to_use.title()} Agent Result:</strong><br>{result}</div>', 
                               unsafe_allow_html=True)
        
        with col_collaborate:
            if st.button("🤝 Collaborative Task", type="secondary") and task:
                with st.spinner("Multi-agent collaboration in progress..."):
                    results = st.session_state['multi_agent'].collaborative_task(task)
                    
                    for agent_name, result in results.items():
                        st.markdown(f'<div class="agent-result"><strong>{agent_name.title()} Agent:</strong><br>{result[:500]}...</div>', 
                                   unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Agent Status")
        
        agents_info = [
            {"Agent": "Researcher", "Status": "🟢 Ready", "Tools": "Web Search, Scraping"},
            {"Agent": "Coder", "Status": "🟢 Ready", "Tools": "Python Executor, Data Analysis"},
            {"Agent": "Analyst", "Status": "🟢 Ready", "Tools": "All Tools, Synthesis"}
        ]
        
        df = pd.DataFrame(agents_info)
        st.dataframe(df, use_container_width=True)
        
        # Agent performance metrics (simulated)
        st.subheader("📈 Performance Metrics")
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.metric("Tasks Completed", "47", "5")
        with metrics_col2:
            st.metric("Avg Response Time", "2.3s", "-0.4s")

# --- Advanced RAG Tab ---
with tab2:
    st.markdown('<h2 class="section-header">Advanced Retrieval-Augmented Generation</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📁 Document Upload & Processing")
        
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, TXT, DOCX):",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                
                file_type = uploaded_file.name.split('.')[-1]
                result = st.session_state['advanced_rag'].load_document(
                    tmp_path, 
                    file_type,
                    metadata={"filename": uploaded_file.name, "size": uploaded_file.size}
                )
                st.success(f"✅ {result}")
        
        # Document query interface
        st.subheader("🔍 Intelligent Document Query")
        
        query_col1, query_col2 = st.columns([3, 1])
        
        with query_col1:
            query = st.text_input(
                "Ask a question about your documents:",
                placeholder="e.g., What are the key findings? Summarize the main concepts."
            )
        
        with query_col2:
            retrieval_strategy = st.selectbox(
                "Retrieval Strategy:",
                ["ensemble", "dense", "bm25", "auto"]
            )
        
        if st.button("🚀 Query Documents") and query:
            with st.spinner("Processing query with advanced RAG..."):
                results = st.session_state['advanced_rag'].query_documents(
                    query, 
                    retrieval_strategy=retrieval_strategy,
                    top_k=5
                )
                
                if "error" not in results:
                    st.markdown(f"**Answer:** {results['answer']}")
                    
                    with st.expander("🔍 Source Documents & Metadata"):
                        for i, doc in enumerate(results['source_documents']):
                            st.markdown(f"**Source {i+1}:**")
                            st.markdown(f"```\n{doc['content']}\n```")
                            st.json(doc['metadata'])
                    
                    # Query analytics
                    st.subheader("📊 Query Analytics")
                    metrics_data = results['metadata']
                    
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Sources Used", metrics_data['num_sources'])
                    with metric_col2:
                        st.metric("Query Type", metrics_data['query_type'])
                    with metric_col3:
                        st.metric("Strategy", results['strategy'])
                else:
                    st.error(results['error'])
    
    with col2:
        st.subheader("📋 Document Summary")
        
        if hasattr(st.session_state['advanced_rag'], 'document_metadata'):
            summary = st.session_state['advanced_rag'].get_document_summary()
            
            st.metric("Total Documents", summary['total_documents'])
            st.metric("Total Chunks", summary['total_chunks'])
            
            if summary['documents']:
                doc_df = pd.DataFrame(summary['documents'])
                st.dataframe(doc_df, use_container_width=True)
        
        # Chunking analytics
        if st.button("📊 Analyze Chunking"):
            analytics = st.session_state['advanced_rag'].get_chunk_analytics()
            
            if analytics['chunk_strategies']:
                # Create pie chart of chunking strategies
                strategies = list(analytics['chunk_strategies'].keys())
                counts = [analytics['chunk_strategies'][s]['count'] for s in strategies]
                
                fig = px.pie(
                    values=counts, 
                    names=strategies,
                    title="Chunking Strategy Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

# --- Tool Execution Tab ---
with tab3:
    st.markdown('<h2 class="section-header">Advanced Tool Execution Environment</h2>', unsafe_allow_html=True)
    
    # Tool selector
    tool_type = st.selectbox(
        "Select Tool Type:",
        ["Python Code Executor", "Web Scraper", "Data Analyzer", "Web Search"]
    )
    
    if tool_type == "Python Code Executor":
        st.subheader("🐍 Python Code Execution")
        
        code = st.text_area(
            "Enter Python code:",
            value="""import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data analysis
data = np.random.randn(100)
df = pd.DataFrame({'values': data})

print("Data Statistics:")
print(df.describe())

# Create a simple plot
plt.figure(figsize=(10, 6))
plt.hist(data, bins=20, alpha=0.7)
plt.title("Random Data Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

print("Analysis complete!")""",
            height=200
        )
        
        if st.button("▶️ Execute Code"):
            with st.spinner("Executing code..."):
                from agents import CodeExecutorTool
                executor = CodeExecutorTool()
                result = executor._run(code)
                st.markdown(f'<div class="tool-result">{result}</div>', unsafe_allow_html=True)
    
    elif tool_type == "Web Scraper":
        st.subheader("🌐 Web Content Scraper")
        
        url = st.text_input("Enter URL to scrape:", placeholder="https://example.com")
        
        if st.button("🔍 Scrape Content") and url:
            with st.spinner("Scraping content..."):
                from agents import WebScrapeTool
                scraper = WebScrapeTool()
                result = scraper._run(url)
                st.markdown(f'<div class="tool-result">{result}</div>', unsafe_allow_html=True)
    
    elif tool_type == "Data Analyzer":
        st.subheader("📊 Advanced Data Analysis")
        
        data_desc = st.text_area(
            "Describe your dataset or paste CSV data:",
            placeholder="Sales data from Q1 2024 with columns: date, product, revenue, region"
        )
        
        if st.button("📈 Analyze Data") and data_desc:
            with st.spinner("Analyzing data..."):
                from agents import DataAnalysisTool
                analyzer = DataAnalysisTool()
                result = analyzer._run(data_desc)
                st.markdown(f'<div class="tool-result">{result}</div>', unsafe_allow_html=True)

# --- Analytics Dashboard Tab ---
with tab4:
    st.markdown('<h2 class="section-header">Enterprise Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Simulated analytics data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queries", "1,247", "12%")
    with col2:
        st.metric("Avg Response Time", "1.8s", "-15%")
    with col3:
        st.metric("Documents Processed", "342", "8%")
    with col4:
        st.metric("Agent Efficiency", "94.2%", "2.1%")
    
    # Usage trends
    st.subheader("📈 Usage Trends")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    usage_data = pd.DataFrame({
        'Date': dates,
        'Queries': np.random.poisson(50, len(dates)),
        'Agent_Calls': np.random.poisson(30, len(dates)),
        'Documents_Processed': np.random.poisson(15, len(dates))
    })
    
    fig = px.line(
        usage_data, 
        x='Date', 
        y=['Queries', 'Agent_Calls', 'Documents_Processed'],
        title="Daily Platform Usage"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Agent performance comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Agent Performance Analysis")
        
        # Get real agent capabilities
        capabilities = st.session_state['multi_agent'].get_agent_capabilities()
        
        # Create performance data with real capabilities
        agent_data = []
        for agent_name, caps in capabilities.items():
            agent_data.append({
                'Agent': agent_name.title(),
                'Tools_Count': len(caps['tools']),
                'Strengths_Count': len(caps['strengths']),
                'Best_For_Count': len(caps['best_for'])
            })
        
        agent_df = pd.DataFrame(agent_data)
        
        # Create multi-metric chart
        fig = px.bar(agent_df, 
                    x='Agent', 
                    y=['Tools_Count', 'Strengths_Count', 'Best_For_Count'],
                    title="Agent Capability Comparison",
                    barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed capabilities
        with st.expander("📋 Detailed Agent Capabilities"):
            for agent_name, caps in capabilities.items():
                st.write(f"**{agent_name.title()}:**")
                st.write(f"- {caps['description']}")
                st.write(f"- Tools: {', '.join(caps['tools'])}")
                st.write(f"- Best for: {', '.join(caps['best_for'])}")
                st.write("---")
    
    with col2:
        st.subheader("🔍 Query Classification & Routing")
        
        # Simulate query classification data
        query_classification = pd.DataFrame({
            'Query_Type': ['Factual', 'Conceptual', 'Analytical', 'Research', 'Code'],
            'Count': [45, 32, 28, 67, 23],
            'Avg_Response_Time': [1.2, 2.1, 2.8, 1.9, 3.2]
        })
        
        # Create dual-axis chart
        fig = go.Figure()
        
        # Add bar chart for count
        fig.add_trace(go.Bar(
            name='Query Count',
            x=query_classification['Query_Type'],
            y=query_classification['Count'],
            yaxis='y',
            marker_color='lightblue'
        ))
        
        # Add line chart for response time
        fig.add_trace(go.Scatter(
            name='Avg Response Time (s)',
            x=query_classification['Query_Type'],
            y=query_classification['Avg_Response_Time'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red', width=3)
        ))
        
        # Update layout
        fig.update_layout(
            title="Query Type Distribution & Performance",
            xaxis_title="Query Type",
            yaxis=dict(title="Query Count", side="left"),
            yaxis2=dict(title="Avg Response Time (s)", side="right", overlaying="y"),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show routing insights
        with st.expander("🧠 Intelligent Routing Insights"):
            st.write("**Query Classification Patterns:**")
            st.write("- **Factual queries** → Researcher Agent (fast, accurate)")
            st.write("- **Conceptual queries** → Analyst Agent (deep analysis)")
            st.write("- **Code queries** → Coder Agent (technical expertise)")
            st.write("- **Research queries** → Researcher Agent (web search)")
            st.write("- **Analytical queries** → Analyst Agent (pattern recognition)")

# --- Enterprise Demo Tab ---
with tab5:
    st.markdown('<h2 class="section-header">Enterprise Use Case Demonstration</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 **Complete Workflow Demonstration**
    
    This tab showcases a comprehensive enterprise workflow that combines all advanced features:
    """)
    
    demo_scenario = st.selectbox(
        "Select Enterprise Scenario:",
        [
            "📊 Business Intelligence Analysis",
            "🔬 Research & Development",
            "📈 Market Analysis & Strategy",
            "🏗️ Technical Documentation Review"
        ]
    )
    
    if demo_scenario == "📊 Business Intelligence Analysis":
        st.subheader("Business Intelligence Analysis Workflow")
        
        if st.button("🚀 Run Complete BI Analysis"):
            with st.spinner("Executing enterprise BI workflow..."):
                # Simulate a complete BI workflow
                st.info("**Step 1:** Research Agent gathering market data...")
                st.success("✅ Market data collected from 15 sources")
                
                st.info("**Step 2:** Coder Agent processing financial data...")
                st.success("✅ Financial models executed, trends identified")
                
                st.info("**Step 3:** Analyst Agent synthesizing insights...")
                st.success("✅ Strategic recommendations generated")
                
                # Display mock results
                st.markdown("""
                ### 📋 **Executive Summary**
                
                **Key Findings:**
                - Market growth projected at 15.3% YoY
                - Competitor analysis reveals 3 key opportunities
                - Revenue optimization potential: $2.4M annually
                
                **Recommendations:**
                1. Expand into emerging markets (Q2 2024)
                2. Invest in AI/ML capabilities
                3. Optimize pricing strategy for premium segments
                """)
    
    # Feature showcase
    st.subheader("🌟 Advanced Features Showcase")
    
    features = [
        "Multi-agent collaboration with specialized roles",
        "Hybrid search combining semantic and keyword matching",
        "Intelligent query routing and strategy selection",
        "Real-time code execution in sandboxed environment",
        "Advanced document chunking with multiple strategies",
        "Enterprise-grade analytics and monitoring",
        "Scalable vector store management",
        "Memory-enhanced conversation flows"
    ]
    
    for feature in features:
        st.markdown(f"✅ {feature}")
    
    # Architecture diagram (text-based)
    st.subheader("🏗️ System Architecture")
    st.markdown("""
    ```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Streamlit UI  │    │  Multi-Agent    │    │  Advanced RAG   │
    │                 │◄──►│    System       │◄──►│     System      │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
              │                        │                        │
              ▼                        ▼                        ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   User Interface│    │  LangChain      │    │  Vector Stores  │
    │   Components    │    │  Agents & Tools │    │  & Retrievers   │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
              │                        │                        │
              └────────────────────────┼────────────────────────┘
                                       ▼
                             ┌─────────────────┐
                             │   OpenAI API    │
                             │   GPT Models    │
                             └─────────────────┘
    ```
    """)

# --- Model Registry Tab ---
with tab6:
    st.markdown('<h2 class="section-header">Model Registry & Versioning</h2>', unsafe_allow_html=True)
    
    # Initialize registry
    if 'model_registry' not in st.session_state:
        st.session_state['model_registry'] = ModelRegistryManager()
    
    registry = st.session_state['model_registry']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📦 Register New Model")
        
        model_name = st.text_input("Model Name", placeholder="e.g., sentiment-classifier")
        model_version = st.text_input("Version", placeholder="e.g., 1.0.0")
        model_type = st.selectbox("Model Type", [mt.value for mt in ModelType])
        stage = st.selectbox("Stage", [ms.value for ms in ModelStage])
        description = st.text_area("Description", height=100)
        author = st.text_input("Author", value="Data Scientist")
        
        st.subheader("Performance Metrics")
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            accuracy = st.number_input("Accuracy", 0.0, 1.0, 0.85, 0.01)
            precision = st.number_input("Precision", 0.0, 1.0, 0.82, 0.01)
        with metric_col2:
            recall = st.number_input("Recall", 0.0, 1.0, 0.88, 0.01)
            f1_score = st.number_input("F1 Score", 0.0, 1.0, 0.85, 0.01)
        
        performance_metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
        
        hyperparameters = {
            "learning_rate": st.number_input("Learning Rate", 0.0001, 1.0, 0.001, 0.0001),
            "batch_size": st.number_input("Batch Size", 16, 512, 32, 16),
            "epochs": st.number_input("Epochs", 1, 100, 10, 1)
        }
        
        if st.button("📝 Register Model", type="primary"):
            # Create a dummy model for demo
            from sklearn.linear_model import LogisticRegression
            dummy_model = LogisticRegression()
            dummy_model.fit(np.random.randn(10, 5), np.random.randint(0, 2, 10))
            
            try:
                model_id = registry.register_model(
                    model=dummy_model,
                    name=model_name,
                    version=model_version,
                    model_type=ModelType(model_type),
                    description=description,
                    author=author,
                    performance_metrics=performance_metrics,
                    hyperparameters=hyperparameters,
                    stage=ModelStage(stage)
                )
                st.success(f"✅ Model registered with ID: {model_id}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("📋 Registered Models")
        
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_name = st.text_input("Filter by Name", "")
        with filter_col2:
            filter_stage = st.selectbox("Filter by Stage", ["All"] + [ms.value for ms in ModelStage])
        
        # List models
        filters = {}
        if filter_name:
            filters['name'] = filter_name
        if filter_stage != "All":
            filters['stage'] = ModelStage(filter_stage)
        
        models = registry.list_models(**filters)
        
        if models:
            df = pd.DataFrame(models)
            st.dataframe(
                df[['name', 'version', 'stage', 'model_type', 'model_size_mb', 'created_at']],
                use_container_width=True
            )
            
            # Model comparison
            if len(models) >= 2:
                st.subheader("🔍 Compare Models")
                compare_col1, compare_col2 = st.columns(2)
                with compare_col1:
                    model1_name = st.selectbox("Model 1", [m['name'] for m in models])
                    model1_version = st.selectbox("Version 1", 
                        [m['version'] for m in models if m['name'] == model1_name])
                with compare_col2:
                    model2_name = st.selectbox("Model 2", [m['name'] for m in models])
                    model2_version = st.selectbox("Version 2",
                        [m['version'] for m in models if m['name'] == model2_name])
                
                if st.button("Compare"):
                    comparison = registry.compare_models(model1_name, model1_version, model2_version)
                    st.json(comparison)
        else:
            st.info("No models registered yet")

# --- A/B Testing Tab ---
with tab7:
    st.markdown('<h2 class="section-header">A/B Testing Framework</h2>', unsafe_allow_html=True)
    
    # Initialize A/B testing framework
    if 'ab_testing' not in st.session_state:
        st.session_state['ab_testing'] = ABTestingFramework()
    
    ab_framework = st.session_state['ab_testing']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🧪 Create Experiment")
        
        exp_name = st.text_input("Experiment Name", placeholder="e.g., model-v2-test")
        exp_description = st.text_area("Description", height=80)
        hypothesis = st.text_area("Hypothesis", placeholder="Treatment model will improve accuracy by 5%")
        
        metric_name = st.text_input("Metric Name", value="accuracy")
        metric_type = st.selectbox("Metric Type", [mt.value for mt in MetricType])
        
        baseline_model = st.text_input("Baseline Model", placeholder="model-v1")
        treatment_model = st.text_input("Treatment Model", placeholder="model-v2")
        
        traffic_split = st.slider("Traffic Split (%)", 0, 100, 50) / 100.0
        min_sample_size = st.number_input("Min Sample Size", 100, 100000, 1000, 100)
        max_duration_days = st.number_input("Max Duration (days)", 1, 90, 7, 1)
        significance_level = st.number_input("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
        
        if st.button("🚀 Create Experiment", type="primary"):
            config = ExperimentConfig(
                name=exp_name,
                description=exp_description,
                hypothesis=hypothesis,
                metric_name=metric_name,
                metric_type=MetricType(metric_type),
                baseline_model=baseline_model,
                treatment_model=treatment_model,
                traffic_split=traffic_split,
                min_sample_size=min_sample_size,
                max_duration_days=max_duration_days,
                significance_level=significance_level
            )
            
            try:
                exp_id = ab_framework.create_experiment(config)
                st.success(f"✅ Experiment created with ID: {exp_id}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.subheader("📊 Sample Size Calculator")
        baseline_rate = st.number_input("Baseline Rate", 0.0, 1.0, 0.5, 0.01)
        mde = st.number_input("Minimum Detectable Effect (%)", 1, 50, 5, 1) / 100.0
        
        if st.button("Calculate"):
            sample_size = ab_framework.calculate_sample_size(baseline_rate, mde)
            st.info(f"Required sample size per variant: **{sample_size}**")
    
    with col2:
        st.subheader("📈 Active Experiments")
        
        experiments = ab_framework.list_experiments(status=ExperimentStatus.RUNNING)
        
        if experiments:
            for exp in experiments:
                with st.expander(f"🔬 {exp['name']} (ID: {exp['id']})"):
                    st.write(f"**Status:** {exp['status']}")
                    st.write(f"**Metric:** {exp['metric_name']}")
                    st.write(f"**Baseline:** {exp['baseline_model']}")
                    st.write(f"**Treatment:** {exp['treatment_model']}")
                    
                    if st.button(f"Analyze Experiment {exp['id']}", key=f"analyze_{exp['id']}"):
                        with st.spinner("Analyzing..."):
                            results = ab_framework.analyze_experiment(exp['id'])
                            st.json(results)
        else:
            st.info("No active experiments")
        
        # Simulate experiment data
        st.subheader("🎲 Simulate Experiment Data")
        sim_exp_id = st.number_input("Experiment ID", 1, 100, 1)
        num_events = st.number_input("Number of Events", 10, 10000, 100, 10)
        
        if st.button("Generate Simulated Data"):
            np.random.seed(42)
            for i in range(num_events):
                # Simulate slightly better treatment
                baseline_value = np.random.normal(0.75, 0.1)
                treatment_value = np.random.normal(0.78, 0.1)  # 3% improvement
                
                user_id = f"user_{i}"
                ab_framework.record_event(sim_exp_id, user_id, baseline_value if i % 2 == 0 else treatment_value)
            
            st.success(f"✅ Generated {num_events} events for experiment {sim_exp_id}")

# --- Experiment Tracking Tab ---
with tab8:
    st.markdown('<h2 class="section-header">Experiment Tracking (MLflow-like)</h2>', unsafe_allow_html=True)
    
    # Initialize experiment tracking
    if 'experiment_tracking' not in st.session_state:
        st.session_state['experiment_tracking'] = ExperimentTracking()
    
    tracking = st.session_state['experiment_tracking']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 Start New Run")
        
        exp_name = st.text_input("Experiment Name", value="model-training")
        run_name = st.text_input("Run Name (optional)", placeholder="Auto-generated if empty")
        
        if st.button("▶️ Start Run", type="primary"):
            run_id = tracking.start_run(exp_name, run_name if run_name else None)
            st.session_state['current_run_id'] = run_id
            st.success(f"✅ Run started with ID: {run_id}")
        
        if 'current_run_id' in st.session_state:
            st.info(f"Current Run ID: {st.session_state['current_run_id']}")
            
            st.subheader("Log Parameters")
            param_name = st.text_input("Parameter Name")
            param_value = st.text_input("Parameter Value")
            if st.button("Add Parameter"):
                tracking.log_params(st.session_state['current_run_id'], {param_name: param_value})
                st.success("Parameter logged")
            
            st.subheader("Log Metrics")
            metric_name = st.text_input("Metric Name")
            metric_value = st.number_input("Metric Value", 0.0, 1.0, 0.85, 0.01)
            step = st.number_input("Step (optional)", 0, 1000, 0, 1)
            if st.button("Add Metric"):
                tracking.log_metrics(
                    st.session_state['current_run_id'],
                    {metric_name: metric_value},
                    step if step > 0 else None
                )
                st.success("Metric logged")
            
            if st.button("✅ End Run"):
                tracking.end_run(st.session_state['current_run_id'])
                st.success("Run completed")
                del st.session_state['current_run_id']
    
    with col2:
        st.subheader("📊 Experiment Runs")
        
        search_exp_name = st.text_input("Search by Experiment Name", "")
        runs = tracking.search_runs(experiment_name=search_exp_name if search_exp_name else None)
        
        if runs:
            runs_df = pd.DataFrame([{
                'run_id': r['id'],
                'run_name': r['run_name'],
                'experiment': r['experiment_name'],
                'status': r['status'],
                'duration_sec': r['duration_seconds']
            } for r in runs])
            st.dataframe(runs_df, use_container_width=True)
            
            # Compare runs
            if len(runs) >= 2:
                st.subheader("🔍 Compare Runs")
                run_ids = st.multiselect("Select Runs to Compare", [r['id'] for r in runs])
                if run_ids and st.button("Compare"):
                    comparison_df = tracking.compare_runs(run_ids)
                    st.dataframe(comparison_df, use_container_width=True)
        else:
            st.info("No runs found")

# --- Model Monitoring Tab ---
with tab9:
    st.markdown('<h2 class="section-header">Model Performance Monitoring</h2>', unsafe_allow_html=True)
    
    # Initialize monitoring
    if 'model_monitoring' not in st.session_state:
        st.session_state['model_monitoring'] = ModelMonitoring()
    
    monitoring = st.session_state['model_monitoring']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Log Performance")
        
        model_name = st.text_input("Model Name", value="sentiment-classifier")
        model_version = st.text_input("Version", value="1.0.0")
        metric_name = st.text_input("Metric Name", value="accuracy")
        metric_value = st.number_input("Metric Value", 0.0, 1.0, 0.85, 0.01)
        prediction_count = st.number_input("Prediction Count", 1, 100000, 100, 1)
        
        if st.button("📝 Log Performance", type="primary"):
            monitoring.log_performance(
                model_name, model_version, metric_name, metric_value, prediction_count
            )
            st.success("Performance logged")
        
        st.subheader("🔍 Check for Drift")
        check_model = st.text_input("Model Name (for drift)", value="sentiment-classifier")
        check_version = st.text_input("Version (for drift)", value="1.0.0")
        check_metric = st.text_input("Metric Name (for drift)", value="accuracy")
        lookback_days = st.number_input("Lookback Days", 1, 30, 7, 1)
        
        if st.button("🔍 Detect Drift"):
            drift_results = monitoring.detect_performance_drift(
                check_model, check_version, check_metric, lookback_days
            )
            st.json(drift_results)
    
    with col2:
        st.subheader("📈 Performance Trends")
        
        trend_model = st.text_input("Model Name (for trends)", value="sentiment-classifier")
        trend_version = st.text_input("Version (for trends)", value="1.0.0")
        trend_metric = st.text_input("Metric Name (for trends)", value="accuracy")
        trend_days = st.number_input("Days to Show", 1, 90, 30, 1)
        
        if st.button("📊 Generate Report"):
            report = monitoring.generate_monitoring_report(trend_model, trend_version, trend_days)
            
            if 'error' not in report:
                st.subheader("Monitoring Report")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Predictions", report['total_predictions'])
                with col2:
                    st.metric("Report Period", f"{report['report_period_days']} days")
                with col3:
                    st.metric("Metrics Tracked", len(report['metrics']))
                
                # Metrics breakdown
                for metric_name, metric_data in report['metrics'].items():
                    with st.expander(f"📊 {metric_name}"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Mean", f"{metric_data['mean']:.4f}")
                        with col2:
                            st.metric("Std", f"{metric_data['std']:.4f}")
                        with col3:
                            st.metric("Min", f"{metric_data['min']:.4f}")
                        with col4:
                            st.metric("Max", f"{metric_data['max']:.4f}")
                        
                        # Drift status
                        if metric_data['drift_detected']:
                            st.warning(f"⚠️ Drift detected! Severity: {metric_data['drift_severity']}")
                        else:
                            st.success("✅ No drift detected")
                
                # Performance trends chart
                trends_df = monitoring.get_performance_trends(trend_model, trend_version, trend_metric, trend_days)
                if not trends_df.empty:
                    fig = px.line(
                        trends_df,
                        x='timestamp',
                        y='metric_value',
                        title=f"{trend_metric} Over Time",
                        labels={'metric_value': trend_metric, 'timestamp': 'Date'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(report['error'])

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p><strong>Enterprise LangChain AI Workbench</strong> - Advanced LLM Orchestration Platform</p>
    <p>Built with LangChain • OpenAI • Streamlit • Python</p>
    <p><strong>Now featuring:</strong> Model Registry • A/B Testing • Experiment Tracking • Model Monitoring</p>
</div>
""", unsafe_allow_html=True) 