from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_tenant_id(request: Request) -> str:
    """Extract tenant ID from request state for rate limiting."""
    return getattr(request.state, "app_id", get_remote_address(request))

# Configure storage (Redis if available, else Memory)
storage_uri = "memory://"
if settings.REDIS_URL:
    storage_uri = settings.REDIS_URL
    logger.info("Rate limiter using Redis storage")
else:
    logger.warning("Rate limiter using IN-MEMORY storage (limits reset on restart)")

limiter = Limiter(key_func=get_tenant_id, storage_uri=storage_uri)
