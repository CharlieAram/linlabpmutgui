"""Complete device configuration models."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .channel import ChannelConfig
from .beamforming import BeamformingConfig
from .pattern import PatternConfig


class ConfigMetadata(BaseModel):
    """Metadata for configuration."""
    name: str = Field(description="Configuration name")
    description: str = Field(default="", description="Configuration description")
    author: str = Field(default="", description="Author name")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Focus at 15mm center",
                "description": "Standard center focus configuration",
                "author": "Researcher Name",
                "created_at": "2025-11-14T10:30:00Z"
            }
        }


class DeviceConfig(BaseModel):
    """Complete device configuration."""
    version: str = Field(default="1.0", description="Config format version")
    device_type: str = Field(default="TX7332", description="Device type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Configuration timestamp")
    channels: list[ChannelConfig] = Field(description="Array of 32 channel configurations")
    beamforming: BeamformingConfig = Field(description="Beamforming configuration")
    pattern: PatternConfig = Field(description="Pattern configuration")
    metadata: ConfigMetadata = Field(description="Configuration metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "version": "1.0",
                "device_type": "TX7332",
                "timestamp": "2025-11-14T10:30:00Z",
                "channels": [],  # Would contain 32 channel configs
                "beamforming": {
                    "focal_point_x_mm": 0.0,
                    "focal_point_z_mm": 15.0,
                    "steering_angle_deg": 0.0,
                    "speed_of_sound": 1500,
                    "auto_calculate": True
                },
                "pattern": {
                    "pattern_type": "5.6MHz_3LVL_A",
                    "frequency_mhz": 5.6,
                    "cycles": 2,
                    "custom_hex": None,
                    "description": "5.6 MHz 3-level wave"
                },
                "metadata": {
                    "name": "Focus at 15mm center",
                    "description": "Standard configuration",
                    "author": "Researcher"
                }
            }
        }


class ConfigSaveRequest(BaseModel):
    """Request to save configuration."""
    filename: str = Field(description="Filename to save configuration")
    config: DeviceConfig = Field(description="Configuration to save")


class ConfigLoadRequest(BaseModel):
    """Request to load configuration."""
    filename: str = Field(description="Filename to load configuration from")


class ConfigListItem(BaseModel):
    """Item in configuration list."""
    filename: str = Field(description="Configuration filename")
    name: str = Field(description="Configuration name")
    description: str = Field(description="Configuration description")
    created_at: Optional[datetime] = Field(description="Creation timestamp")
    device_type: str = Field(description="Device type")


class ConfigListResponse(BaseModel):
    """List of saved configurations."""
    configs: list[ConfigListItem] = Field(description="List of saved configurations")

