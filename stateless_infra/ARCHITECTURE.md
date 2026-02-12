# Stateless Infrastructure Architecture

## Overview

This infrastructure is designed to support **ephemeral, multi-tenant applications** where data privacy and automatic cleanup are paramount. The system enforces strict data lifecycle policies and tenant isolation.

## Core Principles

### 1. Statelessness
- **No Long-Term User Data**: All data has a TTL (Time To Live)
- **Ephemeral Storage**: Files stored in S3 with presigned URLs that expire
- **Transient Sessions**: No persistent user sessions or authentication tokens

### 2. Multi-Tenancy
- **Tenant Identifier**: `X-App-ID` header required on all requests
- **Data Isolation**: Database queries scoped by `tenant_id`
- **Rate Limiting**: Per-tenant limits prevent resource abuse

### 3. Privacy-First
- **No PII Storage**: System designed to avoid storing personal information
- **Aggregate Metrics Only**: Conversion tracking stores counts, not user data
- **Automatic Deletion**: Expired data is hard-deleted, not soft-deleted

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Apps                          │
│                    (iOS, Web, Mobile)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │ X-App-ID Header
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Tenant Middleware                          │  │
│  │  - Validates X-App-ID header                         │  │
│  │  - Injects tenant_id into request state             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Rate Limiter (SlowAPI)                     │  │
│  │  - Per-tenant request limits                         │  │
│  │  - Prevents abuse and ensures fair usage            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                API Endpoints                          │  │
│  │  - /api/v1/bots      (Bot Runtime)                   │  │
│  │  - /api/v1/ios       (APNs, StoreKit)               │  │
│  │  - /api/v1/affiliate (Referral System)              │  │
│  │  - /api/v1/admin     (Admin Operations)             │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────┬──────────────────┬──────────────────┬──────────┘
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PostgreSQL    │  │   AWS S3 /      │  │   SendGrid      │
│   Database      │  │   MinIO         │  │   Email API     │
│                 │  │                 │  │                 │
│ - Drafts        │  │ - Temp Files    │  │ - Transactional │
│ - Bot Outputs   │  │ - Presigned     │  │   Emails        │
│ - TTL Indexes   │  │   URLs          │  │ - No Storage    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│              Background Scheduler (APScheduler)              │
│  - Runs cleanup every hour                                   │
│  - Hard deletes expired rows from database                   │
│  - Logs cleanup metrics                                      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Bot Execution Flow
```
Client → POST /api/v1/bots/execute
  ↓
Middleware validates X-App-ID
  ↓
Bot Runtime executes task
  ↓
Result stored in bot_outputs table (with expires_at)
  ↓
Response returned to client
  ↓
[After TTL expires] → Scheduler deletes row
```

### 2. Affiliate Code Flow
```
Client → POST /api/v1/affiliate/generate
  ↓
Generate hash from: app_id + session_id + salt
  ↓
Return code (no database storage)
  ↓
Client → POST /api/v1/affiliate/conversion
  ↓
Log aggregate metric (no user data)
```

### 3. iOS Notification Flow
```
iOS App → POST /api/v1/ios/register-token
  ↓
Token cached temporarily (Redis/Memory)
  ↓
Used for immediate notification
  ↓
Discarded after use (no persistent storage)
```

## Database Schema

### Drafts Table
Stores temporary draft content with automatic expiration.

```sql
CREATE TABLE drafts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_drafts_tenant_id ON drafts(tenant_id);
CREATE INDEX idx_drafts_expires_at ON drafts(expires_at);
```

### Bot Outputs Table
Stores bot execution results temporarily.

```sql
CREATE TABLE bot_outputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR NOT NULL,
    output_data TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_bot_outputs_tenant_id ON bot_outputs(tenant_id);
CREATE INDEX idx_bot_outputs_expires_at ON bot_outputs(expires_at);
```

**Key Design Decisions:**
- `expires_at` is indexed for efficient cleanup queries
- `tenant_id` is indexed for fast tenant-scoped queries
- No foreign keys to other tables (stateless design)
- UUID primary keys for distributed systems

## Services

### Affiliate Service
- **Stateless Code Generation**: Uses SHA-256 hash of `app_id + session_id + salt`
- **No Database Storage**: Codes are deterministic and verifiable without storage
- **Aggregate Metrics**: Conversion tracking stores only counts, not user data

### Bot Runtime
- **Task Execution**: Integrates with Clawi or similar bot frameworks
- **Ephemeral Results**: Outputs stored with TTL, then deleted
- **Async Processing**: Uses Python's asyncio for concurrent tasks

### Email Service
- **SendGrid Integration**: Sends transactional emails
- **No Email Storage**: Emails sent and forgotten (no logs)
- **Template Support**: Can use SendGrid templates for consistency

### Storage Service
- **S3 Compatible**: Works with AWS S3, MinIO, or any S3-compatible storage
- **Presigned URLs**: Time-limited access to uploaded files
- **No Permanent Storage**: Files should have lifecycle policies for auto-deletion

### Cleanup Service
- **Scheduled Execution**: Runs every hour via APScheduler
- **Hard Deletion**: Permanently removes expired rows
- **Logging**: Records cleanup metrics for monitoring

## Security

### Tenant Isolation
- **Middleware Enforcement**: All requests must include `X-App-ID`
- **Query Scoping**: Database queries filtered by `tenant_id`
- **No Cross-Tenant Access**: Tenants cannot access each other's data

### Rate Limiting
- **Per-Tenant Limits**: Each tenant has independent rate limits
- **Endpoint-Specific**: Different limits for different endpoints
- **SlowAPI Integration**: Uses Redis or in-memory storage for counters

### Data Protection
- **No PII**: System designed to avoid storing personal information
- **Encryption in Transit**: HTTPS required for all connections
- **Encryption at Rest**: Database and S3 encryption enabled
- **Automatic Cleanup**: Data deleted after TTL expires

## Deployment

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Security
SECRET_KEY=random-secret-key-here

# AWS S3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket

# SendGrid
SENDGRID_API_KEY=your-key
EMAIL_FROM=noreply@yourdomain.com

# Environment
ENVIRONMENT=production
```

### Render Deployment
The `render.yaml` file defines:
- **Web Service**: FastAPI backend with Docker runtime
- **Database**: Managed PostgreSQL with automatic backups
- **Environment Variables**: Injected from Render dashboard
- **Auto-Deploy**: Triggered on push to main branch

### Scaling Considerations
- **Horizontal Scaling**: Multiple FastAPI instances behind load balancer
- **Database Pooling**: Connection pooling for efficient database access
- **Scheduler**: Only one instance should run cleanup (use leader election)
- **Caching**: Redis for rate limiting and temporary token storage

## Monitoring

### Health Checks
- `GET /health` - Basic health check
- `GET /api/v1/admin/health-detailed` - Database connectivity check

### Metrics to Track
- Request rate per tenant
- Database query performance
- Cleanup job execution time
- Number of expired rows deleted
- S3 upload/download rates
- Email delivery success rates

### Logging
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Tenant ID included in all logs for tracing
- Cleanup job results logged for auditing

## Future Enhancements

1. **Redis Integration**: For caching and distributed rate limiting
2. **Webhook Support**: Async webhooks for bot results
3. **GraphQL API**: Alternative to REST for complex queries
4. **Real-time Updates**: WebSocket support for live notifications
5. **Advanced Analytics**: Time-series metrics without storing user data
6. **Multi-Region**: Deploy across multiple regions for low latency
7. **Backup Strategy**: Point-in-time recovery for database
8. **Disaster Recovery**: Automated failover and recovery procedures
