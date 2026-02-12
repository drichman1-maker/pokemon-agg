import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_malicious_tenant_id_sql_injection():
    """Test that SQL injection attempts in X-App-ID are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "'; DROP TABLE drafts; --"},
            json={"task_type": "email_campaign", "context": {}}
        )
    
    assert response.status_code == 400
    assert "Invalid tenant ID format" in response.json()["error"]


@pytest.mark.asyncio
async def test_malicious_tenant_id_xss():
    """Test that XSS attempts in X-App-ID are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "<script>alert('xss')</script>"},
            json={"task_type": "email_campaign", "context": {}}
        )
    
    assert response.status_code == 400
    assert "Invalid tenant ID format" in response.json()["error"]


@pytest.mark.asyncio
async def test_malicious_tenant_id_path_traversal():
    """Test that path traversal attempts in X-App-ID are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "../../../etc/passwd"},
            json={"task_type": "email_campaign", "context": {}}
        )
    
    assert response.status_code == 400
    assert "Invalid tenant ID format" in response.json()["error"]


@pytest.mark.asyncio
async def test_tenant_id_too_long():
    """Test that excessively long tenant IDs are rejected."""
    long_id = "a" * 100
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": long_id},
            json={"task_type": "email_campaign", "context": {}}
        )
    
    assert response.status_code == 400
    assert "too long" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_valid_tenant_id_formats():
    """Test that valid tenant ID formats are accepted."""
    valid_ids = [
        "app123",
        "my-app",
        "my_app",
        "App-123_Test",
        "a",
        "1",
        "a" * 64  # Max length
    ]
    
    for tenant_id in valid_ids:
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/bots/execute",
                headers={"X-App-ID": tenant_id},
                json={"task_type": "email_campaign", "context": {}}
            )
        
        # Should not fail on validation (may fail on other things)
        assert response.status_code != 400 or "Invalid tenant ID format" not in response.json().get("error", "")


@pytest.mark.asyncio
async def test_bot_invalid_task_type():
    """Test that invalid task types are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "test-app"},
            json={"task_type": "malicious_task", "context": {}}
        )
    
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_bot_context_too_large():
    """Test that oversized context payloads are rejected."""
    # Create a context larger than 1MB
    large_context = {"data": "x" * (2 * 1024 * 1024)}  # 2MB
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/bots/execute",
            headers={"X-App-ID": "test-app"},
            json={"task_type": "email_campaign", "context": large_context}
        )
    
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_affiliate_code_verification():
    """Test that affiliate code verification works correctly."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Generate a code
        gen_response = await client.post(
            "/api/v1/affiliate/generate",
            headers={"X-App-ID": "test-app"},
            json={"session_id": "test-session-123"}
        )
        
        assert gen_response.status_code == 200
        code = gen_response.json()["code"]
        
        # Try to use the code with correct session
        conv_response = await client.post(
            "/api/v1/affiliate/conversion",
            headers={"X-App-ID": "test-app"},
            json={
                "code": code,
                "session_id": "test-session-123",
                "value": 99.99,
                "currency": "USD"
            }
        )
        
        assert conv_response.status_code == 200
        assert conv_response.json()["status"] == "recorded"


@pytest.mark.asyncio
async def test_affiliate_code_invalid():
    """Test that invalid affiliate codes are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/affiliate/conversion",
            headers={"X-App-ID": "test-app"},
            json={
                "code": "INVALID",
                "session_id": "wrong-session",
                "value": 99.99,
                "currency": "USD"
            }
        )
        
        assert response.status_code == 400
        assert "Invalid affiliate code" in response.json()["detail"]


@pytest.mark.asyncio
async def test_admin_error_sanitization():
    """Test that admin endpoints don't leak internal error details."""
    # This test would need to trigger a database error
    # For now, we just verify the endpoint structure
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/admin/stats",
            headers={"X-App-ID": "test-app"}
        )
        
        # Should return stats or generic error, not detailed exception
        if response.status_code != 200:
            error_msg = response.json().get("error", "")
            assert "Traceback" not in error_msg
            assert "Exception" not in error_msg
            assert "sqlalchemy" not in error_msg.lower()


@pytest.mark.asyncio
async def test_session_id_validation():
    """Test that invalid session IDs are rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Empty session ID
        response = await client.post(
            "/api/v1/affiliate/generate",
            headers={"X-App-ID": "test-app"},
            json={"session_id": ""}
        )
        
        assert response.status_code == 400
        
        # Excessively long session ID
        long_session = "x" * 200
        response = await client.post(
            "/api/v1/affiliate/generate",
            headers={"X-App-ID": "test-app"},
            json={"session_id": long_session}
        )
        
        assert response.status_code == 400
