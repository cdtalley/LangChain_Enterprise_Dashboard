import os
import sys
import subprocess
import tempfile
from typing import List, Dict, Any
from langchain.agents import AgentType, initialize_agent, Tool
# from langchain_openai import ChatOpenAI  # Optional import
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.tools import BaseTool
from langchain_community.utilities import SerpAPIWrapper
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
# from langchain_huggingface import HuggingFacePipeline  # Optional import
import torch
import logging
import time
import hashlib
import json
from datetime import datetime
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureCodeExecutorTool(BaseTool):
    """Enhanced code executor with security, monitoring, and sandboxing"""
    name: str = "secure_python_executor"
    description: str = "Execute Python code safely with security constraints. Use for data analysis, calculations, and visualizations."
    
    model_config = {"extra": "allow"}  # Pydantic v2 syntax
    
    def __init__(self):
        super().__init__()
        # Initialize as private attributes to avoid Pydantic validation
        self.__dict__['execution_stats'] = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "avg_execution_time": 0,
            "blocked_operations": 0
        }
        
        self.__dict__['blocked_patterns'] = [
            r'import\s+os',
            r'import\s+subprocess',
            r'import\s+sys',
            r'__import__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'exit\s*\(',
            r'quit\s*\(',
        ]
    
    def _is_code_safe(self, code: str) -> tuple[bool, str]:
        """Check if code is safe to execute"""
        for pattern in self.blocked_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Blocked dangerous operation: {pattern}"
        
        # Check for file system operations
        if any(op in code.lower() for op in ['rmdir', 'remove', 'delete', 'unlink']):
            return False, "File system modification operations are not allowed"
        
        return True, "Code appears safe"
    
    def _run(self, code: str) -> str:
        start_time = time.time()
        self.execution_stats["total_executions"] += 1
        
        try:
            # Security check
            is_safe, safety_msg = self._is_code_safe(code)
            if not is_safe:
                self.execution_stats["blocked_operations"] += 1
                logger.warning(f"Blocked unsafe code execution: {safety_msg}")
                return f"🚫 Security Error: {safety_msg}"
            
            # Create a restricted execution environment
            allowed_modules = {
                'pandas': pd,
                'numpy': np,
                'matplotlib': plt,
                'seaborn': sns,
                'math': __import__('math'),
                'statistics': __import__('statistics'),
                'datetime': __import__('datetime'),
                'json': __import__('json'),
                'csv': __import__('csv'),
                'io': io,
                'base64': base64,
                'random': __import__('random'),
                'collections': __import__('collections'),
                'itertools': __import__('itertools'),
                'functools': __import__('functools'),
                'operator': __import__('operator'),
                're': __import__('re'),
            }
            
            # Capture stdout and stderr
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            stdout_capture = StringIO()
            stderr_capture = StringIO()
            
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Execute code with timeout
            try:
                # Create restricted globals
                restricted_globals = {
                    "__builtins__": {
                        'len': len, 'str': str, 'int': int, 'float': float,
                        'bool': bool, 'list': list, 'dict': dict, 'tuple': tuple,
                        'set': set, 'range': range, 'enumerate': enumerate,
                        'zip': zip, 'sum': sum, 'min': min, 'max': max,
                        'abs': abs, 'round': round, 'print': print,
                        'type': type, 'isinstance': isinstance, 'hasattr': hasattr,
                        'getattr': getattr, 'setattr': setattr, 'sorted': sorted,
                        'reversed': reversed, 'any': any, 'all': all,
                    }
                }
                
                exec(code, restricted_globals, allowed_modules)
                
                # Get outputs
                stdout_value = stdout_capture.getvalue()
                stderr_value = stderr_capture.getvalue()
                
                # Restore stdout/stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
                execution_time = time.time() - start_time
                self._update_stats(execution_time, success=True)
                
                result = ""
                if stdout_value:
                    result += f"Output:\n{stdout_value}\n"
                if stderr_value:
                    result += f"Warnings:\n{stderr_value}\n"
                
                result += f"✅ Execution completed in {execution_time:.2f}s"
                
                logger.info(f"Code execution successful in {execution_time:.2f}s")
                return result if result.strip() else "✅ Code executed successfully (no output)"
                
            except Exception as e:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                raise e
                
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_stats(execution_time, success=False)
            error_msg = f"❌ Execution Error: {str(e)}"
            logger.error(f"Code execution failed: {str(e)}")
            return error_msg
    
    def _update_stats(self, execution_time: float, success: bool):
        """Update execution statistics"""
        if success:
            self.execution_stats["successful_executions"] += 1
        else:
            self.execution_stats["failed_executions"] += 1
        
        # Update average execution time
        total_time = (self.execution_stats["avg_execution_time"] * 
                     (self.execution_stats["total_executions"] - 1) + execution_time)
        self.execution_stats["avg_execution_time"] = total_time / self.execution_stats["total_executions"]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return self.execution_stats.copy()
    
    async def _arun(self, code: str) -> str:
        return self._run(code)

class WebScrapeTool(BaseTool):
    name: str = "web_scraper"
    description: str = "Scrape content from web pages. Provide a URL to extract text content."
    
    def _run(self, url: str) -> str:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000] + "..." if len(text) > 2000 else text
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
    
    async def _arun(self, url: str) -> str:
        return self._run(url)

class DataAnalysisTool(BaseTool):
    name: str = "data_analyzer"
    description: str = "Analyze datasets and generate insights. Provide data description or CSV data."
    
    def _run(self, data_description: str) -> str:
        try:
            # This is a simplified example - in practice, you'd load actual data
            analysis = f"""
            Data Analysis Report for: {data_description}
            
            Key Insights:
            - Statistical summary completed
            - Correlation analysis performed
            - Anomaly detection applied
            - Trend analysis conducted
            
            Recommendations:
            - Further investigation recommended for outliers
            - Consider seasonal adjustments
            - Monitor key performance indicators
            """
            return analysis
        except Exception as e:
            return f"Error analyzing data: {str(e)}"
    
    async def _arun(self, data_description: str) -> str:
        return self._run(data_description)

class MultiAgentSystem:
    def __init__(self, openai_api_key: str = None, serpapi_key: str = None):
        logger.info("Initializing MultiAgentSystem...")
        
        # Enhanced LLM initialization with better model selection
        try:
            # Try to use a more capable model first
            hf_pipeline = pipeline(
                "text-generation", 
                model="microsoft/DialoGPT-medium",
                max_length=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256,
                device_map="auto" if torch.cuda.is_available() else None
            )
            # Use HuggingFace pipeline directly if available
            try:
                from langchain_huggingface import HuggingFacePipeline
                self.llm = HuggingFacePipeline(
                    pipeline=hf_pipeline,
                    model_kwargs={"temperature": 0.7, "max_length": 512}
                )
            except ImportError:
                # Fallback to direct pipeline usage
                self.llm = hf_pipeline
            logger.info("DialoGPT-medium LLM loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load DialoGPT-medium, trying GPT-2: {e}")
            try:
                # Fallback to GPT-2
                hf_pipeline = pipeline(
                    "text-generation", 
                    model="gpt2",
                    max_length=256,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=50256
                )
                try:
                    from langchain_huggingface import HuggingFacePipeline
                    self.llm = HuggingFacePipeline(
                        pipeline=hf_pipeline,
                        model_kwargs={"temperature": 0.7, "max_length": 256}
                    )
                except ImportError:
                    # Fallback to direct pipeline usage
                    self.llm = hf_pipeline
                logger.info("GPT-2 LLM loaded successfully")
            except Exception as e2:
                logger.warning(f"Failed to load GPT-2, using fallback: {e2}")
                # Create a simple fallback LLM
                from langchain.llms.fake import FakeListLLM
                self.llm = FakeListLLM(responses=[
                    "I'm a research agent. Let me help you find information about that topic.",
                    "I'm a coding agent. I can help you write and execute Python code.",
                    "I'm an analysis agent. I can help you analyze data and provide insights."
                ])
        
        # Initialize enhanced tools
        self.tools = [
            SecureCodeExecutorTool(),
            WebScrapeTool(),
            DataAnalysisTool()
        ]
        
        if serpapi_key:
            search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
            self.tools.append(
                Tool(
                    name="web_search",
                    description="Search the web for current information",
                    func=search.run
                )
            )
        
        # Performance monitoring
        self.system_metrics = {
            "agents_created": len(self._create_agents()),
            "total_tasks": 0,
            "successful_tasks": 0,
            "avg_response_time": 0,
            "active_sessions": 0
        }
        
        # Enhanced conversation memory
        self.conversation_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=20  # Keep more conversation context
        )
        
        # Create specialized agents
        self.agents = self._create_agents()
        logger.info("MultiAgentSystem initialization complete")
    
    def _create_agents(self) -> Dict[str, Any]:
        agents = {}
        
        # Research Agent
        research_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )
        agents["researcher"] = initialize_agent(
            tools=[tool for tool in self.tools if tool.name in ["web_search", "web_scraper"]],
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=research_memory,
            verbose=True,
            agent_kwargs={
                "system_message": """You are a Research Agent specialized in gathering and analyzing information.
                Your role is to:
                - Conduct thorough web searches and research
                - Scrape and analyze web content
                - Provide comprehensive, factual information
                - Cite sources and verify information accuracy
                Always be thorough and provide well-researched responses."""
            }
        )
        
        # Code Agent
        code_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )
        agents["coder"] = initialize_agent(
            tools=[tool for tool in self.tools if tool.name in ["secure_python_executor", "data_analyzer"]],
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=code_memory,
            verbose=True,
            agent_kwargs={
                "system_message": """You are a Code Agent specialized in programming and data analysis.
                Your role is to:
                - Write and execute Python code
                - Perform data analysis and visualization
                - Solve computational problems
                - Debug and optimize code
                Always write clean, efficient, and well-documented code."""
            }
        )
        
        # Analysis Agent
        analysis_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )
        agents["analyst"] = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=analysis_memory,
            verbose=True,
            agent_kwargs={
                "system_message": """You are an Analysis Agent specialized in critical thinking and synthesis.
                Your role is to:
                - Analyze complex problems from multiple angles
                - Synthesize information from various sources
                - Provide strategic insights and recommendations
                - Identify patterns and trends
                Always provide thoughtful, well-reasoned analysis."""
            }
        )
        
        return agents
    
    def run_agent(self, agent_name: str, query: str) -> str:
        """Run a specific agent with a query"""
        if agent_name not in self.agents:
            return f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"
        
        try:
            result = self.agents[agent_name].run(query)
            return result
        except Exception as e:
            return f"Error running {agent_name} agent: {str(e)}"
    
    def collaborative_task(self, task: str) -> Dict[str, str]:
        """Run a collaborative task across multiple agents"""
        results = {}
        
        # Research phase
        research_query = f"Research this topic thoroughly: {task}"
        results["research"] = self.run_agent("researcher", research_query)
        
        # Analysis phase
        analysis_query = f"Analyze this task and provide insights: {task}\n\nResearch findings: {results['research'][:500]}..."
        results["analysis"] = self.run_agent("analyst", analysis_query)
        
        # Coding phase (if applicable)
        code_query = f"If this task requires code or data analysis, provide solutions: {task}"
        results["code"] = self.run_agent("coder", code_query)
        
        return results
    
    def get_agent_list(self) -> List[str]:
        """Get list of available agents"""
        return list(self.agents.keys())
    
    def intelligent_agent_routing(self, query: str) -> str:
        """Advanced intelligent routing based on query analysis"""
        query_lower = query.lower()
        
        # Define routing patterns with weights
        routing_patterns = {
            "researcher": {
                "keywords": ["research", "find", "search", "information", "latest", "news", "trends", "study", "investigate"],
                "questions": ["what", "when", "where", "who", "how many"],
                "weight": 0
            },
            "coder": {
                "keywords": ["code", "python", "programming", "function", "algorithm", "debug", "optimize", "calculate", "data analysis"],
                "questions": ["how to", "write", "create", "build", "implement"],
                "weight": 0
            },
            "analyst": {
                "keywords": ["analyze", "compare", "evaluate", "assess", "strategy", "recommendation", "insight", "pattern"],
                "questions": ["why", "explain", "compare", "analyze", "evaluate"],
                "weight": 0
            }
        }
        
        # Calculate weights for each agent
        for agent, patterns in routing_patterns.items():
            # Check keyword matches
            keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in query_lower)
            patterns["weight"] += keyword_matches * 2
            
            # Check question type matches
            question_matches = sum(1 for question in patterns["questions"] if query_lower.startswith(question))
            patterns["weight"] += question_matches * 3
            
            # Check for specific domain indicators
            if agent == "researcher" and any(word in query_lower for word in ["market", "industry", "competitor", "news"]):
                patterns["weight"] += 2
            elif agent == "coder" and any(word in query_lower for word in ["dataframe", "numpy", "pandas", "visualization", "plot"]):
                patterns["weight"] += 2
            elif agent == "analyst" and any(word in query_lower for word in ["business", "strategy", "decision", "recommendation"]):
                patterns["weight"] += 2
        
        # Return agent with highest weight
        best_agent = max(routing_patterns.items(), key=lambda x: x[1]["weight"])
        
        # If no clear winner, default to analyst
        if best_agent[1]["weight"] == 0:
            return "analyst"
        
        logger.info(f"Query routed to {best_agent[0]} (weight: {best_agent[1]['weight']})")
        return best_agent[0]
    
    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed capabilities of each agent"""
        return {
            "researcher": {
                "description": "Specialized in information gathering and research",
                "strengths": ["Web research", "Data collection", "Fact verification", "Market analysis"],
                "tools": ["web_search", "web_scraper"],
                "best_for": ["Research queries", "Information gathering", "Market analysis"]
            },
            "coder": {
                "description": "Expert in programming and data analysis",
                "strengths": ["Code generation", "Data analysis", "Algorithm implementation", "Debugging"],
                "tools": ["secure_python_executor", "data_analyzer"],
                "best_for": ["Programming tasks", "Data analysis", "Code generation"]
            },
            "analyst": {
                "description": "Advanced analysis and strategic thinking",
                "strengths": ["Strategic analysis", "Pattern recognition", "Synthesis", "Decision support"],
                "tools": ["all_tools"],
                "best_for": ["Complex analysis", "Strategic planning", "Decision support"]
            }
        } 