# TX7332 PMUT Control Panel

A modern web-based GUI for controlling Texas Instruments TX7332 PMUT (Piezoelectric Micromachined Ultrasound Transducer) devices for transcranial focused ultrasound applications.

## Overview

This application provides a user-friendly interface to replace the Texas Instruments control panel, with features for:
- 32-channel configuration (TX/RX modes, delays, power control)
- Beamforming configuration (focal point, steering angle)
- Waveform pattern selection and application
- Configuration save/load functionality
- Device diagnostics and monitoring

## Architecture

- **Backend**: Python FastAPI REST API
  - Communicates with TX7332 device via FTDI USB (ftd2xx library)
  - Provides REST endpoints for all device operations
  - Reuses existing device control code from EVM_FTDI_API

- **Frontend**: React + TypeScript with Material-UI
  - Modern, responsive user interface
  - Real-time device status monitoring
  - Intuitive configuration management

## Requirements

### Hardware
- TX7332 PMUT device
- FTDI USB interface (FT4232 Mini Module or similar)
- Windows machine (tested on Windows, macOS support may vary)

### Software
- Python 3.7+ 
- Node.js 16+ and npm
- FTDI drivers installed

## Installation

### 1. Install FTDI Drivers

Download and install FTDI D2XX drivers from:
https://ftdichip.com/drivers/d2xx-drivers/

### 2. Clone Repository

```bash
cd /path/to/your/projects
git clone <repository-url>
cd linlabpmutgui
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Note: ftd2xx and numpy are the main dependencies
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
# From the backend directory
cd backend
python run.py
```

The API will start on `http://localhost:8000`
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Start Frontend Application

```bash
# From the frontend directory (in a new terminal)
cd frontend
npm run dev
```

The GUI will open in your browser at `http://localhost:5173`

## Usage Guide

### 1. Connect to Device

1. Ensure TX7332 device is connected via USB
2. Open the application in your browser
3. Click **"Connect"** button in the Device Status bar
4. The system will auto-detect the device

### 2. Configure Channels

1. Go to **"Channels & Beamforming"** tab
2. Click on any channel box to configure:
   - **Mode**: TX (transmit) or RX (receive)
   - **Delay**: Set delay in clock cycles
   - **Enable/Disable**: Turn channel on/off
   - **Power Down**: Power down specific channels
3. Use preset buttons for quick configuration:
   - **All TX**: Set all channels to transmit mode
   - **All RX**: Set all channels to receive mode
   - **Half/Half**: First 16 TX, last 16 RX
4. Click **"Apply to Device"** to send configuration to hardware

### 3. Configure Beamforming

1. In the **Beamforming Configuration** panel:
   - **Focal Point Mode**: Set X, Z coordinates (mm) for focus point
   - **Steering Angle Mode**: Set beam steering angle (-30° to +30°)
2. Choose a preset or enter custom values
3. Click **"Calculate Delays"** to preview
4. Click **"Apply to Device"** to apply beamforming

### 4. Select Waveform Pattern

1. Go to **"Pattern"** tab
2. Select pattern from dropdown:
   - 5.6 MHz 3-Level (standard)
   - 3.4 MHz 2-Level (deeper penetration)
   - Custom patterns (advanced)
3. Click **"Apply Pattern to Device"**

### 5. Save/Load Configurations

1. Go to **"Configuration"** tab
2. Click **"Save Configuration"**:
   - Enter name and description
   - Configuration includes all channel, beamforming, and pattern settings
3. Load configurations from the list
4. Export configurations as JSON files

### 6. Run Diagnostics

1. Go to **"Diagnostics"** tab
2. Click **"Run Diagnostics"**
3. View diagnostic results:
   - Temperature checks
   - Supply voltage checks
   - Clock detection
   - Error flags

## Configuration Files

Saved configurations are stored in `configs/` directory as JSON files.

Example configuration structure:
```json
{
  "version": "1.0",
  "device_type": "TX7332",
  "timestamp": "2025-11-14T10:30:00Z",
  "channels": [...],
  "beamforming": {...},
  "pattern": {...},
  "metadata": {
    "name": "Focus at 15mm center",
    "description": "Standard configuration",
    "author": "Researcher Name"
  }
}
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger/OpenAPI.

### Key Endpoints

- **Device**: `/api/device/*` - Connection, status, reset, diagnostics
- **Channels**: `/api/channels/*` - Channel configuration and presets
- **Beamforming**: `/api/beamforming/*` - Beamforming calculations and application
- **Patterns**: `/api/patterns/*` - Waveform pattern management
- **Config**: `/api/config/*` - Configuration save/load

## Troubleshooting

### Device Won't Connect

1. Check USB connection
2. Verify FTDI drivers are installed
3. Check device address in backend logs
4. Try manually specifying USB address in connection dialog

### Backend Errors

1. Check Python dependencies are installed: `pip list`
2. Verify ftd2xx library can find device: `python -c "import ftd2xx; print(ftd2xx.listDevices())"`
3. Check backend logs for detailed error messages

### Frontend Can't Reach Backend

1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify API base URL in `frontend/src/services/api.ts`

### Permission Errors (macOS/Linux)

On macOS/Linux, you may need to add FTDI permissions:
```bash
# Add user to dialout group (Linux)
sudo usermod -a -G dialout $USER

# Restart for changes to take effect
```

## Development

### Backend Development

```bash
cd backend
# Run with auto-reload
python run.py
```

The server will auto-reload on code changes.

### Frontend Development

```bash
cd frontend
# Run development server
npm run dev
```

Vite provides hot-module replacement for instant updates.

### Project Structure

```
linlabpmutgui/
├── backend/              # Python FastAPI backend
│   ├── api/             # API routes and models
│   ├── device/          # Device controller
│   ├── services/        # Business logic
│   └── requirements.txt
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json
├── EVM_FTDI_API/        # Original device code (reference)
├── BeamformingSimulation/ # Beamforming calculations
├── configs/             # Saved configurations
└── README.md
```

## Safety Notes

⚠️ **Important Safety Considerations:**

1. **High Voltage**: TX7332 can output high voltages. Ensure proper safety measures.
2. **Parameter Validation**: Always verify parameters before applying to device.
3. **Testing**: Test configurations with low power settings first.
4. **Monitoring**: Use external monitoring equipment to verify device behavior.

## Contributing

When modifying the code:

1. Backend changes: Update API documentation
2. Frontend changes: Maintain TypeScript types
3. Test with actual hardware when possible
4. Document any new features in this README

## License

[Specify your license here]

## Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation at `/docs`
3. Contact lab administrator

## Acknowledgments

- Original EVM_FTDI_API code by previous lab members
- Texas Instruments for TX7332 documentation and hardware
- Lab researchers for requirements and testing

---

**Version**: 1.0.0  
**Last Updated**: November 2025

