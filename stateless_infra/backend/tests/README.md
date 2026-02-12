# Tests Directory

This directory contains the test suite for the stateless infrastructure backend.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Test Structure

- `test_api.py` - API endpoint tests
  - Health checks
  - Tenant validation
  - Bot execution
  - iOS integration
  - Affiliate system

## Writing New Tests

All tests should:
1. Use `@pytest.mark.asyncio` for async tests
2. Include `X-App-ID` header for protected endpoints
3. Assert both status codes and response data
4. Clean up any test data created

Example:
```python
@pytest.mark.asyncio
async def test_new_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/new-endpoint",
            headers={"X-App-ID": "test-app"}
        )
    assert response.status_code == 200
```
