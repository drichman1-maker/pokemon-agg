from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.cleanup import cleanup_expired_data
from app.services.scheduler import get_scheduler_health
from app.db.models import Draft, BotOutput
from sqlalchemy import select, func
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/cleanup")
async def trigger_cleanup(request: Request, db: AsyncSession = Depends(get_db)):
    """Manually trigger cleanup of expired data."""
    app_id = request.state.app_id
    logger.info(f"Manual cleanup triggered by tenant: {app_id}")
    
    try:
        await cleanup_expired_data(db)
        return {
            "status": "success",
            "message": "Cleanup completed",
            "tenant": app_id
        }
    except Exception as e:
        # Log detailed error server-side
        logger.error(f"Manual cleanup failed for tenant {app_id}: {e}", exc_info=True)
        # Return generic error to client
        return {
            "status": "error",
            "message": "Cleanup operation failed",
            "tenant": app_id
        }


@router.get("/stats")
async def get_tenant_stats(request: Request, db: AsyncSession = Depends(get_db)):
    """Get aggregate statistics for the requesting tenant."""
    app_id = request.state.app_id
    
    try:
        # Count drafts for this tenant
        draft_count = await db.scalar(
            select(func.count(Draft.id)).where(Draft.tenant_id == app_id)
        )
        
        # Count bot outputs for this tenant
        bot_output_count = await db.scalar(
            select(func.count(BotOutput.id)).where(BotOutput.tenant_id == app_id)
        )
        
        return {
            "tenant": app_id,
            "stats": {
                "active_drafts": draft_count or 0,
                "active_bot_outputs": bot_output_count or 0
            }
        }
    except Exception as e:
        logger.error(f"Stats query failed for tenant {app_id}: {e}", exc_info=True)
        return {"error": "Failed to retrieve statistics"}


@router.get("/health-detailed")
async def detailed_health(request: Request, db: AsyncSession = Depends(get_db)):
    """Detailed health check including database connectivity."""
    try:
        # Test database connection
        await db.execute(select(1))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "tenant": getattr(request.state, "app_id", "unknown")
    }


@router.get("/scheduler-health")
async def scheduler_health(request: Request):
    """
    Get scheduler health information.
    
    Returns last run time, status, run count, and error count.
    Use this endpoint to detect if cleanup has stopped running.
    """
    health = get_scheduler_health()
    
    # Determine overall status
    status = "ok"
    if not health["is_running"]:
        status = "stopped"
    elif health["last_run_status"] == "error":
        status = "degraded"
    elif health["error_count"] > health["run_count"] * 0.1:  # >10% errors
        status = "warning"
    
    return {
        "status": status,
        "scheduler": health,
        "tenant": getattr(request.state, "app_id", "unknown")
    }
