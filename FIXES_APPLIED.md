# Fixes Applied

## Issues Resolved

### 1. Port Conflict (Port 5000)
**Problem:** Port 5000 was already in use by macOS AirPlay Receiver

**Solution:** Changed Flask backend to use port 5001

**Files Modified:**
- `api/app.py` - Changed port from 5000 to 5001
- `frontend/vite.config.ts` - Updated proxy to point to 5001
- `start_webapp.sh` - Updated port references
- `start_webapp.bat` - Updated port references
- `WEB_APP_README.md` - Updated documentation
- `WEBAPP_QUICKSTART.md` - Updated documentation

### 2. Tailwind CSS v4 PostCSS Configuration
**Problem:** Tailwind CSS v4 uses a separate PostCSS plugin package

**Solution:** Installed `@tailwindcss/postcss` and updated configuration

**Changes Made:**
- Installed `@tailwindcss/postcss` package
- Updated `frontend/postcss.config.js` to use `@tailwindcss/postcss`
- Updated `frontend/src/index.css` to use `@import "tailwindcss";` (v4 syntax)

## How to Run Now

The application now runs on:
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:5001

### Quick Start

```bash
./start_webapp.sh        # Mac/Linux
start_webapp.bat         # Windows
```

Or manually:

**Terminal 1 - Backend:**
```bash
python api/app.py
# Runs on http://localhost:5001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

## Verification

After starting both servers, you should see:
1. Backend console showing "Model loaded successfully"
2. Frontend showing Vite dev server at http://localhost:5173
3. No errors about port conflicts or PostCSS

Open http://localhost:5173 in your browser to use the app!

## Alternative: If Port 5001 is Also Busy

Edit `api/app.py` line 164 and change to any free port (e.g., 5002):
```python
app.run(debug=True, host='0.0.0.0', port=5002)
```

Then update `frontend/vite.config.ts` line 9:
```typescript
target: 'http://localhost:5002',
```

## Alternative: Disable macOS AirPlay Receiver

If you prefer to use port 5000:
1. Open System Settings
2. Go to General → AirDrop & Handoff
3. Turn off "AirPlay Receiver"
4. Revert the port changes back to 5000
