"""Device control API endpoints."""
from fastapi import APIRouter, HTTPException
from backend.api.models.device import (
    DeviceConnectionRequest,
    DeviceStatus,
    DeviceResetRequest,
    DiagnosticsResponse,
    DiagnosticResult,
    ApiResponse
)
from backend.device.controller import get_controller
from backend.services.diagnostics_service import DiagnosticsService
from datetime import datetime


router = APIRouter(prefix="/api/device", tags=["device"])


@router.post("/connect", response_model=DeviceStatus)
async def connect_device(request: DeviceConnectionRequest):
    """Connect to the TX7332 device."""
    controller = get_controller()
    
    try:
        success = controller.connect(request.usb_address)
        
        if success:
            return DeviceStatus(
                connected=True,
                device_type="TX7332",
                usb_address=controller.usb_address,
                last_error=None,
                uptime_seconds=0
            )
        else:
            return DeviceStatus(
                connected=False,
                device_type="TX7332",
                usb_address=None,
                last_error=controller.last_error,
                uptime_seconds=None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")


@router.post("/disconnect", response_model=ApiResponse)
async def disconnect_device():
    """Disconnect from the device."""
    controller = get_controller()
    
    try:
        success = controller.disconnect()
        return ApiResponse(
            success=success,
            message="Device disconnected" if success else "Failed to disconnect",
            data=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disconnection error: {str(e)}")


@router.get("/status", response_model=DeviceStatus)
async def get_device_status():
    """Get current device status."""
    controller = get_controller()
    
    return DeviceStatus(
        connected=controller.is_connected(),
        device_type="TX7332",
        usb_address=controller.usb_address,
        last_error=controller.last_error,
        uptime_seconds=controller.get_uptime()
    )


@router.post("/reset", response_model=ApiResponse)
async def reset_device(request: DeviceResetRequest):
    """Reset the device."""
    controller = get_controller()
    
    try:
        if not controller.is_connected():
            raise HTTPException(status_code=400, detail="Device not connected")
        
        if request.reset_type == "hardware":
            controller.hardware_reset()
            message = "Hardware reset completed"
        elif request.reset_type == "software":
            controller.software_reset()
            message = "Software reset completed"
        elif request.reset_type == "memory":
            controller.memory_reset()
            message = "Memory reset completed"
        else:
            raise HTTPException(status_code=400, detail="Invalid reset type")
        
        return ApiResponse(
            success=True,
            message=message,
            data={"reset_type": request.reset_type}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset error: {str(e)}")


@router.post("/diagnostics", response_model=DiagnosticsResponse)
async def run_diagnostics():
    """Run device diagnostics."""
    controller = get_controller()
    
    try:
        if not controller.is_connected():
            raise HTTPException(status_code=400, detail="Device not connected")
        
        diagnostics_service = DiagnosticsService(controller)
        overall_status, checks = diagnostics_service.run_diagnostics()
        
        error_count = sum(1 for check in checks if not check["passed"])
        
        return DiagnosticsResponse(
            timestamp=datetime.now(),
            overall_status=overall_status,
            checks=[DiagnosticResult(**check) for check in checks],
            error_count=error_count
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostics error: {str(e)}")

