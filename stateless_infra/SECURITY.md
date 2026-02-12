# Security Policy

## Overview

This document outlines the security policies and best practices for the stateless infrastructure.

## Authentication & Authorization

### Tenant Identification
- All API requests (except health checks and docs) **MUST** include the `X-App-ID` header
- Tenant IDs are validated using regex: `^[a-zA-Z0-9_-]{1,64}$`
- Invalid tenant IDs are rejected with HTTP 400
- Maximum length: 64 characters

### Secrets Management
- **NEVER** commit secrets to version control
- All secrets must be provided via environment variables or `.env` file
- Production deployments **MUST NOT** use default values
- System performs startup validation and exits if defaults detected in production

### Required Secrets
- `SECRET_KEY`: Application secret key (min 32 characters recommended)
- `AWS_ACCESS_KEY_ID`: AWS credentials for S3
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AFFILIATE_SALT`: Salt for affiliate code generation
- `SENDGRID_API_KEY`: Email service API key (optional)

## Input Validation

### Tenant ID Validation
- Alphanumeric, underscore, and hyphen only
- Length: 1-64 characters
- Prevents SQL injection, XSS, and path traversal attacks

### Payload Size Limits
- Bot context: Maximum 1MB
- S3 uploads: Maximum 100MB
- Request body: Maximum 10MB

### Task Type Allowlist
Bot execution only accepts the following task types:
- `email_campaign`
- `social_post`
- `data_export`
- `report_generation`

## Data Lifecycle

### Time-To-Live (TTL) Policies
- **Drafts**: 24 hours default
- **Bot Outputs**: 48 hours default
- All timestamps are UTC timezone-aware
- Cleanup runs every 60 minutes via scheduler

### Data Deletion
- Hard deletion (no soft deletes)
- Automatic cleanup via background scheduler
- Manual cleanup available via admin endpoint
- Transaction rollback on cleanup errors

## Error Handling

### Error Message Sanitization
- Generic error messages returned to clients
- Detailed errors logged server-side only
- No stack traces or internal details exposed
- HTTP status codes used appropriately

### Exception Types
- `400 Bad Request`: Invalid input, validation failures
- `413 Payload Too Large`: Exceeds size limits
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side failures (generic message)

## Rate Limiting

### Per-Tenant Limits
- Bot execution: 30 requests/minute
- Health check: 10 requests/minute
- Admin endpoints: No rate limiting (consider adding)

### Implementation
- Uses `SlowAPI` with `X-App-ID` as rate limit key
- In-memory storage (consider Redis for production)

## Logging & Monitoring

### What to Log
- ✅ Authentication failures (invalid tenant IDs)
- ✅ Validation errors (sanitized)
- ✅ Service errors (email, S3, database)
- ✅ Cleanup operations (success/failure)
- ✅ Affiliate code generation and conversions

### What NOT to Log
- ❌ User passwords or secrets
- ❌ Full request payloads (may contain PII)
- ❌ Database connection strings
- ❌ API keys or tokens

### Log Levels
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Validation failures, rejected requests
- `ERROR`: Service failures, exceptions

## Database Security

### Connection Pool
- Pool size: 20 connections
- Max overflow: 10 connections
- Pool timeout: 30 seconds
- Pre-ping enabled (verify connections before use)

### Query Safety
- All queries use SQLAlchemy ORM (prevents SQL injection)
- Tenant ID validated before database queries
- Parameterized queries only

## External Services

### S3 Storage
- Presigned URLs expire after 1 hour
- File size validation before upload
- Empty file uploads logged as warnings
- Errors raise exceptions (no silent failures)

### SendGrid Email
- API key required for email service
- Errors raise exceptions (no silent failures)
- Email addresses validated before sending
- Logging includes success/failure status

## Disaster Recovery

### Backup Strategy
- Database backups managed by hosting provider (Render)
- No application-level backups (ephemeral data by design)
- Point-in-time recovery available via Render

### Accidental Deletion
- **WARNING**: Cleanup is hard delete with no recovery
- Ensure `expires_at` timestamps are set correctly
- Test cleanup logic in staging before production
- Monitor cleanup logs for unexpected deletions

## Deployment Security

### Environment Validation
- Startup checks for default secrets in production
- Application exits if validation fails
- Logs warnings for missing optional configs

### Horizontal Scaling
- **IMPORTANT**: Only ONE instance should run the scheduler
- Use distributed locking or dedicated worker instance
- Scheduler configured with `max_instances=1`

### CI/CD Pipeline
- Automated linting (ruff)
- Automated testing (pytest)
- Deploy only on push to `main` branch
- Environment variables set in Render dashboard

## Incident Response

### If Secrets Are Compromised
1. Immediately rotate all affected secrets
2. Update environment variables in Render
3. Redeploy application
4. Review logs for unauthorized access
5. Notify affected tenants if applicable

### If Data Breach Suspected
1. Review application logs for suspicious activity
2. Check database for unauthorized access patterns
3. Verify tenant isolation is working correctly
4. Audit recent API requests by tenant
5. Document findings and remediation steps

## Security Checklist

### Before Deployment
- [ ] All secrets set in environment variables
- [ ] No default values in production
- [ ] Database connection pool configured
- [ ] Rate limiting enabled
- [ ] Logging configured properly
- [ ] Scheduler running on single instance only
- [ ] Backup strategy confirmed
- [ ] Monitoring and alerting set up

### Regular Audits
- [ ] Review logs for suspicious activity
- [ ] Check cleanup job execution
- [ ] Verify rate limits are effective
- [ ] Test error handling and sanitization
- [ ] Review tenant isolation
- [ ] Update dependencies for security patches

## Contact

For security concerns or to report vulnerabilities, contact the development team immediately.
