"""Device status and control models."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class DeviceConnectionRequest(BaseModel):
    """Request to connect to device."""
    usb_address: Optional[str] = Field(default=None, description="USB device address (auto-detect if None)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "usb_address": "FT4232 Mini Module A"
            }
        }


class DeviceStatus(BaseModel):
    """Current device status."""
    connected: bool = Field(description="Device connection status")
    device_type: str = Field(default="TX7332", description="Device type")
    usb_address: Optional[str] = Field(default=None, description="USB address")
    last_error: Optional[str] = Field(default=None, description="Last error message")
    uptime_seconds: Optional[float] = Field(default=None, description="Connection uptime in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "connected": True,
                "device_type": "TX7332",
                "usb_address": "FT4232 Mini Module A",
                "last_error": None,
                "uptime_seconds": 123.45
            }
        }


class DiagnosticResult(BaseModel):
    """Result of a diagnostic check."""
    check_name: str = Field(description="Name of the diagnostic check")
    passed: bool = Field(description="Whether the check passed")
    message: str = Field(description="Result message")
    value: Optional[str] = Field(default=None, description="Measured value if applicable")
    
    class Config:
        json_schema_extra = {
            "example": {
                "check_name": "TEMP_SHUT_ERR",
                "passed": True,
                "message": "TEMP_SHUT_ERR: PASSED",
                "value": None
            }
        }


class DiagnosticsResponse(BaseModel):
    """Complete diagnostics response."""
    timestamp: datetime = Field(default_factory=datetime.now, description="Diagnostic timestamp")
    overall_status: Literal["PASS", "FAIL", "WARNING"] = Field(description="Overall status")
    checks: list[DiagnosticResult] = Field(description="Individual diagnostic checks")
    error_count: int = Field(description="Number of failed checks")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-11-14T10:30:00Z",
                "overall_status": "PASS",
                "checks": [
                    {"check_name": "TEMP_SHUT_ERR", "passed": True, "message": "Temperature OK", "value": None}
                ],
                "error_count": 0
            }
        }


class DeviceResetRequest(BaseModel):
    """Request to reset device."""
    reset_type: Literal["hardware", "software", "memory"] = Field(default="hardware", description="Type of reset")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reset_type": "hardware"
            }
        }


class ApiResponse(BaseModel):
    """Generic API response."""
    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Response message")
    data: Optional[dict] = Field(default=None, description="Additional data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": None
            }
        }

