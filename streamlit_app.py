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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 Multi-Agent System", 
    "📊 Advanced RAG", 
    "🔧 Tool Execution", 
    "📈 Analytics Dashboard",
    "🎯 Enterprise Demo"
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
                        # Intelligent routing based on task content
                        if any(word in task.lower() for word in ["research", "find", "search", "information"]):
                            agent_to_use = "researcher"
                        elif any(word in task.lower() for word in ["code", "python", "analyze", "data", "calculate"]):
                            agent_to_use = "coder"
                        else:
                            agent_to_use = "analyst"
                        
                        st.info(f"🎯 Auto-routed to: **{agent_to_use.title()} Agent**")
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
    
    # Agent performance comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Agent Performance")
        agent_perf = pd.DataFrame({
            'Agent': ['Researcher', 'Coder', 'Analyst'],
            'Success_Rate': [95.2, 91.8, 97.1],
            'Avg_Time': [2.1, 3.4, 1.9]
        })
        
        fig = px.bar(agent_perf, x='Agent', y='Success_Rate', title="Agent Success Rates")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔍 Query Distribution")
        query_types = pd.DataFrame({
            'Type': ['Research', 'Analysis', 'Code Generation', 'Q&A'],
            'Count': [45, 32, 28, 67]
        })
        
        fig = px.pie(query_types, values='Count', names='Type', title="Query Type Distribution")
        st.plotly_chart(fig, use_container_width=True)

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

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p><strong>Enterprise LangChain AI Workbench</strong> - Advanced LLM Orchestration Platform</p>
    <p>Built with LangChain • OpenAI • Streamlit • Python</p>
</div>
""", unsafe_allow_html=True) 