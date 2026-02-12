from fastapi import FastAPI, Request
from app.core.config import settings
from app.core.middleware import TenantMiddleware
from app.core.size_limit import RequestSizeLimitMiddleware
from app.api.v1.api import api_router
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware (order matters: size limit first, then tenant)
app.add_middleware(TenantMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routers
app.include_router(api_router, prefix="/api/v1")

# Lifecycle Events
@app.on_event("startup")
async def startup_event():
    # Validate production secrets before starting
    settings.validate_production_secrets()
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()

@app.get("/health")
@limiter.limit("10/minute")
def health_check(request: Request):
    return {"status": "ok", "env": settings.ENVIRONMENT}

@app.get("/")
def root(request: Request):
    return {
        "message": "Stateless Infra API Running",
        "tenant": getattr(request.state, "app_id", "unknown")
    }
