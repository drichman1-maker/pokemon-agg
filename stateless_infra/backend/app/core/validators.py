import re
from typing import Optional
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

# Tenant ID validation
TENANT_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')

# Maximum payload sizes (in bytes)
MAX_CONTEXT_SIZE = 1024 * 1024  # 1MB
MAX_REQUEST_BODY = 10 * 1024 * 1024  # 10MB


def validate_tenant_id(tenant_id: str) -> str:
    """
    Validate tenant ID format to prevent injection attacks.
    
    Args:
        tenant_id: The tenant identifier from X-App-ID header
        
    Returns:
        The validated tenant_id
        
    Raises:
        HTTPException: If tenant_id is invalid
    """
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID cannot be empty")
    
    if len(tenant_id) > 64:
        raise HTTPException(status_code=400, detail="Tenant ID too long (max 64 characters)")
    
    if not TENANT_ID_PATTERN.match(tenant_id):
        raise HTTPException(
            status_code=400, 
            detail="Invalid tenant ID format. Only alphanumeric, underscore, and hyphen allowed"
        )
    
    return tenant_id


def validate_session_id(session_id: str) -> str:
    """Validate session ID format."""
    if not session_id or len(session_id) > 128:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    return session_id


def validate_task_type(task_type: str, allowed_types: Optional[list] = None) -> str:
    """
    Validate bot task type against allowlist.
    
    Args:
        task_type: The requested task type
        allowed_types: Optional list of allowed task types
        
    Returns:
        The validated task_type
    """
    if not task_type or len(task_type) > 64:
        raise HTTPException(status_code=400, detail="Invalid task type")
    
    if allowed_types and task_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Task type not allowed. Allowed types: {', '.join(allowed_types)}"
        )
    
    return task_type


def validate_context_size(context: dict) -> dict:
    """
    Validate that context payload is not too large.
    
    Args:
        context: The context dictionary
        
    Returns:
        The validated context
        
    Raises:
        HTTPException: If context is too large
    """
    import json
    
    # Estimate size by serializing to JSON
    try:
        context_json = json.dumps(context)
        size = len(context_json.encode('utf-8'))
        
        if size > MAX_CONTEXT_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Context payload too large (max {MAX_CONTEXT_SIZE} bytes)"
            )
    except (TypeError, ValueError) as e:
        raise HTTPException(status_code=400, detail="Invalid context format")
    
    return context


def validate_email(email: str) -> str:
    """Basic email validation."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    if not email or len(email) > 254:
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    if not email_pattern.match(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    return email


def sanitize_error_message(error: Exception, include_details: bool = False) -> str:
    """
    Sanitize error messages to prevent information leakage.
    
    Args:
        error: The exception that occurred
        include_details: Whether to include detailed error info (for logging)
        
    Returns:
        Sanitized error message
    """
    if include_details:
        return str(error)
    
    # Generic error messages for different exception types
    error_type = type(error).__name__
    
    generic_messages = {
        'DatabaseError': 'Database operation failed',
        'IntegrityError': 'Data integrity constraint violated',
        'OperationalError': 'Database connection error',
        'TimeoutError': 'Operation timed out',
        'ConnectionError': 'External service unavailable',
    }
    
    return generic_messages.get(error_type, 'An internal error occurred')


def validate_expires_at(timestamp: datetime, max_days: int = 7) -> datetime:
    """
    Validate that an expiration timestamp is reasonable.
    
    Args:
        timestamp: The timestamp to validate
        max_days: Maximum allowed days in the future (default 7)
        
    Returns:
        The validated timestamp
        
    Raises:
        HTTPException: If timestamp is in the past or too far in the future
    """
    # Ensure timestamp is timezone-aware (UTC)
    if timestamp.tzinfo is None:
         timestamp = timestamp.replace(tzinfo=timezone.utc)
         
    now = datetime.now(timezone.utc)
    
    if timestamp < now:
        raise HTTPException(
            status_code=400,
            detail="Expiration time cannot be in the past"
        )
        
    max_expiry = now + timedelta(days=max_days)
    
    if timestamp > max_expiry:
        raise HTTPException(
            status_code=400, 
            detail=f"Expiration time cannot be more than {max_days} days in the future"
        )
        
    return timestamp

