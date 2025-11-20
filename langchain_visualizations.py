"""Advanced visualizations for LangChain execution traces and agent reasoning."""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
from datetime import datetime


def create_execution_flow_diagram(chain_steps: List[Dict[str, Any]]) -> go.Figure:
    """Create Sankey diagram showing chain execution flow."""
    if not chain_steps:
        return go.Figure()
    
    nodes = []
    node_labels = []
    source_indices = []
    target_indices = []
    values = []
    
    for idx, step in enumerate(chain_steps):
        step_name = step.get('step', f'Step {idx+1}')
        node_labels.append(step_name)
        nodes.append(idx)
        
        if idx > 0:
            source_indices.append(idx - 1)
            target_indices.append(idx)
            values.append(1)
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=["#667eea", "#4facfe", "#43e97b", "#fa709a", "#f093fb"][:len(node_labels)]
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=["rgba(102, 126, 234, 0.4)"] * len(source_indices)
        )
    )])
    
    fig.update_layout(
        title="LangChain Execution Flow",
        font_size=12,
        height=400
    )
    
    return fig


def create_token_usage_chart(token_usage: Dict[str, int], historical: Optional[List[Dict]] = None) -> go.Figure:
    """Create token usage visualization."""
    if historical:
        df = pd.DataFrame(historical)
        df['timestamp'] = pd.to_datetime(df.get('timestamp', pd.Timestamp.now()))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df.get('prompt_tokens', []),
            mode='lines+markers',
            name='Prompt Tokens',
            line=dict(color='#667eea', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df.get('completion_tokens', []),
            mode='lines+markers',
            name='Completion Tokens',
            line=dict(color='#4facfe', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df.get('total_tokens', []),
            mode='lines+markers',
            name='Total Tokens',
            line=dict(color='#43e97b', width=3)
        ))
        
        fig.update_layout(
            title="Token Usage Over Time",
            xaxis_title="Time",
            yaxis_title="Tokens",
            hovermode='x unified',
            height=400,
            template="plotly_white"
        )
    else:
        categories = ['Prompt', 'Completion', 'Total']
        values = [
            token_usage.get('prompt_tokens', 0),
            token_usage.get('completion_tokens', 0),
            token_usage.get('total_tokens', 0)
        ]
        
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            marker_color=['#667eea', '#4facfe', '#43e97b'],
            text=values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Current Token Usage",
            yaxis_title="Tokens",
            height=300,
            template="plotly_white"
        )
    
    return fig


def create_agent_reasoning_timeline(reasoning_steps: List[Dict[str, Any]]) -> go.Figure:
    """Create timeline visualization of agent reasoning process."""
    if not reasoning_steps:
        return go.Figure()
    
    df = pd.DataFrame(reasoning_steps)
    df['timestamp'] = pd.to_datetime(df.get('timestamp', pd.Timestamp.now()))
    
    colors = {
        'action': '#667eea',
        'observation': '#4facfe',
        'finish': '#43e97b',
        'error': '#f5576c'
    }
    
    fig = go.Figure()
    
    for step_type in df.get('type', []).unique():
        type_data = df[df.get('type') == step_type]
        fig.add_trace(go.Scatter(
            x=type_data['timestamp'],
            y=type_data.get('step', range(len(type_data))),
            mode='markers+lines',
            name=step_type.title(),
            marker=dict(
                size=12,
                color=colors.get(step_type, '#888888'),
                symbol='circle'
            ),
            line=dict(width=2, color=colors.get(step_type, '#888888'))
        ))
    
    fig.update_layout(
        title="Agent Reasoning Timeline",
        xaxis_title="Time",
        yaxis_title="Step Number",
        hovermode='closest',
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_rag_retrieval_visualization(retrieved_docs: List[Dict[str, Any]]) -> go.Figure:
    """Visualize RAG retrieval with similarity scores."""
    if not retrieved_docs:
        return go.Figure()
    
    scores = [doc.get('score', 0.0) for doc in retrieved_docs]
    doc_indices = [f"Doc {i+1}" for i in range(len(retrieved_docs))]
    
    fig = go.Figure(data=[go.Bar(
        x=doc_indices,
        y=scores,
        marker=dict(
            color=scores,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Similarity Score")
        ),
        text=[f"{s:.3f}" for s in scores],
        textposition='auto'
    )])
    
    fig.update_layout(
        title="RAG Retrieval Scores",
        xaxis_title="Retrieved Documents",
        yaxis_title="Similarity Score",
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_chain_performance_comparison(chain_metrics: List[Dict[str, Any]]) -> go.Figure:
    """Compare performance of different chain strategies."""
    if not chain_metrics:
        return go.Figure()
    
    df = pd.DataFrame(chain_metrics)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Latency (s)',
        x=df.get('chain_name', []),
        y=df.get('latency', []),
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Bar(
        name='Token Usage',
        x=df.get('chain_name', []),
        y=df.get('tokens', []),
        marker_color='#4facfe',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Chain Performance Comparison",
        xaxis_title="Chain Strategy",
        yaxis=dict(title="Latency (seconds)", side='left'),
        yaxis2=dict(title="Token Usage", overlaying='y', side='right'),
        barmode='group',
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_agent_decision_tree(agent_actions: List[Dict[str, Any]]) -> go.Figure:
    """Create decision tree visualization of agent tool selection."""
    if not agent_actions:
        return go.Figure()
    
    tool_counts = {}
    for action in agent_actions:
        tool = action.get('action_type', 'unknown')
        tool_counts[tool] = tool_counts.get(tool, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(tool_counts.keys()),
        values=list(tool_counts.values()),
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3[:len(tool_counts)]
    )])
    
    fig.update_layout(
        title="Agent Tool Usage Distribution",
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_cost_estimation_chart(token_usage: Dict[str, int], model_pricing: Dict[str, float]) -> go.Figure:
    """Estimate costs based on token usage and model pricing."""
    prompt_cost = (token_usage.get('prompt_tokens', 0) / 1000) * model_pricing.get('prompt_per_1k', 0.002)
    completion_cost = (token_usage.get('completion_tokens', 0) / 1000) * model_pricing.get('completion_per_1k', 0.002)
    total_cost = prompt_cost + completion_cost
    
    fig = go.Figure(data=[go.Bar(
        x=['Prompt', 'Completion', 'Total'],
        y=[prompt_cost, completion_cost, total_cost],
        marker_color=['#667eea', '#4facfe', '#43e97b'],
        text=[f"${c:.4f}" for c in [prompt_cost, completion_cost, total_cost]],
        textposition='auto'
    )])
    
    fig.update_layout(
        title=f"Estimated Cost: ${total_cost:.4f}",
        yaxis_title="Cost (USD)",
        height=300,
        template="plotly_white"
    )
    
    return fig

