# Pokémon Card Aggregator Application

A cross-platform application to find graded Pokémon cards (PSA, BGS, CGC) across eBay, with a Python/Flask backend, React web frontend, and native iOS app.

## 🎯 Features

- **Smart Grade Parsing**: Automatically extracts grading company (PSA, BGS, CGC) and grade (1-10) from eBay listing titles
- **Multi-Platform**: Web (React) and iOS (SwiftUI) interfaces
- **Advanced Filtering**: Filter listings by grading company
- **Steal Alerts**: Highlights listings priced 20% below average for their grade
- **Card Metadata**: Displays card images and details from pokemontcg.io
- **Smart Sorting**: Results sorted by grade (high to low), then price (low to high)

## 📁 Project Structure

```
pokemon agg/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── config.py              # Configuration file
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Example environment variables
│
├── web-frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Tailwind CSS styles
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Tailwind configuration
│   └── postcss.config.js     # PostCSS configuration
│
└── ios-app/
    └── PokemonCardAgg/
        ├── PokemonCardAggApp.swift    # App entry point
        ├── ContentView.swift          # Main SwiftUI views
        ├── NetworkManager.swift       # API networking layer
        └── Models.swift               # Data models
```

## 🚀 Setup Instructions

### Prerequisites

- **Backend**: Python 3.8+
- **Web Frontend**: Node.js 16+ and npm
- **iOS App**: macOS with Xcode 14+
- **API Keys**: 
  - eBay Developer credentials (required)
  - pokemontcg.io API key (optional but recommended)

### 1. Backend Setup

#### Get API Credentials

1. **eBay API**: 
   - Sign up at [https://developer.ebay.com/](https://developer.ebay.com/)
   - Create a new application to get your App ID, Dev ID, and Cert ID

2. **Pokémon TCG API** (optional):
   - Get your key at [https://dev.pokemontcg.io/](https://dev.pokemontcg.io/)

#### Install and Run

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (Option 1: .env file)
cp .env.example .env
# Edit .env and add your API credentials

# OR (Option 2: Export directly)
export EBAY_APP_ID="your_app_id"
export EBAY_DEV_ID="your_dev_id"
export EBAY_CERT_ID="your_cert_id"
export POKEMONTCG_API_KEY="your_api_key"  # Optional

# Run the server
python app.py
```

The API will be available at `http://127.0.0.1:5000`

**Test the API:**
```bash
# Health check
curl http://127.0.0.1:5000/health

# Search for cards
curl "http://127.0.0.1:5000/search?q=Charizard"
```

### 2. Web Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Start development server
npm start
```

The web app will open at `http://localhost:3000`

**Build for production:**
```bash
npm run build
```

### 3. iOS App Setup

#### Option A: Using Xcode GUI

1. Open Xcode
2. Select "Create a new Xcode project"
3. Choose "iOS" → "App"
4. Set:
   - Product Name: `PokemonCardAgg`
   - Interface: `SwiftUI`
   - Language: `Swift`
5. Save to `ios-app/` directory
6. Add the following files to your project:
   - `PokemonCardAggApp.swift`
   - `ContentView.swift`
   - `NetworkManager.swift`
   - `Models.swift`

#### Option B: Using Existing Files

If you already have the Swift files:

1. Open the project in Xcode
2. Make sure the backend is running (`python app.py`)
3. Build and run (⌘R)

**For Physical Device Testing:**

If testing on a physical iPhone/iPad, update the base URL in `NetworkManager.swift`:

```swift
// Change from:
private let baseURL = "http://127.0.0.1:5000"

// To your computer's local IP:
private let baseURL = "http://192.168.1.100:5000"  // Use your actual IP
```

Find your local IP:
```bash
# macOS
ipconfig getifaddr en0

# Windows
ipconfig
```

## 🎮 Usage

### Web Application

1. Enter a Pokémon name (e.g., "Charizard", "Pikachu")
2. Click "Search"
3. View card details on the left
4. Browse listings on the right
5. Use filter badges to show specific grading companies
6. Look for green-highlighted "STEAL ALERT" listings

### iOS Application

1. Enter a Pokémon name in the search bar
2. Tap the search button or press return
3. View search results with card metadata
4. Tap any listing to see full details
5. Tap "View on eBay" to open the listing in Safari

## 🔧 API Endpoints

### `GET /search`

Search for graded Pokémon cards.

**Parameters:**
- `q` (required): Search query (e.g., "Charizard")

**Response:**
```json
{
  "query": "Charizard",
  "card": {
    "name": "Charizard",
    "image_url": "https://...",
    "set_name": "Base Set",
    "set_series": "Base",
    "number": "4",
    "rarity": "Rare Holo"
  },
  "listings": [
    {
      "title": "Charizard PSA 10 Base Set...",
      "price": 1250.00,
      "currency": "USD",
      "url": "https://ebay.com/...",
      "company": "PSA",
      "grade": 10,
      "is_steal": false,
      "condition": "New",
      "location": "United States"
    }
  ],
  "total_results": 25
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Pokemon Card Aggregator API"
}
```

## 🎨 Features Breakdown

### Backend (Python/Flask)

- **Grade Parser**: Regex-based extraction of grading information
  - Supports PSA, BGS, and CGC
  - Validates grades are in 1-10 range
  - Handles decimal grades (e.g., 9.5)

- **Steal Alert Algorithm**:
  - Calculates average price per grade
  - Marks listings 20% below average as "steals"

- **Sorting Logic**:
  - Primary: Grade (descending)
  - Secondary: Price (ascending)

### Web Frontend (React)

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Filtering**: Client-side filtering for instant results
- **Modern UI**: Gradient backgrounds, shadows, and smooth transitions
- **Accessibility**: Semantic HTML and keyboard navigation

### iOS App (SwiftUI)

- **Native Performance**: Built with SwiftUI for iOS 16+
- **Color-Coded Grades**:
  - Grade 10: Gold (Yellow)
  - Grade 9: Silver (Gray)
  - Grade 8: Bronze (Orange)
  - Grade 7 and below: Standard (Gray)
- **Async/Await**: Modern Swift concurrency
- **Error Handling**: User-friendly error messages

## 🐛 Troubleshooting

### Backend Issues

**"No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**"Invalid eBay credentials"**
- Verify your API keys in `.env` or environment variables
- Check that you're using Production credentials (not Sandbox)

**"No listings found"**
- eBay API may be rate-limited
- Try a different search query
- Check eBay's API status

### Web Frontend Issues

**"Failed to fetch results"**
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify API URL in `App.js`

**Blank page after npm start**
- Clear browser cache
- Run `npm install` again
- Check console for errors

### iOS App Issues

**"No data received from server"**
- Ensure backend is running
- For Simulator: Use `http://127.0.0.1:5000`
- For Device: Use your computer's local IP

**Build errors**
- Clean build folder (⇧⌘K)
- Ensure iOS deployment target is 16.0+
- Check that all files are added to the target

## 📝 License

This project is for educational purposes. Make sure to comply with eBay's API Terms of Service and pokemontcg.io's usage guidelines.

## 🙏 Acknowledgments

- [pokemontcg.io](https://pokemontcg.io/) for card metadata
- [eBay Finding API](https://developer.ebay.com/) for live listings
- React, Tailwind CSS, and SwiftUI communities

## 🔮 Future Enhancements

- [ ] Price history tracking
- [ ] Email alerts for new steals
- [ ] Saved searches
- [ ] User authentication
- [ ] Watchlist functionality
- [ ] Additional marketplaces (TCGPlayer, etc.)
- [ ] Android app (React Native or Kotlin)
