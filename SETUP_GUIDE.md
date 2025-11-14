# Quick Setup Guide

## Prerequisites Checklist

- [ ] TX7332 device connected via USB
- [ ] FTDI D2XX drivers installed
- [ ] Python 3.7+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed

## Step-by-Step Setup

### 1. Install FTDI Drivers (Windows)

1. Download from: https://ftdichip.com/drivers/d2xx-drivers/
2. Choose "Windows" → "setup executable"
3. Run installer and restart computer

### 2. Verify Device Connection

1. Open Device Manager (Windows)
2. Look for "Universal Serial Bus controllers" → "FT4232 Mini Module"
3. Note the COM port number

### 3. Install Backend

```bash
# Open Command Prompt or Terminal
cd C:\path\to\linlabpmutgui\backend

# Install Python dependencies
pip install -r requirements.txt

# Test installation
python -c "import ftd2xx; print('FTDI OK')"
```

### 4. Install Frontend

```bash
# Open new Command Prompt or Terminal
cd C:\path\to\linlabpmutgui\frontend

# Install Node dependencies
npm install
```

### 5. Start Application

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

Wait for message: "Application startup complete"

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Browser should open automatically to http://localhost:5173

### 6. First Connection

1. Click **"Connect"** button
2. Device should connect automatically
3. Green "Connected" status indicates success

## Quick Test

1. **Connect**: Click "Connect" button → Should show "Connected"
2. **Channels**: Go to "Channels & Beamforming" → Click "All TX" → Click "Apply to Device"
3. **Pattern**: Go to "Pattern" tab → Select "5.6 MHz 3-Level" → Click "Apply Pattern"
4. **Diagnostics**: Go to "Diagnostics" tab → Click "Run Diagnostics" → Should show "PASS"

## Common Issues

### "No instrument" Error

**Problem**: Backend can't find device  
**Solution**:
1. Check USB connection
2. Restart device
3. Try different USB port
4. Reinstall FTDI drivers

### "Connection refused" Error

**Problem**: Frontend can't reach backend  
**Solution**:
1. Check backend is running (should show "Application startup complete")
2. Check URL: http://localhost:8000/health (should return {"status": "healthy"})
3. Restart backend

### Port Already in Use

**Problem**: Port 8000 or 5173 is busy  
**Solution**:
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Then restart backend
```

## Getting Help

1. Check browser console (F12) for errors
2. Check backend terminal for error messages
3. Review `README.md` for detailed documentation
4. Check API docs at http://localhost:8000/docs

## Next Steps

Once setup is complete:
1. Read the Usage Guide in `README.md`
2. Try the example configurations
3. Save your first configuration
4. Review safety notes before production use

---

**Setup Time**: ~15-20 minutes  
**Difficulty**: Beginner-friendly

