import asyncio
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class BotTimeoutError(Exception):
    """Raised when bot execution exceeds timeout."""
    pass


class BotRuntime:
    """
    Bot execution runtime with timeout protection.
    
    All bot tasks are wrapped with a timeout to prevent worker exhaustion.
    Default timeout is 30 seconds, configurable via BOT_TIMEOUT_SECONDS.
    """
    
    def __init__(self, timeout_seconds: Optional[int] = None):
        self.timeout = timeout_seconds or getattr(settings, 'BOT_TIMEOUT_SECONDS', 30)
    
    async def execute_task(self, task_type: str, context: dict) -> str:
        """
        Execute a bot task with timeout protection.
        
        Args:
            task_type: Type of task to execute
            context: Task context/parameters
            
        Returns:
            Task execution result
            
        Raises:
            BotTimeoutError: If task exceeds timeout
        """
        try:
            result = await asyncio.wait_for(
                self._do_execute(task_type, context),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.error(
                f"Bot task '{task_type}' timed out after {self.timeout}s. "
                f"Context keys: {list(context.keys())}"
            )
            raise BotTimeoutError(
                f"Task '{task_type}' exceeded {self.timeout}s timeout"
            )
    
    async def _do_execute(self, task_type: str, context: dict) -> str:
        """
        Actual task execution logic.
        
        In production, this would call the Clawi API or load local agents.
        Currently a mock that simulates work.
        """
        # Simulate varying execution times based on task type
        delays = {
            "email_campaign": 2,
            "social_post": 1,
            "data_export": 5,
            "report_generation": 3
        }
        delay = delays.get(task_type, 1)
        
        await asyncio.sleep(delay)
        
        logger.info(f"Bot task '{task_type}' completed in ~{delay}s")
        return f"Executed {task_type} for context keys: {list(context.keys())}"
