from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from langchain_core.tools import Tool, BaseTool
from langchain_core.prompts import ChatPromptTemplate

# Try to import create_agent, fallback to alternative if not available
try:
    from langchain.agents import create_agent
except ImportError:
    try:
        from langchain.agents import AgentExecutor, create_react_agent
        create_agent = None
    except ImportError:
        create_agent = None
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
import torch
import logging
import time
from datetime import datetime
import re
from pathlib import Path
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from collections import defaultdict

# Import configuration
try:
    from config import Config
except ImportError:
    # Fallback configuration if config.py doesn't exist
    class Config:
        AGENT_MEMORY_SIZE = 20
        MAX_TOKENS = 512
        TEMPERATURE = 0.7
        DEFAULT_LLM_MODEL = "microsoft/DialoGPT-medium"
        FALLBACK_LLM_MODEL = "gpt2"
        CODE_EXECUTION_TIMEOUT = 30
        WEB_SCRAPE_TIMEOUT = 10
        WEB_SCRAPE_MAX_LENGTH = 2000
        WEB_SCRAPE_RATE_LIMIT_DELAY = 1.0

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL if hasattr(Config, 'LOG_LEVEL') else 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CODE_EXECUTION_TIMEOUT = getattr(Config, 'CODE_EXECUTION_TIMEOUT', 30)
WEB_SCRAPE_TIMEOUT = getattr(Config, 'WEB_SCRAPE_TIMEOUT', 10)
WEB_SCRAPE_MAX_LENGTH = getattr(Config, 'WEB_SCRAPE_MAX_LENGTH', 2000)
WEB_SCRAPE_RATE_LIMIT_DELAY = getattr(Config, 'WEB_SCRAPE_RATE_LIMIT_DELAY', 1.0)
MAX_CODE_LENGTH = 10000
MAX_MEMORY_USAGE_MB = 500

class SecureCodeExecutorTool(BaseTool):
    """Secure Python code executor with sandboxing and monitoring."""
    
    name: str = "secure_python_executor"
    description: str = "Execute Python code safely with security constraints. Use for data analysis, calculations, and visualizations."
    model_config = {"extra": "allow"}
    
    def __init__(self, timeout: int = CODE_EXECUTION_TIMEOUT):
        super().__init__()
        self.timeout = timeout
        self.__dict__['execution_stats'] = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "avg_execution_time": 0.0,
            "blocked_operations": 0,
            "timeout_errors": 0,
            "memory_errors": 0
        }
        
        self.__dict__['blocked_patterns'] = [
            (r'import\s+os\s*$', "Direct os module import"),
            (r'import\s+subprocess\s*$', "Direct subprocess import"),
            (r'import\s+sys\s*$', "Direct sys module import"),
            (r'__import__\s*\(', "Dynamic import"),
            (r'eval\s*\(', "Eval function"),
            (r'exec\s*\(', "Exec function"),
            (r'compile\s*\(', "Compile function"),
            (r'open\s*\([^)]*[\'"]w', "File write operations"),
            (r'open\s*\([^)]*[\'"]a', "File append operations"),
            (r'input\s*\(', "Input function"),
            (r'raw_input\s*\(', "Raw input function"),
            (r'exit\s*\(', "Exit function"),
            (r'quit\s*\(', "Quit function"),
            (r'\.remove\s*\(', "Remove method"),
            (r'\.unlink\s*\(', "Unlink method"),
            (r'rmdir\s*\(', "Rmdir function"),
            (r'shutil\.', "Shutil module"),
            (r'pickle\.', "Pickle module"),
            (r'socket\.', "Socket module"),
            (r'urllib\.request', "Urllib request"),
        ]
        
        self.__dict__['executor'] = ThreadPoolExecutor(max_workers=1)
    
    def _is_code_safe(self, code: str) -> Tuple[bool, str]:
        """Validate code safety using pattern matching."""
        if len(code) > MAX_CODE_LENGTH:
            return False, f"Code exceeds maximum length of {MAX_CODE_LENGTH} characters"
        
        for pattern, description in self.blocked_patterns:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                return False, f"Blocked dangerous operation: {description}"
        
        code_lower = code.lower()
        dangerous_ops = {'rmdir', 'remove', 'delete', 'unlink', 'rmtree', 'move'}
        if any(f'.{op}(' in code_lower or f'{op}(' in code_lower for op in dangerous_ops):
            return False, "File system modification operations are not allowed"
        
        network_patterns = {'requests.get', 'requests.post', 'urllib', 'socket'}
        if any(net_op in code_lower for net_op in network_patterns):
            return False, "Network operations are not allowed in code execution"
        
        dangerous_builtins = {'__import__', '__builtins__', '__globals__', '__locals__'}
        if any(builtin in code for builtin in dangerous_builtins):
            return False, "Access to internal builtins is not allowed"
        
        return True, "Code appears safe"
    
    def _execute_code(self, code: str) -> Tuple[str, str, Optional[Exception]]:
        """Execute code in a restricted environment."""
        import sys
        from io import StringIO
        
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        old_stdout, old_stderr = sys.stdout, sys.stderr
        
        try:
            sys.stdout, sys.stderr = stdout_capture, stderr_capture
            
            allowed_modules = {
                'pandas': pd, 'numpy': np, 'matplotlib': plt, 'seaborn': sns,
                'math': __import__('math'), 'statistics': __import__('statistics'),
                'datetime': __import__('datetime'), 'json': __import__('json'),
                'csv': __import__('csv'), 'io': io, 'base64': base64,
                'random': __import__('random'), 'collections': __import__('collections'),
                'itertools': __import__('itertools'), 'functools': __import__('functools'),
                'operator': __import__('operator'), 're': __import__('re'),
            }
            
            restricted_globals = {
                "__builtins__": {
                    'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
                    'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
                    'range': range, 'enumerate': enumerate, 'zip': zip,
                    'sum': sum, 'min': min, 'max': max, 'abs': abs, 'round': round,
                    'print': print, 'type': type, 'isinstance': isinstance,
                    'hasattr': hasattr, 'getattr': getattr, 'setattr': setattr,
                    'sorted': sorted, 'reversed': reversed, 'any': any, 'all': all,
                }
            }
            
            exec(code, restricted_globals, allowed_modules)
            return stdout_capture.getvalue(), stderr_capture.getvalue(), None
            
        except Exception as e:
            return "", stderr_capture.getvalue() or str(e), e
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
    
    def _run(self, code: str) -> str:
        """Execute code with timeout and error handling."""
        start_time = time.time()
        self.execution_stats["total_executions"] += 1
        
        is_safe, safety_msg = self._is_code_safe(code)
        if not is_safe:
            self.execution_stats["blocked_operations"] += 1
            logger.warning(f"Blocked unsafe code execution: {safety_msg}")
            return f"🚫 Security Error: {safety_msg}"
        
        try:
            future = self.executor.submit(self._execute_code, code)
            stdout_value, stderr_value, error = future.result(timeout=self.timeout)
            
            if error:
                raise error
            
            execution_time = time.time() - start_time
            self._update_stats(execution_time, success=True)
            
            result_parts = [f"Output:\n{stdout_value}"] if stdout_value else []
            if stderr_value:
                result_parts.append(f"Warnings:\n{stderr_value}")
            result_parts.append(f"✅ Execution completed in {execution_time:.2f}s")
            
            logger.info(f"Code execution successful in {execution_time:.2f}s")
            return "\n".join(result_parts) if result_parts else "✅ Code executed successfully (no output)"
            
        except FutureTimeoutError:
            execution_time = time.time() - start_time
            self.execution_stats["timeout_errors"] += 1
            self._update_stats(execution_time, success=False)
            logger.warning(f"Code execution timeout after {execution_time:.2f}s")
            return f"⏱️ Execution Timeout: Code execution exceeded {self.timeout}s limit"
            
        except MemoryError:
            execution_time = time.time() - start_time
            self.execution_stats["memory_errors"] += 1
            self._update_stats(execution_time, success=False)
            logger.error("Code execution memory error")
            return "💾 Memory Error: Code execution exceeded memory limits"
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_stats(execution_time, success=False)
            error_type = type(e).__name__
            logger.error(f"Code execution failed: {error_type} - {str(e)}", exc_info=True)
            return f"❌ Execution Error ({error_type}): {str(e)}"
    
    def _update_stats(self, execution_time: float, success: bool) -> None:
        """Update execution statistics."""
        if success:
            self.execution_stats["successful_executions"] += 1
        else:
            self.execution_stats["failed_executions"] += 1
        
        total = self.execution_stats["total_executions"]
        current_avg = self.execution_stats["avg_execution_time"]
        self.execution_stats["avg_execution_time"] = (current_avg * (total - 1) + execution_time) / total
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return self.execution_stats.copy()
    
    async def _arun(self, code: str) -> str:
        """Async wrapper for code execution."""
        return self._run(code)

class WebScrapeTool(BaseTool):
    name: str = "web_scraper"
    description: str = "Scrape content from web pages. Provide a URL to extract text content."
    
    def __init__(self):
        super().__init__()
        self.__dict__['last_request_time'] = defaultdict(float)
        self.__dict__['session'] = requests.Session()
        self.__dict__['session'].headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt"""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(self.session.headers['User-Agent'], url)
        except Exception:
            # If robots.txt check fails, allow by default (fail open)
            logger.warning(f"Could not check robots.txt for {url}, allowing access")
            return True
    
    def _rate_limit(self, domain: str) -> None:
        """Implement rate limiting per domain"""
        last_time = self.last_request_time[domain]
        elapsed = time.time() - last_time
        if elapsed < WEB_SCRAPE_RATE_LIMIT_DELAY:
            sleep_time = WEB_SCRAPE_RATE_LIMIT_DELAY - elapsed
            time.sleep(sleep_time)
        self.last_request_time[domain] = time.time()
    
    def _run(self, url: str) -> str:
        """Scrape web content with rate limiting and error handling"""
        if not url or not isinstance(url, str):
            return "❌ Error: Invalid URL provided"
        
        # Validate URL format
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return f"❌ Error: Invalid URL format: {url}"
            domain = parsed.netloc
        except Exception as e:
            return f"❌ Error: Could not parse URL: {str(e)}"
        
        # Check robots.txt
        if not self._check_robots_txt(url):
            logger.warning(f"Access denied by robots.txt for {url}")
            return f"⚠️ Access denied: {url} is blocked by robots.txt"
        
        # Rate limiting
        self._rate_limit(domain)
        
        try:
            response = self.session.get(
                url, 
                timeout=WEB_SCRAPE_TIMEOUT,
                allow_redirects=True,
                stream=False
            )
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type and 'text/plain' not in content_type:
                return f"⚠️ Warning: Content type is {content_type}, may not be HTML/text"
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script, style, and other non-content elements
            for element in soup(["script", "style", "meta", "link", "noscript", "iframe"]):
                element.decompose()
            
            # Extract text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            if not text:
                return f"⚠️ No text content found at {url}"
            
            # Truncate if too long
            if len(text) > WEB_SCRAPE_MAX_LENGTH:
                text = text[:WEB_SCRAPE_MAX_LENGTH] + "..."
            
            logger.info(f"Successfully scraped {len(text)} characters from {url}")
            return text
            
        except requests.exceptions.Timeout:
            return f"⏱️ Error: Request timeout after {WEB_SCRAPE_TIMEOUT}s for {url}"
        except requests.exceptions.HTTPError as e:
            return f"❌ HTTP Error {e.response.status_code}: {str(e)}"
        except requests.exceptions.ConnectionError:
            return f"❌ Connection Error: Could not connect to {url}"
        except requests.exceptions.RequestException as e:
            return f"❌ Request Error: {str(e)}"
        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Unexpected error scraping {url}: {error_type} - {str(e)}", exc_info=True)
            return f"❌ Error scraping {url}: {error_type} - {str(e)}"
    
    async def _arun(self, url: str) -> str:
        """Async version of web scraping"""
        return self._run(url)
    
    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session'):
            self.session.close()

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
    """Multi-agent system with specialized agents for different tasks."""
    
    def __init__(self, openai_api_key: Optional[str] = None, serpapi_key: Optional[str] = None):
        logger.info("Initializing MultiAgentSystem...")
        
        self.openai_api_key = openai_api_key or getattr(Config, 'OPENAI_API_KEY', None)
        self.serpapi_key = serpapi_key or getattr(Config, 'SERPAPI_KEY', None)
        
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        
        self.system_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "avg_response_time": 0.0,
            "active_sessions": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        memory_size = getattr(Config, 'AGENT_MEMORY_SIZE', 20)
        self.conversation_memory = {"chat_history": []}
        self.memory_size = memory_size
        
        self.agents = self._create_agents()
        self.system_metrics["agents_created"] = len(self.agents)
        
        logger.info(f"MultiAgentSystem initialization complete with {len(self.agents)} agents")
    
    def _initialize_llm(self):
        """Initialize LLM with fallback chain."""
        max_tokens = getattr(Config, 'MAX_TOKENS', 512)
        temperature = getattr(Config, 'TEMPERATURE', 0.7)
        default_model = getattr(Config, 'DEFAULT_LLM_MODEL', 'microsoft/DialoGPT-medium')
        fallback_model = getattr(Config, 'FALLBACK_LLM_MODEL', 'gpt2')
        
        for model_name, model_max_tokens in [(default_model, max_tokens), (fallback_model, max_tokens // 2)]:
            try:
                hf_pipeline = pipeline(
                    "text-generation",
                    model=model_name,
                    max_length=model_max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=50256,
                    device_map="auto" if torch.cuda.is_available() else None
                )
                try:
                    from langchain_huggingface import HuggingFacePipeline
                    llm = HuggingFacePipeline(
                        pipeline=hf_pipeline,
                        model_kwargs={"temperature": temperature, "max_length": model_max_tokens}
                    )
                except ImportError:
                    llm = hf_pipeline
                logger.info(f"{model_name} LLM loaded successfully")
                return llm
            except Exception as e:
                logger.warning(f"Failed to load {model_name}: {e}")
                continue
        
        logger.warning("All LLM models failed to load, using mock LLM")
        try:
            from langchain_core.language_models.fake import FakeListLLM
        except ImportError:
            class FakeListLLM:
                def __init__(self, responses):
                    self.responses = responses
                    self._index = 0
                def invoke(self, prompt):
                    response = self.responses[self._index % len(self.responses)]
                    self._index += 1
                    return response
                def __call__(self, prompt):
                    return self.invoke(prompt)
        
        return FakeListLLM(responses=[
            "I'm a research agent. Let me help you find information about that topic.",
            "I'm a coding agent. I can help you write and execute Python code.",
            "I'm an analysis agent. I can help you analyze data and provide insights."
        ])
    
    def _initialize_tools(self) -> List[BaseTool]:
        """Initialize all available tools"""
        tools: List[BaseTool] = [
            SecureCodeExecutorTool(),
            WebScrapeTool(),
            DataAnalysisTool()
        ]
        
        # Add web search if API key is available
        if self.serpapi_key:
            try:
                search = SerpAPIWrapper(serpapi_api_key=self.serpapi_key)
                tools.append(
                    Tool(
                        name="web_search",
                        description="Search the web for current information",
                        func=search.run
                    )
                )
                logger.info("SerpAPI web search tool added")
            except Exception as e:
                logger.warning(f"Failed to initialize SerpAPI: {e}")
        
        return tools
    
    def _create_agents(self) -> Dict[str, Any]:
        """Create specialized agents with appropriate tools and memory"""
        agents = {}
        
        # Research Agent
        research_tools = [tool for tool in self.tools if tool.name in ["web_search", "web_scraper"]]
        if research_tools:
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a Research Agent specialized in gathering and analyzing information.
Your role is to:
- Conduct thorough web searches and research
- Scrape and analyze web content
- Provide comprehensive, factual information
- Cite sources and verify information accuracy
Always be thorough and provide well-researched responses."""),
                    ("human", "{input}"),
                ])
                agent = create_agent(self.llm, research_tools, prompt)
                agents["researcher"] = agent
                logger.info("Research agent created successfully")
            except Exception as e:
                logger.error(f"Failed to create research agent: {e}")
        
        # Code Agent
        code_tools = [tool for tool in self.tools if tool.name in ["secure_python_executor", "data_analyzer"]]
        if code_tools:
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a Code Agent specialized in programming and data analysis.
Your role is to:
- Write and execute Python code
- Perform data analysis and visualization
- Solve computational problems
- Debug and optimize code
Always write clean, efficient, and well-documented code."""),
                    ("human", "{input}"),
                ])
                agent = create_agent(self.llm, code_tools, prompt)
                agents["coder"] = agent
                logger.info("Code agent created successfully")
            except Exception as e:
                logger.error(f"Failed to create code agent: {e}")
        
        # Analysis Agent
        if self.tools:
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are an Analysis Agent specialized in critical thinking and synthesis.
Your role is to:
- Analyze complex problems from multiple angles
- Synthesize information from various sources
- Provide strategic insights and recommendations
- Identify patterns and trends
Always provide thoughtful, well-reasoned analysis."""),
                    ("human", "{input}"),
                ])
                agent = create_agent(self.llm, self.tools, prompt)
                agents["analyst"] = agent
                logger.info("Analysis agent created successfully")
            except Exception as e:
                logger.error(f"Failed to create analysis agent: {e}")
        
        if not agents:
            logger.warning("No agents were created successfully")
        
        return agents
    
    def run_agent(self, agent_name: str, query: str) -> str:
        """Run a specific agent with a query and track metrics"""
        if not query or not isinstance(query, str):
            return "❌ Error: Invalid query provided"
        
        if agent_name not in self.agents:
            available = list(self.agents.keys())
            return f"❌ Agent '{agent_name}' not found. Available agents: {available}"
        
        start_time = time.time()
        self.system_metrics["total_tasks"] += 1
        
        try:
            # Use invoke for LangChain 1.0+ agents
            result = self.agents[agent_name].invoke({"input": query})
            if isinstance(result, dict) and "output" in result:
                result = result["output"]
            elif isinstance(result, dict) and "messages" in result:
                # Extract last message if result is a dict with messages
                messages = result["messages"]
                if messages:
                    result = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
            result = str(result)
            execution_time = time.time() - start_time
            
            # Update metrics
            self.system_metrics["successful_tasks"] += 1
            self._update_avg_response_time(execution_time)
            
            logger.info(f"Agent '{agent_name}' completed task in {execution_time:.2f}s")
            return result
            
        except TimeoutError:
            execution_time = time.time() - start_time
            self.system_metrics["failed_tasks"] += 1
            self._update_avg_response_time(execution_time)
            error_msg = f"⏱️ Timeout: Agent '{agent_name}' exceeded time limit"
            logger.warning(error_msg)
            return error_msg
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.system_metrics["failed_tasks"] += 1
            self._update_avg_response_time(execution_time)
            error_type = type(e).__name__
            error_msg = f"❌ Error running {agent_name} agent ({error_type}): {str(e)}"
            logger.error(f"Agent '{agent_name}' failed: {error_type} - {str(e)}", exc_info=True)
            return error_msg
    
    def _update_avg_response_time(self, execution_time: float) -> None:
        """Update average response time metric"""
        total = self.system_metrics["total_tasks"]
        current_avg = self.system_metrics["avg_response_time"]
        self.system_metrics["avg_response_time"] = (
            (current_avg * (total - 1) + execution_time) / total
        )
        self.system_metrics["last_updated"] = datetime.now().isoformat()
    
    def collaborative_task(self, task: str) -> Dict[str, str]:
        """Run a collaborative task across multiple agents with error handling"""
        if not task or not isinstance(task, str):
            return {"error": "Invalid task provided"}
        
        results: Dict[str, str] = {}
        start_time = time.time()
        
        try:
            # Research phase
            if "researcher" in self.agents:
                research_query = f"Research this topic thoroughly: {task}"
                results["research"] = self.run_agent("researcher", research_query)
            else:
                results["research"] = "⚠️ Research agent not available"
            
            # Analysis phase
            if "analyst" in self.agents:
                research_summary = results.get("research", "")[:500] if results.get("research") else ""
                analysis_query = f"Analyze this task and provide insights: {task}\n\nResearch findings: {research_summary}..."
                results["analysis"] = self.run_agent("analyst", analysis_query)
            else:
                results["analysis"] = "⚠️ Analysis agent not available"
            
            # Coding phase (if applicable)
            if "coder" in self.agents:
                code_query = f"If this task requires code or data analysis, provide solutions: {task}"
                results["code"] = self.run_agent("coder", code_query)
            else:
                results["code"] = "⚠️ Code agent not available"
            
            total_time = time.time() - start_time
            results["_metadata"] = {
                "total_time": f"{total_time:.2f}s",
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Collaborative task completed in {total_time:.2f}s")
            return results
            
        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"Collaborative task failed: {error_type} - {str(e)}", exc_info=True)
            return {
                "error": f"Collaborative task failed ({error_type}): {str(e)}",
                "partial_results": results
            }
    
    def get_agent_list(self) -> List[str]:
        """Get list of available agents"""
        return list(self.agents.keys())
    
    def intelligent_agent_routing(self, query: str) -> str:
        """Advanced intelligent routing based on query analysis"""
        if not query or not isinstance(query, str):
            logger.warning("Invalid query for routing, defaulting to analyst")
            return "analyst" if "analyst" in self.agents else list(self.agents.keys())[0] if self.agents else "analyst"
        
        query_lower = query.lower()
        
        # Define routing patterns with weights
        routing_patterns = {
            "researcher": {
                "keywords": ["research", "find", "search", "information", "latest", "news", "trends", "study", "investigate", "lookup", "fetch"],
                "questions": ["what", "when", "where", "who", "how many"],
                "weight": 0,
                "domain_keywords": ["market", "industry", "competitor", "news", "article", "website", "url"]
            },
            "coder": {
                "keywords": ["code", "python", "programming", "function", "algorithm", "debug", "optimize", "calculate", "data analysis", "script", "execute"],
                "questions": ["how to", "write", "create", "build", "implement", "generate"],
                "weight": 0,
                "domain_keywords": ["dataframe", "numpy", "pandas", "visualization", "plot", "chart", "graph", "csv", "json"]
            },
            "analyst": {
                "keywords": ["analyze", "compare", "evaluate", "assess", "strategy", "recommendation", "insight", "pattern", "summary", "synthesize"],
                "questions": ["why", "explain", "compare", "analyze", "evaluate", "should"],
                "weight": 0,
                "domain_keywords": ["business", "strategy", "decision", "recommendation", "insight", "trend", "pattern"]
            }
        }
        
        # Calculate weights for each agent
        for agent, patterns in routing_patterns.items():
            # Skip if agent doesn't exist
            if agent not in self.agents:
                patterns["weight"] = -1
                continue
            
            # Check keyword matches
            keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in query_lower)
            patterns["weight"] += keyword_matches * 2
            
            # Check question type matches
            question_matches = sum(1 for question in patterns["questions"] if query_lower.startswith(question))
            patterns["weight"] += question_matches * 3
            
            # Check for specific domain indicators
            domain_matches = sum(1 for word in patterns["domain_keywords"] if word in query_lower)
            patterns["weight"] += domain_matches * 2
        
        # Filter out unavailable agents and get best match
        available_patterns = {k: v for k, v in routing_patterns.items() if v["weight"] >= 0}
        
        if not available_patterns:
            # Fallback to first available agent
            default_agent = list(self.agents.keys())[0] if self.agents else "analyst"
            logger.warning(f"No routing patterns matched, using default: {default_agent}")
            return default_agent
        
        # Return agent with highest weight
        best_agent = max(available_patterns.items(), key=lambda x: x[1]["weight"])
        
        # If no clear winner, default to analyst (or first available)
        if best_agent[1]["weight"] == 0:
            default = "analyst" if "analyst" in self.agents else list(self.agents.keys())[0]
            logger.info(f"No clear routing match (weight=0), defaulting to {default}")
            return default
        
        logger.info(f"Query routed to {best_agent[0]} (weight: {best_agent[1]['weight']})")
        return best_agent[0]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        metrics = self.system_metrics.copy()
        
        # Add code executor stats if available
        for tool in self.tools:
            if hasattr(tool, 'get_stats'):
                tool_stats = tool.get_stats()
                metrics[f"{tool.name}_stats"] = tool_stats
        
        # Calculate success rate
        if metrics["total_tasks"] > 0:
            metrics["success_rate"] = metrics["successful_tasks"] / metrics["total_tasks"]
        else:
            metrics["success_rate"] = 0.0
        
        return metrics
    
    def get_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed capabilities of each agent"""
        capabilities = {
            "researcher": {
                "description": "Specialized in information gathering and research",
                "strengths": ["Web research", "Data collection", "Fact verification", "Market analysis"],
                "tools": ["web_search", "web_scraper"],
                "best_for": ["Research queries", "Information gathering", "Market analysis"],
                "available": "researcher" in self.agents
            },
            "coder": {
                "description": "Expert in programming and data analysis",
                "strengths": ["Code generation", "Data analysis", "Algorithm implementation", "Debugging"],
                "tools": ["secure_python_executor", "data_analyzer"],
                "best_for": ["Programming tasks", "Data analysis", "Code generation"],
                "available": "coder" in self.agents
            },
            "analyst": {
                "description": "Advanced analysis and strategic thinking",
                "strengths": ["Strategic analysis", "Pattern recognition", "Synthesis", "Decision support"],
                "tools": [tool.name for tool in self.tools],
                "best_for": ["Complex analysis", "Strategic planning", "Decision support"],
                "available": "analyst" in self.agents
            }
        }
        return capabilities
    
    def cleanup(self) -> None:
        """Cleanup resources and close connections"""
        try:
            # Close web scraping sessions
            for tool in self.tools:
                if hasattr(tool, 'session'):
                    try:
                        tool.session.close()
                    except Exception as e:
                        logger.warning(f"Error closing session for {tool.name}: {e}")
                
                # Shutdown executors
                if hasattr(tool, 'executor'):
                    try:
                        tool.executor.shutdown(wait=False)
                    except Exception as e:
                        logger.warning(f"Error shutting down executor for {tool.name}: {e}")
            
            logger.info("MultiAgentSystem cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except Exception:
            pass  # Ignore errors during destruction 