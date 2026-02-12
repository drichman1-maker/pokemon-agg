from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Draft, BotOutput
from sqlalchemy.sql import func
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

async def cleanup_expired_data(db: AsyncSession):
    """
    Hard delete expired rows to enforce statelessness.
    
    Uses timezone-aware timestamps to ensure consistent cleanup
    regardless of database server timezone.
    """
    # Use timezone-aware current time (UTC)
    now = datetime.now(timezone.utc)
    
    try:
        # 1. Delete Drafts
        result_drafts = await db.execute(
            delete(Draft).where(Draft.expires_at < now)
        )
        deleted_drafts = result_drafts.rowcount
        
        # 2. Delete Bot Outputs
        result_outputs = await db.execute(
            delete(BotOutput).where(BotOutput.expires_at < now)
        )
        deleted_outputs = result_outputs.rowcount
        
        await db.commit()
        
        if deleted_drafts > 0 or deleted_outputs > 0:
            logger.info(f"Cleanup: Deleted {deleted_drafts} drafts and {deleted_outputs} bot outputs.")
        else:
            logger.debug("Cleanup: No expired data found")
            
    except Exception as e:
        logger.error(f"Cleanup failed, rolling back transaction: {e}", exc_info=True)
        await db.rollback()
        raise
