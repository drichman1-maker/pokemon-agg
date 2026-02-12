import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test that the health endpoint returns 200 OK."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_missing_app_id_header():
    """Test that requests without X-App-ID header are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/bots/execute", json={
            "task_type": "test",
            "context": {}
        })
    
    assert response.status_code == 400
    assert "Missing X-App-ID header" in response.json()["error"]


@pytest.mark.asyncio
async def test_affiliate_code_generation():
    """Test affiliate code generation with valid tenant."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/affiliate/generate",
            headers={"X-App-ID": "test-app"},
            json={"session_id": "test-session-123"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert data["tenant"] == "test-app"
    assert len(data["code"]) == 8  # Code should be 8 characters


@pytest.mark.asyncio
async def test_bot_execution():
    """Test bot task execution endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "test-app"},
            json={
                "task_type": "email_campaign",
                "context": {"recipient": "test@example.com"}
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["tenant"] == "test-app"
    assert data["ephemeral"] is True


@pytest.mark.asyncio
async def test_root_endpoint_with_tenant():
    """Test root endpoint returns tenant info."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/", headers={"X-App-ID": "test-app"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Stateless Infra API Running"
    assert data["tenant"] == "test-app"


@pytest.mark.asyncio
async def test_ios_register_token():
    """Test iOS APNs token registration."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/ios/register-token",
            headers={"X-App-ID": "test-app"},
            json={
                "token": "test-apns-token-123",
                "device_id": "test-device-456"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["tenant"] == "test-app"


@pytest.mark.asyncio
async def test_ios_validate_receipt():
    """Test iOS StoreKit receipt validation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/ios/validate-receipt",
            headers={"X-App-ID": "test-app"},
            json={"receipt_data": "test-receipt-data"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "valid"
    assert data["tenant"] == "test-app"


@pytest.mark.asyncio
async def test_affiliate_conversion_tracking():
    """Test affiliate conversion tracking."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/affiliate/conversion",
            headers={"X-App-ID": "test-app"},
            json={
                "code": "TESTCODE",
                "value": 99.99,
                "currency": "USD"
            }
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "recorded"
