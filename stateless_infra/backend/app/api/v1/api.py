from fastapi import APIRouter
from app.api.v1.endpoints import bots, ios, affiliate, admin

api_router = APIRouter()
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(ios.router, prefix="/ios", tags=["ios"])
api_router.include_router(affiliate.router, prefix="/affiliate", tags=["affiliate"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
