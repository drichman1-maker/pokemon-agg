# Backend Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- eBay Developer account
- (Optional) pokemontcg.io API key

## Step 1: Get API Credentials

### eBay API (Required)

1. Go to [https://developer.ebay.com/](https://developer.ebay.com/)
2. Sign in or create an account
3. Navigate to "My Account" → "Application Keys"
4. Create a new application (if you haven't already)
5. Note down:
   - **App ID** (Client ID)
   - **Dev ID**
   - **Cert ID** (Client Secret)

### Pokémon TCG API (Optional but Recommended)

1. Go to [https://dev.pokemontcg.io/](https://dev.pokemontcg.io/)
2. Sign up for a free API key
3. Higher rate limits with an API key

## Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 3: Configure API Keys

### Option A: Environment Variables

**Windows (PowerShell):**
```powershell
$env:EBAY_APP_ID="your_app_id_here"
$env:EBAY_DEV_ID="your_dev_id_here"
$env:EBAY_CERT_ID="your_cert_id_here"
$env:POKEMONTCG_API_KEY="your_api_key_here"
```

**macOS/Linux:**
```bash
export EBAY_APP_ID="your_app_id_here"
export EBAY_DEV_ID="your_dev_id_here"
export EBAY_CERT_ID="your_cert_id_here"
export POKEMONTCG_API_KEY="your_api_key_here"
```

### Option B: .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   POKEMONTCG_API_KEY=your_api_key_here
   EBAY_APP_ID=your_app_id_here
   EBAY_DEV_ID=your_dev_id_here
   EBAY_CERT_ID=your_cert_id_here
   ```

3. Install python-dotenv (if using .env):
   ```bash
   pip install python-dotenv
   ```

4. Update `app.py` to load .env:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Step 4: Run the Server

```bash
python app.py
```

You should see:
```
Starting Pokemon Card Aggregator API...
API will be available at http://127.0.0.1:5000

Endpoints:
  GET /search?q=<query>  - Search for Pokemon cards
  GET /health            - Health check

Note: Make sure to set your eBay API credentials in environment variables or config.py
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## Step 5: Test the API

### Health Check

```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Pokemon Card Aggregator API"
}
```

### Search Test

```bash
curl "http://127.0.0.1:5000/search?q=Charizard"
```

You should receive JSON with card metadata and listings.

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "Invalid eBay credentials" or empty listings

1. Verify your API keys are correct
2. Make sure you're using **Production** credentials (not Sandbox)
3. Check eBay Developer account status
4. Try a different search query

### CORS errors from web frontend

The backend already has CORS enabled via `flask-cors`. If you still see errors:
1. Make sure the backend is running
2. Check that the web frontend is using the correct API URL
3. Restart the backend server

### Port 5000 already in use

Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

Then update the API URL in the web and iOS apps.

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `config.py`
2. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Set up proper environment variable management
4. Configure CORS to allow only specific origins
5. Add rate limiting and authentication
6. Use HTTPS

## API Rate Limits

- **eBay Finding API**: 5,000 calls per day (free tier)
- **pokemontcg.io**: 1,000 requests/day without key, 20,000/day with key

Monitor your usage to avoid hitting limits.
