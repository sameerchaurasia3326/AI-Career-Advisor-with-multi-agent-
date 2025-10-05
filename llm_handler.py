# Robust LLM Handler with Retry + Fallback Switching
# Handles errors gracefully across multiple API providers

import time
import logging
from typing import List, Dict, Any, Optional
from crewai import LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustLLMHandler:
    """
    Handles LLM calls with retry mechanism and fallback switching
    across multiple API providers for maximum reliability
    """
    
    def __init__(self):
        self.max_retries = 3
        self.base_delay = 2  # seconds
        self.max_delay = 30  # seconds
        
        # Initialize all available LLMs with fallback priority
        self.llm_providers = self._initialize_llm_providers()
        
    def _initialize_llm_providers(self) -> Dict[str, List[LLM]]:
        """Initialize all LLM providers with fallback chains"""
        
        # Primary LLMs for each agent type
        gemini_primary = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.7,
        )
        
        gemini_secondary = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.5,
        )
        
        perplexity_llm = LLM(
            model="sonar-reasoning-pro",
            base_url="https://api.perplexity.ai/",
            api_key=os.getenv("PERPLEXITY_API_KEY")
        )
        
        openrouter_claude_1 = LLM(
            model="openrouter/deepseek/deepseek-r1",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=0.7,
        )
        
        openrouter_claude_2 = LLM(
            model="openrouter/deepseek/deepseek-r1",
            base_url="https://openrouter.ai/api/v1", 
            api_key=os.getenv("OPENROUTER_API_KEY_1"),
            temperature=0.5,
        )
        
        # Define fallback chains for different agent types
        return {
            "profile_analysis": [gemini_primary, openrouter_claude_1, perplexity_llm],
            "career_exploration": [perplexity_llm, openrouter_claude_1, gemini_primary],
            "skill_development": [openrouter_claude_1, gemini_secondary, perplexity_llm],
            "market_analysis": [perplexity_llm, openrouter_claude_2, gemini_primary],
            "roadmap_strategy": [gemini_secondary, openrouter_claude_1, perplexity_llm],
            "learning_resources": [openrouter_claude_2, perplexity_llm, gemini_primary],
            "report_generation": [gemini_primary, openrouter_claude_1, gemini_secondary]
        }
    
    def execute_with_fallback(self, agent_type: str, agent_function, *args, **kwargs) -> Any:
        """
        Execute agent function with retry + fallback mechanism
        
        Args:
            agent_type: Type of agent (e.g., 'profile_analysis')
            agent_function: The agent execution function
            *args, **kwargs: Arguments to pass to the agent function
            
        Returns:
            Result from successful LLM call
            
        Raises:
            Exception: If all fallback options fail
        """
        fallback_chain = self.llm_providers.get(agent_type, [])
        
        if not fallback_chain:
            logger.error(f"No fallback chain defined for agent type: {agent_type}")
            raise ValueError(f"No LLM providers configured for {agent_type}")
        
        last_exception = None
        
        # Try each LLM in the fallback chain
        for llm_index, llm in enumerate(fallback_chain):
            llm_name = self._get_llm_name(llm)
            logger.info(f"Trying {agent_type} with {llm_name} (option {llm_index + 1}/{len(fallback_chain)})")
            
            # Try this LLM with retry mechanism
            try:
                result = self._execute_with_retry(llm, agent_function, *args, **kwargs)
                logger.info(f"✅ {agent_type} succeeded with {llm_name}")
                return result
                
            except Exception as e:
                last_exception = e
                logger.warning(f"❌ {agent_type} failed with {llm_name}: {str(e)}")
                
                # If this wasn't the last option, continue to next LLM
                if llm_index < len(fallback_chain) - 1:
                    logger.info(f"🔄 Falling back to next LLM provider...")
                    continue
        
        # All fallback options failed
        logger.error(f"🚨 All LLM providers failed for {agent_type}")
        raise Exception(f"All LLM providers failed for {agent_type}. Last error: {str(last_exception)}")
    
    def _execute_with_retry(self, llm: LLM, agent_function, *args, **kwargs) -> Any:
        """Execute with exponential backoff retry mechanism"""
        
        # Update the agent's LLM before execution
        if hasattr(agent_function, '__self__'):  # If it's a bound method
            agent_function.__self__.llm = llm
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Execute the agent function
                result = agent_function(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"✅ Succeeded on retry attempt {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if this is a retryable error
                if not self._is_retryable_error(e):
                    logger.info(f"Non-retryable error, switching to next LLM: {str(e)}")
                    raise e
                
                # If this is the last attempt, don't wait
                if attempt == self.max_retries - 1:
                    logger.warning(f"Max retries ({self.max_retries}) reached")
                    raise e
                
                # Calculate delay with exponential backoff
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.info(f"Retry {attempt + 1}/{self.max_retries} after {delay}s delay...")
                time.sleep(delay)
        
        # This should never be reached due to the raise in the loop
        raise last_exception
    
    def _is_retryable_error(self, error: Exception) -> bool:
        """Determine if an error is worth retrying"""
        error_str = str(error).lower()
        
        # Non-retryable errors (should switch to fallback LLM immediately)
        non_retryable_indicators = [
            "402",  # Payment Required - Credits exhausted
            "401",  # Unauthorized - Invalid API key
            "403",  # Forbidden - Access denied
            "credits",  # OpenRouter credits exhausted
            "afford",   # OpenRouter can't afford tokens
            "upgrade to a paid account",  # OpenRouter payment required
        ]
        
        # If it's a non-retryable error, don't retry - switch LLM immediately
        if any(indicator in error_str for indicator in non_retryable_indicators):
            return False
        
        # Retryable errors (temporary issues)
        retryable_indicators = [
            "503",  # Service Unavailable
            "502",  # Bad Gateway  
            "504",  # Gateway Timeout
            "429",  # Too Many Requests
            "overloaded",
            "timeout",
            "temporarily unavailable",
            "rate limit",
            "internal server error"
        ]
        
        return any(indicator in error_str for indicator in retryable_indicators)
    
    def _get_llm_name(self, llm: LLM) -> str:
        """Get friendly name for LLM for logging"""
        model = getattr(llm, 'model', 'Unknown')
        if 'gemini' in model:
            return "Gemini"
        elif 'sonar' in model:
            return "Perplexity"
        elif 'openrouter' in model:
            return "OpenRouter"
        else:
            return f"LLM({model})"

# Global instance
llm_handler = RobustLLMHandler()
