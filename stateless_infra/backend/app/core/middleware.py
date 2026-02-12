from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.validators import validate_tenant_id
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health checks and docs without app_id
        if request.url.path in ["/health", "/docs", "/openapi.json", "/"]:
            return await call_next(request)
            
        app_id = request.headers.get("X-App-ID")
        if not app_id:
            return JSONResponse(
                status_code=400, 
                content={"error": "Missing X-App-ID header"}
            )
        
        # Validate tenant ID format to prevent injection attacks
        try:
            validated_app_id = validate_tenant_id(app_id)
            request.state.app_id = validated_app_id
        except HTTPException as e:
            logger.warning(f"Invalid tenant ID rejected: {app_id[:20]}...")
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
        
        response = await call_next(request)
        return response
