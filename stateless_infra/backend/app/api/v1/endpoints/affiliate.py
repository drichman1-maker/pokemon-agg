from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.affiliate import AffiliateService
from app.core.validators import validate_session_id
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
affiliate_service = AffiliateService()


class AffiliateGenerateRequest(BaseModel):
    """Request to generate an affiliate code."""
    code_id: str = Field(
        ...,
        description="Persistent identifier for code verification. "
                    "Use email hash, user ID, or device ID - NOT session ID.",
        min_length=1,
        max_length=128
    )


class AffiliateConversionRequest(BaseModel):
    """Request to record an affiliate conversion."""
    code: str = Field(..., min_length=8, max_length=8)
    code_id: str = Field(
        ...,
        description="Same persistent identifier used during code generation.",
        min_length=1,
        max_length=128
    )
    value: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)


@router.post("/generate")
async def generate_code(request: Request, payload: AffiliateGenerateRequest):
    """
    Generate an affiliate referral code.
    
    The `code_id` should be a persistent identifier that survives session changes:
    - Hash of user email
    - Device ID
    - User account ID
    
    Do NOT use session IDs as they are ephemeral.
    """
    app_id = request.state.app_id
    
    code = affiliate_service.generate_code(app_id, payload.code_id)
    logger.info(f"Generated affiliate code for tenant {app_id}")
    
    return {
        "code": code,
        "tenant": app_id,
        "note": "Store code_id for conversion verification"
    }


@router.post("/conversion")
async def track_conversion(request: Request, payload: AffiliateConversionRequest):
    """
    Record an affiliate conversion.
    
    The `code_id` must match what was used during code generation.
    """
    app_id = request.state.app_id
    
    # Verify code matches the code_id for this tenant
    if not affiliate_service.verify_code(payload.code, app_id, payload.code_id):
        logger.warning(f"Invalid affiliate code rejected for tenant {app_id}")
        raise HTTPException(status_code=400, detail="Invalid affiliate code")
    
    conversion_data = {
        "code": payload.code,
        "value": payload.value,
        "currency": payload.currency,
        "tenant": app_id
    }
    
    affiliate_service.record_conversion(payload.code, conversion_data)
    return {"status": "recorded", "tenant": app_id}


# Backward compatibility: Accept session_id but warn
class LegacyAffiliateRequest(BaseModel):
    session_id: str


@router.post("/generate-legacy", deprecated=True)
async def generate_code_legacy(request: Request, payload: LegacyAffiliateRequest):
    """
    [DEPRECATED] Generate code using session_id.
    
    Use /generate with code_id instead for reliable verification.
    """
    app_id = request.state.app_id
    
    logger.warning(f"Deprecated /generate-legacy called by tenant {app_id}")
    
    # Validate session ID
    try:
        validate_session_id(payload.session_id)
    except HTTPException:
        logger.warning(f"Invalid session ID for tenant {app_id}")
        raise
    
    code = affiliate_service.generate_code(app_id, payload.session_id)
    
    return {
        "code": code,
        "tenant": app_id,
        "warning": "This endpoint is deprecated. Use /generate with code_id instead."
    }
