from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from app.services.bot import BotRuntime, BotTimeoutError
from app.core.limiter import limiter
from app.core.validators import validate_task_type, validate_context_size
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
bot_runtime = BotRuntime()

# Allowed bot task types (allowlist)
ALLOWED_TASK_TYPES = [
    "email_campaign",
    "social_post",
    "data_export",
    "report_generation"
]


class BotRequest(BaseModel):
    task_type: str
    context: dict


@router.post("/execute")
@limiter.limit("30/minute")
async def execute_bot(request: Request, payload: BotRequest):
    """
    Execute a bot task.
    
    Tasks have a 30-second timeout. Long-running tasks will return 504.
    """
    app_id = request.state.app_id
    
    # Validate task type against allowlist
    try:
        validate_task_type(payload.task_type, ALLOWED_TASK_TYPES)
        validate_context_size(payload.context)
    except Exception as e:
        logger.warning(f"Bot request validation failed for tenant {app_id}: {e}")
        raise
    
    logger.info(f"Executing bot task '{payload.task_type}' for tenant {app_id}")
    
    try:
        # Execute bot task with timeout protection
        result = await bot_runtime.execute_task(payload.task_type, payload.context)
        
        return {
            "status": "success", 
            "result": result, 
            "tenant": app_id,
            "ephemeral": True
        }
    except BotTimeoutError as e:
        logger.error(f"Bot timeout for tenant {app_id}: {e}")
        raise HTTPException(
            status_code=504,
            detail="Bot task timed out. Try a smaller request or retry later."
        )
