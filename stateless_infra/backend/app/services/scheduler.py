from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.cleanup import cleanup_expired_data
from app.db.session import AsyncSessionLocal
from datetime import datetime, timezone
from typing import Optional
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# Scheduler health state (module-level for observability)
_scheduler_state = {
    "last_run_time": None,
    "last_run_status": None,
    "run_count": 0,
    "error_count": 0,
    "started_at": None
}


def get_scheduler_health() -> dict:
    """
    Get scheduler health information.
    
    Returns:
        Dict with last run time, status, counts, and scheduler state
    """
    return {
        "is_running": scheduler.running,
        "last_run_time": _scheduler_state["last_run_time"].isoformat() if _scheduler_state["last_run_time"] else None,
        "last_run_status": _scheduler_state["last_run_status"],
        "run_count": _scheduler_state["run_count"],
        "error_count": _scheduler_state["error_count"],
        "started_at": _scheduler_state["started_at"].isoformat() if _scheduler_state["started_at"] else None,
        "next_run": None  # Will be populated if scheduler is running
    }


async def scheduled_cleanup():
    """
    Run cleanup task every hour.
    
    Note: In a horizontally scaled environment, only ONE instance should run
    the scheduler to avoid duplicate cleanups. Use distributed locking or
    ensure scheduler runs on a dedicated worker instance.
    """
    _scheduler_state["run_count"] += 1
    run_time = datetime.now(timezone.utc)
    
    try:
        async with AsyncSessionLocal() as db:
            await cleanup_expired_data(db)
            
        _scheduler_state["last_run_time"] = run_time
        _scheduler_state["last_run_status"] = "success"
        logger.info("Scheduled cleanup completed successfully")
        
    except Exception as e:
        _scheduler_state["last_run_time"] = run_time
        _scheduler_state["last_run_status"] = "error"
        _scheduler_state["error_count"] += 1
        logger.error(f"Scheduled cleanup failed: {e}", exc_info=True)
        # Don't re-raise - let scheduler continue running


def start_scheduler():
    """Initialize and start the background scheduler."""
    _scheduler_state["started_at"] = datetime.now(timezone.utc)
    
    # Run cleanup every 60 minutes (hourly)
    scheduler.add_job(
        scheduled_cleanup, 
        'interval', 
        minutes=60, 
        id='cleanup_job',
        max_instances=1  # Prevent concurrent runs
    )
    scheduler.start()
    logger.info("Background scheduler started: cleanup runs every 60 minutes")


def shutdown_scheduler():
    """Gracefully shutdown the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=True)
        logger.info("Background scheduler stopped")
