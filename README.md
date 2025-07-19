# MPD Stream Player - Vercel Deployment

A web-based MPD (MPEG-DASH) stream player with CORS proxy support, optimized for Vercel hosting.

## Features

- 🎬 Plays MPD/DASH streams with DRM support
- 🔄 CORS proxy for HTTP streams
- 📱 Responsive design for all devices
- 🚀 Serverless deployment on Vercel
- 🌐 Cross-device access from anywhere

## Deployment to Vercel

### Option 1: Deploy with Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Navigate to your project folder** in PowerShell:
   ```powershell
   cd "c:\Users\Harrold\Downloads\Local Stream - Copy"
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project? `N` (for new deployment)
   - Project name: `mpd-stream-player` (or your preferred name)
   - Directory: `./` (current directory)
   - Deploy: `Y`

4. **Your app will be live** at the URL provided (e.g., `https://mpd-stream-player.vercel.app`)

### Option 2: Deploy via GitHub + Vercel Dashboard

1. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `mpd-stream-player`)

2. **Push your code to GitHub**:
   ```powershell
   cd "c:\Users\Harrold\Downloads\Local Stream - Copy"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/mpd-stream-player.git
   git push -u origin main
   ```

3. **Deploy on Vercel**:
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Import your GitHub repository
   - Click "Deploy"

## File Structure

```
├── index.html              # Main player interface (Vercel optimized)
├── mpd-player.html         # Original local version
├── api/
│   └── proxy.js           # Serverless function for CORS proxy
├── vercel.json            # Vercel configuration
├── package.json           # Project metadata
└── README.md              # This file
```

## How It Works

### Stream Handling
- **Stream 1 (HTTPS)**: Direct access without proxy
- **Stream 2 (HTTP)**: Routed through `/api/proxy` serverless function

### CORS Proxy
The serverless function at `/api/proxy.js`:
- Handles HTTP streams that would otherwise be blocked by CORS
- Forwards requests with appropriate headers
- Maintains streaming performance

### URLs After Deployment
- **Main Player**: `https://your-app.vercel.app/`
- **Original Local Version**: `https://your-app.vercel.app/mpd-player.html`
- **Proxy API**: `https://your-app.vercel.app/api/proxy?url=STREAM_URL`

## Using on Other Devices

Once deployed to Vercel, you can access your stream player from:
- 📱 **Mobile phones** (iOS/Android)
- 💻 **Other computers**
- 📺 **Smart TVs with browsers**
- 🌐 **Any device with internet access**

Just navigate to your Vercel URL: `https://your-app-name.vercel.app`

## Local Testing (Optional)

To test locally before deployment:

```bash
# Install Vercel CLI
npm install -g vercel

# Run local development server
vercel dev
```

Access at `http://localhost:3000`

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure `package.json` exists
   - Run `npm install` if needed

2. **CORS errors on HTTP streams**:
   - The proxy should handle this automatically
   - Check browser console for proxy errors

3. **Streams not loading**:
   - Verify stream URLs are still active
   - Check if the content provider has changed URLs

### Browser Compatibility
- ✅ Chrome 70+
- ✅ Firefox 65+
- ✅ Safari 12+
- ✅ Edge 79+

## Security Notes

- DRM keys are embedded in the client code (not secure for production)
- For production use, implement server-side key management
- The proxy forwards all headers, consider adding filtering for production

## Original Local Files

The original Python-based local server files are preserved:
- `cors-proxy-server.py` - Original Python CORS proxy
- `simple-server.py` - Simple Python HTTP server
- `start-server.bat` - Windows batch file launcher

These are not used in the Vercel deployment but kept for reference.
