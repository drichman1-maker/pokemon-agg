"""
Request body size limit middleware.

This middleware rejects requests with bodies larger than the configured limit
BEFORE FastAPI/Pydantic parses them, preventing memory exhaustion attacks.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to limit request body size before parsing.
    
    Checks Content-Length header and rejects oversized requests with 413.
    This happens BEFORE the body is read, preventing memory exhaustion.
    """
    
    def __init__(self, app, max_size: int = None):
        super().__init__(app)
        self.max_size = max_size or settings.MAX_REQUEST_BODY_BYTES
    
    async def dispatch(self, request: Request, call_next):
        # Check Content-Length header
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                size = int(content_length)
                if size > self.max_size:
                    logger.warning(
                        f"Request rejected: body size {size} bytes exceeds "
                        f"limit of {self.max_size} bytes. "
                        f"Path: {request.url.path}"
                    )
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": "Request body too large",
                            "max_size_bytes": self.max_size,
                            "received_bytes": size
                        }
                    )
            except ValueError:
                # Invalid Content-Length header
                pass
        
        return await call_next(request)
