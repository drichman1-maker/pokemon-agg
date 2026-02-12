# Web Frontend Setup Guide

## Prerequisites

- Node.js 16 or higher
- npm (comes with Node.js)

## Step 1: Install Node.js

If you don't have Node.js installed:

**Windows:**
- Download from [https://nodejs.org/](https://nodejs.org/)
- Run the installer
- Verify installation:
  ```powershell
  node --version
  npm --version
  ```

**macOS:**
```bash
# Using Homebrew
brew install node

# Verify
node --version
npm --version
```

## Step 2: Install Dependencies

```bash
cd web-frontend
npm install
```

This will install:
- React 18
- Tailwind CSS
- Axios
- React Scripts
- PostCSS and Autoprefixer

## Step 3: Configure API URL (if needed)

The app connects to `http://127.0.0.1:5000` by default.

If your backend is on a different URL, edit `src/App.js`:

```javascript
const API_BASE_URL = 'http://your-backend-url:5000';
```

## Step 4: Start Development Server

```bash
npm start
```

The app will automatically open in your browser at `http://localhost:3000`

## Step 5: Test the Application

1. Make sure the backend is running (`python app.py`)
2. Enter a Pokémon name (e.g., "Charizard")
3. Click "Search"
4. You should see:
   - Card image on the left
   - Listings table on the right
   - Filter badges at the top

## Available Scripts

### `npm start`
Runs the app in development mode.
- Opens [http://localhost:3000](http://localhost:3000)
- Hot reload enabled
- Shows lint errors in console

### `npm run build`
Builds the app for production to the `build` folder.
- Optimizes for best performance
- Minifies code
- Hashes filenames for caching

### `npm test`
Launches the test runner in interactive watch mode.

## Troubleshooting

### "npm: command not found"

Install Node.js from [https://nodejs.org/](https://nodejs.org/)

### Port 3000 already in use

The app will prompt you to use a different port. Press `Y` to continue.

Or specify a different port:
```bash
# Windows (PowerShell)
$env:PORT=3001; npm start

# macOS/Linux
PORT=3001 npm start
```

### "Failed to fetch results"

1. **Check backend is running:**
   ```bash
   curl http://127.0.0.1:5000/health
   ```

2. **Check browser console** (F12) for errors

3. **Verify API URL** in `src/App.js`

### Blank page after build

If you're deploying to a subdirectory, add to `package.json`:
```json
{
  "homepage": "/your-subdirectory"
}
```

### Tailwind styles not working

1. Make sure `tailwind.config.js` exists
2. Verify `index.css` has Tailwind directives:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
3. Restart the dev server

## Building for Production

```bash
npm run build
```

This creates a `build/` folder with optimized files.

### Serve the production build locally:

```bash
# Install serve globally
npm install -g serve

# Serve the build folder
serve -s build
```

### Deploy to hosting:

**Netlify:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

**Vercel:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**GitHub Pages:**
1. Add to `package.json`:
   ```json
   {
     "homepage": "https://yourusername.github.io/pokemon-card-agg"
   }
   ```

2. Install gh-pages:
   ```bash
   npm install --save-dev gh-pages
   ```

3. Add scripts to `package.json`:
   ```json
   {
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

4. Deploy:
   ```bash
   npm run deploy
   ```

## Customization

### Change Colors

Edit `src/App.js` and modify the Tailwind classes:

```javascript
// Change primary color from indigo to blue
className="bg-indigo-600"  // Change to bg-blue-600

// Change gradient
className="from-indigo-600 to-purple-600"  // Change to your colors
```

### Add Custom Fonts

1. Add to `public/index.html`:
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
   ```

2. Update `src/index.css`:
   ```css
   body {
     font-family: 'Inter', sans-serif;
   }
   ```

### Modify Tailwind Configuration

Edit `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'pokemon-yellow': '#FFCB05',
        'pokemon-blue': '#3B4CCA',
      }
    },
  },
}
```

## Environment Variables

Create `.env` in the web-frontend directory:

```
REACT_APP_API_URL=http://127.0.0.1:5000
```

Use in code:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';
```

**Note:** Restart the dev server after changing `.env`

## Browser Support

The app supports:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

For older browsers, you may need polyfills.
