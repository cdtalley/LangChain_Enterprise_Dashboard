"""LangChain callbacks for tracking execution, tokens, and performance."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
import logging

logger = logging.getLogger(__name__)


class TokenTrackingCallback(BaseCallbackHandler):
    """Track token usage, latency, and chain execution."""
    
    def __init__(self):
        super().__init__()
        self.token_usage = {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        }
        self.execution_trace = []
        self.chain_steps = []
        self.start_time = None
        self.end_time = None
        self.latencies = []
        
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Track LLM invocation start."""
        self.start_time = datetime.now()
        step = {
            'type': 'llm_start',
            'timestamp': self.start_time.isoformat(),
            'prompt_count': len(prompts),
            'prompt_preview': prompts[0][:100] if prompts else ''
        }
        self.execution_trace.append(step)
        self.chain_steps.append({
            'step': 'LLM Invocation',
            'status': 'started',
            'timestamp': self.start_time.isoformat()
        })
        
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Track LLM completion and token usage."""
        self.end_time = datetime.now()
        latency = (self.end_time - self.start_time).total_seconds() if self.start_time else 0
        self.latencies.append(latency)
        
        if response.llm_output and 'token_usage' in response.llm_output:
            usage = response.llm_output['token_usage']
            self.token_usage['prompt_tokens'] += usage.get('prompt_tokens', 0)
            self.token_usage['completion_tokens'] += usage.get('completion_tokens', 0)
            self.token_usage['total_tokens'] += usage.get('total_tokens', 0)
        
        step = {
            'type': 'llm_end',
            'timestamp': self.end_time.isoformat(),
            'latency_seconds': latency,
            'generation_count': len(response.generations) if response.generations else 0
        }
        self.execution_trace.append(step)
        
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'completed'
            self.chain_steps[-1]['latency_seconds'] = latency
            self.chain_steps[-1]['token_usage'] = self.token_usage.copy()
            
    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Track LLM errors."""
        step = {
            'type': 'llm_error',
            'timestamp': datetime.now().isoformat(),
            'error': str(error)
        }
        self.execution_trace.append(step)
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'error'
            self.chain_steps[-1]['error'] = str(error)
            
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Track chain execution start."""
        chain_name = serialized.get('name', 'unknown')
        step = {
            'type': 'chain_start',
            'timestamp': datetime.now().isoformat(),
            'chain_name': chain_name,
            'inputs_keys': list(inputs.keys()) if isinstance(inputs, dict) else []
        }
        self.execution_trace.append(step)
        self.chain_steps.append({
            'step': f'Chain: {chain_name}',
            'status': 'started',
            'timestamp': datetime.now().isoformat()
        })
        
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Track chain completion."""
        step = {
            'type': 'chain_end',
            'timestamp': datetime.now().isoformat(),
            'outputs_keys': list(outputs.keys()) if isinstance(outputs, dict) else []
        }
        self.execution_trace.append(step)
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'completed'
            
    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Track chain errors."""
        step = {
            'type': 'chain_error',
            'timestamp': datetime.now().isoformat(),
            'error': str(error)
        }
        self.execution_trace.append(step)
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'error'
            self.chain_steps[-1]['error'] = str(error)
            
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Track tool invocation."""
        tool_name = serialized.get('name', 'unknown')
        step = {
            'type': 'tool_start',
            'timestamp': datetime.now().isoformat(),
            'tool_name': tool_name,
            'input_preview': input_str[:100] if input_str else ''
        }
        self.execution_trace.append(step)
        self.chain_steps.append({
            'step': f'Tool: {tool_name}',
            'status': 'started',
            'timestamp': datetime.now().isoformat()
        })
        
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Track tool completion."""
        step = {
            'type': 'tool_end',
            'timestamp': datetime.now().isoformat(),
            'output_preview': output[:100] if output else ''
        }
        self.execution_trace.append(step)
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'completed'
            
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Track tool errors."""
        step = {
            'type': 'tool_error',
            'timestamp': datetime.now().isoformat(),
            'error': str(error)
        }
        self.execution_trace.append(step)
        if self.chain_steps:
            self.chain_steps[-1]['status'] = 'error'
            self.chain_steps[-1]['error'] = str(error)
            
    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics."""
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            'token_usage': self.token_usage.copy(),
            'total_latency_seconds': sum(self.latencies),
            'avg_latency_seconds': avg_latency,
            'step_count': len(self.chain_steps),
            'execution_trace': self.execution_trace.copy(),
            'chain_steps': self.chain_steps.copy()
        }
        
    def reset(self):
        """Reset tracking state."""
        self.token_usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        self.execution_trace = []
        self.chain_steps = []
        self.start_time = None
        self.end_time = None
        self.latencies = []


class AgentReasoningCallback(BaseCallbackHandler):
    """Track agent reasoning steps and decision-making process."""
    
    def __init__(self):
        super().__init__()
        self.reasoning_steps = []
        self.agent_actions = []
        self.observations = []
        
    def on_agent_action(self, action, **kwargs: Any) -> None:
        """Track agent actions and tool selections."""
        step = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action.tool if hasattr(action, 'tool') else 'unknown',
            'tool_input': action.tool_input if hasattr(action, 'tool_input') else {},
            'log': action.log if hasattr(action, 'log') else ''
        }
        self.agent_actions.append(step)
        self.reasoning_steps.append({
            'step': len(self.reasoning_steps) + 1,
            'type': 'action',
            'content': step
        })
        
    def on_agent_finish(self, finish, **kwargs: Any) -> None:
        """Track agent completion."""
        step = {
            'timestamp': datetime.now().isoformat(),
            'return_values': finish.return_values if hasattr(finish, 'return_values') else {},
            'log': finish.log if hasattr(finish, 'log') else ''
        }
        self.reasoning_steps.append({
            'step': len(self.reasoning_steps) + 1,
            'type': 'finish',
            'content': step
        })
        
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Track tool observations."""
        observation = {
            'timestamp': datetime.now().isoformat(),
            'output_preview': output[:200] if output else '',
            'output_length': len(output) if output else 0
        }
        self.observations.append(observation)
        self.reasoning_steps.append({
            'step': len(self.reasoning_steps) + 1,
            'type': 'observation',
            'content': observation
        })
        
    def get_reasoning_trace(self) -> List[Dict[str, Any]]:
        """Get complete reasoning trace."""
        return self.reasoning_steps.copy()
        
    def reset(self):
        """Reset reasoning state."""
        self.reasoning_steps = []
        self.agent_actions = []
        self.observations = []

