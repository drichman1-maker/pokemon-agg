from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime, timedelta, timezone
import uuid

# Default TTL values (in hours)
DEFAULT_DRAFT_TTL_HOURS = 24
DEFAULT_BOT_OUTPUT_TTL_HOURS = 48

class Draft(Base):
    __tablename__ = "drafts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    @staticmethod
    def default_expires_at(hours: int = DEFAULT_DRAFT_TTL_HOURS) -> datetime:
        """Generate default expiration timestamp (UTC)."""
        return datetime.now(timezone.utc) + timedelta(hours=hours)

class BotOutput(Base):
    __tablename__ = "bot_outputs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, index=True, nullable=False)
    output_data = Column(Text, nullable=False) # JSON or serialized content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    @staticmethod
    def default_expires_at(hours: int = DEFAULT_BOT_OUTPUT_TTL_HOURS) -> datetime:
        """Generate default expiration timestamp (UTC)."""
        return datetime.now(timezone.utc) + timedelta(hours=hours)
