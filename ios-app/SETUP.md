# iOS App Setup Guide

## Prerequisites

- macOS (required for iOS development)
- Xcode 14 or higher
- iOS 16+ Simulator or physical device

## Step 1: Install Xcode

1. Open the Mac App Store
2. Search for "Xcode"
3. Click "Get" or "Install"
4. Wait for installation (Xcode is large, ~10GB+)

Or download from [https://developer.apple.com/xcode/](https://developer.apple.com/xcode/)

## Step 2: Create Xcode Project

### Option A: Create New Project

1. Open Xcode
2. Select "Create a new Xcode project"
3. Choose "iOS" → "App"
4. Configure project:
   - **Product Name**: `PokemonCardAgg`
   - **Team**: Select your team (or None for local testing)
   - **Organization Identifier**: `com.yourname` (or any reverse domain)
   - **Interface**: `SwiftUI`
   - **Language**: `Swift`
   - **Storage**: None
   - **Include Tests**: Optional
5. Click "Next"
6. Save to `ios-app/` directory
7. Click "Create"

### Option B: Use Existing Files

If you already have the Swift files in `ios-app/PokemonCardAgg/`:

1. Open Xcode
2. File → New → Project
3. Follow steps above
4. Replace the default files with the provided files:
   - `PokemonCardAggApp.swift`
   - `ContentView.swift`
   - `NetworkManager.swift`
   - `Models.swift`

## Step 3: Add Files to Project

If files aren't automatically included:

1. Right-click on the `PokemonCardAgg` folder in Xcode
2. Select "Add Files to PokemonCardAgg..."
3. Select all `.swift` files
4. Make sure "Copy items if needed" is checked
5. Click "Add"

## Step 4: Configure Backend Connection

### For iOS Simulator (Default)

The default configuration uses `http://127.0.0.1:5000` which works for the Simulator.

No changes needed if testing in Simulator!

### For Physical Device

If testing on a physical iPhone/iPad:

1. Find your computer's local IP address:

   **macOS:**
   ```bash
   ipconfig getifaddr en0
   ```
   
   **Windows:**
   ```powershell
   ipconfig
   # Look for "IPv4 Address" under your active network adapter
   ```

2. Open `NetworkManager.swift` in Xcode

3. Update the base URL:
   ```swift
   // Change from:
   private let baseURL = "http://127.0.0.1:5000"
   
   // To your computer's IP:
   private let baseURL = "http://192.168.1.100:5000"  // Use YOUR actual IP
   ```

4. **Important**: Make sure your iPhone/iPad is on the same WiFi network as your computer

## Step 5: Configure App Transport Security (ATS)

Since we're using HTTP (not HTTPS) for local development, we need to allow insecure connections.

1. Open `Info.plist` in Xcode
2. Right-click in the editor → "Add Row"
3. Add the following:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

Or in the Xcode property list editor:
- Key: `App Transport Security Settings` (Dictionary)
  - Key: `Allow Arbitrary Loads` (Boolean) = `YES`

**Note:** This is only for development. In production, use HTTPS.

## Step 6: Build and Run

1. Make sure the backend is running:
   ```bash
   cd backend
   python app.py
   ```

2. In Xcode:
   - Select a simulator (e.g., "iPhone 15 Pro")
   - Click the "Play" button (▶) or press `⌘R`

3. Wait for the app to build and launch

## Step 7: Test the App

1. Enter a Pokémon name (e.g., "Charizard")
2. Tap the search button or press return
3. You should see:
   - Card metadata section
   - List of active listings
   - Tap any listing to see details

## Troubleshooting

### "No such module 'SwiftUI'"

- Make sure you're using Xcode 11 or higher
- Check that iOS deployment target is 13.0 or higher

### "Build Failed" errors

1. Clean build folder: `⇧⌘K` (Shift + Command + K)
2. Clean derived data: Xcode → Preferences → Locations → Derived Data → Delete
3. Restart Xcode

### "Failed to connect to backend"

1. **Check backend is running:**
   ```bash
   curl http://127.0.0.1:5000/health
   ```

2. **For Simulator**: Use `http://127.0.0.1:5000`

3. **For Physical Device**: 
   - Use your computer's local IP
   - Ensure both devices are on the same WiFi
   - Check firewall isn't blocking port 5000

4. **Check ATS configuration** in Info.plist

### "The operation couldn't be completed"

This usually means the backend isn't reachable:
- Verify backend is running
- Check the URL in `NetworkManager.swift`
- For device testing, verify IP address is correct

### Simulator not showing up

1. Xcode → Preferences → Components
2. Download desired iOS Simulator versions
3. Restart Xcode

### Code signing errors

For local testing:
1. Select the project in Xcode
2. Go to "Signing & Capabilities"
3. Set "Team" to your Apple ID or "None"
4. Xcode will create a development certificate

## Running on Physical Device

1. Connect your iPhone/iPad via USB
2. Trust the computer on your device
3. In Xcode, select your device from the device menu
4. Update `NetworkManager.swift` with your computer's IP
5. Click Run (▶)
6. On first run, go to Settings → General → VPN & Device Management
7. Trust the developer certificate

## Project Structure

```
PokemonCardAgg/
├── PokemonCardAggApp.swift      # App entry point (@main)
├── ContentView.swift            # Main UI views
│   ├── ContentView              # Search screen
│   ├── SearchResultsView        # Results list
│   ├── CardMetadataView         # Card details
│   ├── ListingRowView           # Listing row
│   └── ListingDetailView        # Listing detail screen
├── NetworkManager.swift         # API networking
│   ├── NetworkManager class     # Singleton for API calls
│   └── NetworkError enum        # Error handling
└── Models.swift                 # Data models
    ├── SearchResult             # API response
    ├── CardMetadata             # Card info
    └── Listing                  # eBay listing
```

## Customization

### Change Colors

Edit `ContentView.swift`:

```swift
// Grade colors
private func gradeColor(for grade: Double) -> Color {
    switch grade {
    case 10:
        return .yellow  // Change to .orange, .red, etc.
    case 9..<10:
        return .gray
    // ...
    }
}

// Company colors
private func companyColor(for company: String) -> Color {
    switch company {
    case "PSA":
        return .blue  // Change to your preferred color
    // ...
    }
}
```

### Change API URL

Edit `NetworkManager.swift`:

```swift
private let baseURL = "https://your-production-api.com"
```

### Modify UI Layout

All UI is in `ContentView.swift`. SwiftUI makes it easy to customize:
- Change fonts: `.font(.title)` → `.font(.headline)`
- Adjust spacing: `spacing: 12` → `spacing: 20`
- Modify colors: `.foregroundColor(.blue)` → `.foregroundColor(.red)`

## Deployment to App Store

1. **Enroll in Apple Developer Program** ($99/year)
2. **Configure signing** with your team
3. **Create App Store listing** in App Store Connect
4. **Archive the app**: Product → Archive
5. **Upload to App Store Connect**
6. **Submit for review**

**Before submitting:**
- Use HTTPS for backend (not HTTP)
- Remove development-only code
- Test thoroughly on multiple devices
- Add app icons and screenshots
- Write privacy policy

## Additional Resources

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Xcode Help](https://developer.apple.com/documentation/xcode)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/ios)
