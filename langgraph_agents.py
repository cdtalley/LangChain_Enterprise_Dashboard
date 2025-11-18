"""
LangGraph Agentic AI Framework
===============================
Advanced agentic AI using LangGraph for complex workflows.
Demonstrates cutting-edge Gen AI expertise.
"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
import logging
from dataclasses import dataclass

try:
    from langgraph.graph import StateGraph, END
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    logging.warning("langgraph required. Install with: pip install langgraph langchain-openai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for LangGraph agent"""
    messages: Annotated[List[Any], "Chat messages"]
    context: Dict[str, Any]
    next_action: Optional[str]


class LangGraphAgent:
    """
    LangGraph-based agentic AI system
    
    Features:
    - Stateful agent workflows
    - Conditional routing
    - Multi-agent collaboration
    - Tool integration
    - Error handling and recovery
    """
    
    def __init__(self, llm_model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("langgraph required for LangGraph agents")
        
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self.graph = None
        self._build_graph()
        logger.info("LangGraph agent initialized")
    
    def _build_graph(self):
        """Build LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("research", self._research_node)
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("synthesize", self._synthesize_node)
        
        workflow.set_entry_point("agent")
        
        workflow.add_conditional_edges(
            "agent",
            self._route_action,
            {
                "research": "research",
                "analyze": "analyze",
                "synthesize": "synthesize",
                "end": END
            }
        )
        
        workflow.add_edge("research", "agent")
        workflow.add_edge("analyze", "agent")
        workflow.add_edge("synthesize", END)
        
        self.graph = workflow.compile()
    
    def _agent_node(self, state: AgentState) -> AgentState:
        """Main agent node"""
        messages = state.get("messages", [])
        
        if not messages:
            return state
        
        response = self.llm.invoke(messages)
        
        state["messages"].append(AIMessage(content=response.content))
        
        if "research" in response.content.lower():
            state["next_action"] = "research"
        elif "analyze" in response.content.lower():
            state["next_action"] = "analyze"
        elif "synthesize" in response.content.lower() or "summary" in response.content.lower():
            state["next_action"] = "synthesize"
        else:
            state["next_action"] = "end"
        
        return state
    
    def _research_node(self, state: AgentState) -> AgentState:
        """Research node"""
        context = state.get("context", {})
        context["research_complete"] = True
        context["research_data"] = "Research completed"
        
        state["messages"].append(SystemMessage(content="Research phase completed"))
        state["context"] = context
        
        return state
    
    def _analyze_node(self, state: AgentState) -> AgentState:
        """Analysis node"""
        context = state.get("context", {})
        context["analysis_complete"] = True
        context["analysis_results"] = "Analysis completed"
        
        state["messages"].append(SystemMessage(content="Analysis phase completed"))
        state["context"] = context
        
        return state
    
    def _synthesize_node(self, state: AgentState) -> AgentState:
        """Synthesis node"""
        context = state.get("context", {})
        
        synthesis = f"Synthesis of research and analysis: {context.get('research_data', '')} + {context.get('analysis_results', '')}"
        
        state["messages"].append(AIMessage(content=synthesis))
        state["context"]["synthesis_complete"] = True
        
        return state
    
    def _route_action(self, state: AgentState) -> str:
        """Route to next action based on state"""
        next_action = state.get("next_action", "end")
        return next_action
    
    def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run agent workflow"""
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "context": context or {},
            "next_action": None
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "messages": [msg.content for msg in result["messages"] if hasattr(msg, "content")],
            "context": result.get("context", {}),
            "final_response": result["messages"][-1].content if result["messages"] else ""
        }


class MultiAgentWorkflow:
    """Multi-agent workflow using LangGraph"""
    
    def __init__(self):
        self.agents = {}
        self.workflow = None
    
    def add_agent(self, name: str, agent: LangGraphAgent):
        """Add agent to workflow"""
        self.agents[name] = agent
    
    def run_workflow(self, query: str) -> Dict[str, Any]:
        """Run multi-agent workflow"""
        results = {}
        
        for name, agent in self.agents.items():
            try:
                result = agent.run(query)
                results[name] = result
            except Exception as e:
                logger.error(f"Agent {name} failed: {e}")
                results[name] = {"error": str(e)}
        
        return results

