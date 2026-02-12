from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db.session import AsyncSessionLocal
from app.services.cleanup import cleanup_expired_data
import logging

logger = logging.getLogger(__name__)

class CleanupScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    async def cleanup_job(self):
        """Scheduled job to clean up expired data."""
        logger.info("Running scheduled cleanup job...")
        async with AsyncSessionLocal() as session:
            try:
                await cleanup_expired_data(session)
                logger.info("Cleanup job completed successfully")
            except Exception as e:
                logger.error(f"Cleanup job failed: {e}")
    
    def start(self):
        """Start the scheduler with hourly cleanup."""
        # Run cleanup every hour at minute 0
        self.scheduler.add_job(
            self.cleanup_job,
            CronTrigger(minute=0),
            id='cleanup_expired_data',
            name='Cleanup expired data',
            replace_existing=True
        )
        self.scheduler.start()
        logger.info("Cleanup scheduler started - running every hour")
    
    def shutdown(self):
        """Gracefully shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Cleanup scheduler stopped")

# Global scheduler instance
scheduler = CleanupScheduler()
