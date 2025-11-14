"""Beamforming configuration models."""
from pydantic import BaseModel, Field
from typing import Optional


class BeamformingConfig(BaseModel):
    """Beamforming configuration."""
    focal_point_x_mm: float = Field(default=0.0, description="X position in mm")
    focal_point_z_mm: float = Field(default=15.0, ge=0, description="Z position (depth) in mm")
    steering_angle_deg: float = Field(default=0.0, ge=-30, le=30, description="Steering angle in degrees")
    speed_of_sound: float = Field(default=1500, ge=1000, le=2000, description="Speed of sound in m/s")
    auto_calculate: bool = Field(default=True, description="Auto-calculate delays from focal point")
    
    class Config:
        json_schema_extra = {
            "example": {
                "focal_point_x_mm": 0.0,
                "focal_point_z_mm": 15.0,
                "steering_angle_deg": 0.0,
                "speed_of_sound": 1500,
                "auto_calculate": True
            }
        }


class BeamformingDelays(BaseModel):
    """Calculated beamforming delays."""
    delays: list[int] = Field(description="Array of 32 delay values in clock cycles")
    focal_point_x_mm: float
    focal_point_z_mm: float
    steering_angle_deg: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "delays": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 
                          75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0],
                "focal_point_x_mm": 0.0,
                "focal_point_z_mm": 15.0,
                "steering_angle_deg": 0.0
            }
        }


class BeamformingPreset(BaseModel):
    """Predefined beamforming configuration."""
    name: str = Field(description="Preset name")
    config: BeamformingConfig = Field(description="Beamforming configuration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Center focus 15mm",
                "config": {
                    "focal_point_x_mm": 0.0,
                    "focal_point_z_mm": 15.0,
                    "steering_angle_deg": 0.0,
                    "speed_of_sound": 1500,
                    "auto_calculate": True
                }
            }
        }

