# Stateless Multi-Tenant Infrastructure

A production-ready FastAPI backend designed for **iOS and Web apps** with strict privacy enforcement and ephemeral data lifecycles.

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with async support
- **Database**: Postgres with auto-expiring rows (`expires_at`)
- **Storage**: S3-compatible object storage
- **Email**: SendGrid (stateless)
- **Deployment**: Docker + Render
- **CI/CD**: GitHub Actions

## 🔒 Privacy-First Design

- **Multi-tenant**: Isolated by `X-App-ID` header
- **No PII Storage**: All user data is ephemeral
- **Auto-Cleanup**: Background scheduler deletes expired data every minute
- **Stateless Tokens**: APNs tokens and affiliate codes are transient

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt  # or use pyproject.toml

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the server
uvicorn app.main:app --reload
```

### Docker

```bash
docker build -t stateless-backend .
docker run -p 8000:8000 stateless-backend
```

## 📡 API Endpoints

### Core
- `GET /health` - Health check (rate limited: 10/min)
- `GET /` - Root endpoint

### Bots (`/api/v1/bots`)
- `POST /execute` - Execute bot task (rate limited: 30/min)

### iOS (`/api/v1/ios`)
- `POST /register-token` - Register APNs token (ephemeral)
- `POST /validate-receipt` - Validate StoreKit receipt

### Affiliate (`/api/v1/affiliate`)
- `POST /generate` - Generate referral code (stateless hash)
- `POST /conversion` - Track conversion metrics

## 🔧 Configuration

Key environment variables:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=your-bucket
SENDGRID_API_KEY=your-sendgrid-key
```

## 🛡️ Production Features

- **Rate Limiting**: Per-tenant limits (via `X-App-ID`)
- **Background Scheduler**: Auto-cleanup every 1 minute
- **Multi-tenant Middleware**: Enforces tenant isolation
- **Graceful Shutdown**: Scheduler cleanup on shutdown

## 📦 Deployment

### Render

1. Push to GitHub
2. Connect Render to your repo
3. Use `render.yaml` for infrastructure-as-code
4. Set environment variables in Render dashboard

### Manual

```bash
# Build
docker build -t stateless-backend .

# Run
docker run -p 8000:8000 \
  -e DATABASE_URL=... \
  -e SECRET_KEY=... \
  stateless-backend
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Bot execution (requires X-App-ID)
curl -X POST http://localhost:8000/api/v1/bots/execute \
  -H "X-App-ID: test-app" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "email", "context": {"subject": "Test"}}'
```

## 📝 License

MIT
