import hashlib
import hmac
from datetime import datetime, timezone
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AffiliateService:
    """
    Stateless affiliate code service.
    
    Codes are generated using HMAC-SHA256 and can be verified without storing state.
    The design uses a persistent `code_id` (e.g., email hash, user ID, device ID)
    instead of ephemeral session IDs to enable verification across sessions.
    """
    
    def generate_code(self, app_id: str, code_id: str) -> str:
        """
        Generate a stateless referral code using HMAC.
        
        Args:
            app_id: The tenant identifier
            code_id: A persistent identifier (email hash, user ID, device ID)
                    This should persist across sessions for verification to work.
        
        Returns:
            8-character uppercase affiliate code
        """
        salt = settings.AFFILIATE_SALT
        message = f"{app_id}:{code_id}".encode()
        key = salt.encode()
        
        # Use HMAC for secure code generation
        signature = hmac.new(key, message, hashlib.sha256).hexdigest()
        code = signature[:8].upper()
        
        logger.debug(f"Generated affiliate code for tenant {app_id}")
        return code
    
    def verify_code(self, code: str, app_id: str, code_id: str) -> bool:
        """
        Verify if a code is valid for the given app_id and code_id.
        
        Args:
            code: The affiliate code to verify
            app_id: The tenant identifier
            code_id: The persistent identifier used during generation
            
        Returns:
            True if code is valid, False otherwise
        """
        expected_code = self.generate_code(app_id, code_id)
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(code.upper(), expected_code)
    
    def verify_code_for_tenant(self, code: str, app_id: str) -> bool:
        """
        Verify that a code format is valid for a tenant (basic validation).
        
        This is a fallback for when code_id is not available.
        Only checks format, not cryptographic validity.
        
        Args:
            code: The affiliate code to verify
            app_id: The tenant identifier
            
        Returns:
            True if format is valid (8 hex chars)
        """
        if not code or len(code) != 8:
            return False
        try:
            int(code, 16)  # Check if valid hex
            return True
        except ValueError:
            return False

    def record_conversion(self, code: str, conversion_data: dict):
        """
        Record anonymized conversion metrics.
        In production, write to timeseries DB or analytics (PostHog, Mixpanel).
        """
        logger.info(
            f"Conversion recorded - code: {code}, "
            f"value: {conversion_data.get('value')}, "
            f"currency: {conversion_data.get('currency')}, "
            f"tenant: {conversion_data.get('tenant', 'unknown')}"
        )
        return True
