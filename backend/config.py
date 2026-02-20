"""
Configuration file for Pokemon Card Aggregator API.

Set your API credentials here or use environment variables.
"""

import os

# Unified Backend API Base URL
API_BASE_URL = os.environ.get(
    'API_BASE_URL',
    'https://price-aggregator-api-production.up.railway.app'
)

# Pokemon TCG API Key (optional but recommended for higher rate limits)
# Get your key at: https://dev.pokemontcg.io/
POKEMONTCG_API_KEY = os.environ.get('POKEMONTCG_API_KEY', '')

# eBay API Credentials (required)
# Get your credentials at: https://developer.ebay.com/
EBAY_APP_ID = os.environ.get('EBAY_APP_ID', 'YOUR_EBAY_APP_ID_HERE')
EBAY_DEV_ID = os.environ.get('EBAY_DEV_ID', 'YOUR_EBAY_DEV_ID_HERE')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID', 'YOUR_EBAY_CERT_ID_HERE')

# Flask Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# CORS Configuration
CORS_ORIGINS = '*'  # In production, specify allowed origins
