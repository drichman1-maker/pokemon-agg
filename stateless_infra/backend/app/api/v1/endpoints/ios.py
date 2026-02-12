from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class APNsToken(BaseModel):
    token: str
    device_id: str

@router.post("/register-token")
async def register_token(request: Request, payload: APNsToken):
    """
    STUB: Register APNs token.
    
    Currently returns a placeholder response. In production, this would
    store the token in Redis/DB with a short TTL.
    """
    app_id = request.state.app_id
    logger.warning(f"STUB: iOS token registration called for tenant {app_id}")
    
    return {
        "status": "received", 
        "tenant": app_id,
        "action": "cached_temporarily",
        "stub": True
    }

class ReceiptValidation(BaseModel):
    receipt_data: str

@router.post("/validate-receipt")
async def validate_receipt(request: Request, payload: ReceiptValidation):
    """
    STUB: Validate App Store receipt.
    
    Currently returns 'valid' for everything. In production, this MUST
    verify against Apple's API.
    """
    app_id = request.state.app_id
    logger.warning(f"STUB: iOS receipt validation called for tenant {app_id}")
    
    return {
        "status": "valid", 
        "is_active": True,
        "tenant": app_id,
        "stub": True
    }
