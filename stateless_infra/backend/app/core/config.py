from pydantic_settings import BaseSettings
from typing import Optional
import sys

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stateless Infra API"
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/db"
    SECRET_KEY: str = "changeme"
    ENVIRONMENT: str = "development"
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "stateless-bucket"
    
    # SendGrid
    SENDGRID_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "noreply@example.com"
    
    # Affiliate System
    AFFILIATE_SALT: str = "changeme-affiliate-salt"
    
    # Database Connection Pool
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # Bot Runtime
    BOT_TIMEOUT_SECONDS: int = 30
    
    # Rate Limiting (optional Redis for distributed rate limiting)
    REDIS_URL: Optional[str] = None
    
    # Request Size Limits
    MAX_REQUEST_BODY_BYTES: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
    
    def validate_production_secrets(self):
        """Validate that production secrets are not using defaults."""
        if self.ENVIRONMENT == "production":
            dangerous_defaults = []
            
            if self.SECRET_KEY == "changeme":
                dangerous_defaults.append("SECRET_KEY")
            
            if self.AWS_ACCESS_KEY_ID == "minioadmin":
                dangerous_defaults.append("AWS_ACCESS_KEY_ID")
            
            if self.AWS_SECRET_ACCESS_KEY == "minioadmin":
                dangerous_defaults.append("AWS_SECRET_ACCESS_KEY")
            
            if self.AFFILIATE_SALT == "changeme-affiliate-salt":
                dangerous_defaults.append("AFFILIATE_SALT")
            
            if dangerous_defaults:
                print(f"FATAL: Production environment detected with default secrets: {', '.join(dangerous_defaults)}")
                print("Set proper values in environment variables or .env file")
                sys.exit(1)

settings = Settings()
