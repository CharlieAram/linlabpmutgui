"""Beamforming API endpoints."""
from fastapi import APIRouter, HTTPException
from backend.api.models.beamforming import (
    BeamformingConfig,
    BeamformingDelays,
    BeamformingPreset
)
from backend.api.models.device import ApiResponse
from backend.device.controller import get_controller
from backend.services.beamforming_service import BeamformingService


router = APIRouter(prefix="/api/beamforming", tags=["beamforming"])


# Current beamforming configuration
_current_beamforming: BeamformingConfig = BeamformingConfig()


@router.get("/config", response_model=BeamformingConfig)
async def get_beamforming_config():
    """Get current beamforming configuration."""
    return _current_beamforming


@router.put("/config", response_model=BeamformingConfig)
async def update_beamforming_config(config: BeamformingConfig):
    """Update beamforming configuration."""
    global _current_beamforming
    _current_beamforming = config
    return config


@router.post("/calculate", response_model=BeamformingDelays)
async def calculate_delays(config: BeamformingConfig):
    """Calculate delays from beamforming configuration."""
    try:
        if config.auto_calculate:
            # Calculate from focal point
            delays = BeamformingService.calculate_delays_from_focal_point(
                focal_x_mm=config.focal_point_x_mm,
                focal_z_mm=config.focal_point_z_mm,
                speed_of_sound=config.speed_of_sound
            )
        else:
            # Calculate from steering angle
            delays = BeamformingService.calculate_delays_from_angle(
                steering_angle_deg=config.steering_angle_deg,
                speed_of_sound=config.speed_of_sound
            )
        
        return BeamformingDelays(
            delays=delays,
            focal_point_x_mm=config.focal_point_x_mm,
            focal_point_z_mm=config.focal_point_z_mm,
            steering_angle_deg=config.steering_angle_deg
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@router.post("/apply", response_model=ApiResponse)
async def apply_beamforming():
    """Apply current beamforming configuration to device."""
    controller = get_controller()
    
    try:
        if not controller.is_connected():
            raise HTTPException(status_code=400, detail="Device not connected")
        
        # Calculate delays
        if _current_beamforming.auto_calculate:
            delays = BeamformingService.calculate_delays_from_focal_point(
                focal_x_mm=_current_beamforming.focal_point_x_mm,
                focal_z_mm=_current_beamforming.focal_point_z_mm,
                speed_of_sound=_current_beamforming.speed_of_sound
            )
        else:
            delays = BeamformingService.calculate_delays_from_angle(
                steering_angle_deg=_current_beamforming.steering_angle_deg,
                speed_of_sound=_current_beamforming.speed_of_sound
            )
        
        # Combine delays into register values
        combined_delays = BeamformingService.combine_channel_delays(delays)
        
        # Disable sync before writing
        controller.enable_sync(False)
        
        # Set delay start word (using TX7364 approach)
        delay_start_word = 0x0
        for reg_index in range(0x0D, 0x15):  # Registers 0x0D to 0x14
            controller.write_reg(
                reg_index,
                (delay_start_word << 16) | delay_start_word
            )
        
        # Write delay values to device
        # Delay page select: 0x00010000 (page 17 for delays)
        for index, delay_value in enumerate(combined_delays):
            reg_address = 0x40 + delay_start_word * 8 + index
            controller.write_reg(reg_address, delay_value, page_select=0x00010000)
        
        # Enable sync
        controller.enable_sync(True)
        controller.write_reg(0x08, 0x00000002)  # Enable clock sync detection
        
        return ApiResponse(
            success=True,
            message="Beamforming configuration applied",
            data={
                "focal_point_x_mm": _current_beamforming.focal_point_x_mm,
                "focal_point_z_mm": _current_beamforming.focal_point_z_mm,
                "delays_applied": len(combined_delays)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying beamforming: {str(e)}")


@router.get("/presets", response_model=list[BeamformingPreset])
async def get_beamforming_presets():
    """Get predefined beamforming presets."""
    presets = [
        BeamformingPreset(
            name="Center focus 15mm",
            config=BeamformingConfig(
                focal_point_x_mm=0.0,
                focal_point_z_mm=15.0,
                steering_angle_deg=0.0,
                speed_of_sound=1500,
                auto_calculate=True
            )
        ),
        BeamformingPreset(
            name="Center focus 20mm",
            config=BeamformingConfig(
                focal_point_x_mm=0.0,
                focal_point_z_mm=20.0,
                steering_angle_deg=0.0,
                speed_of_sound=1500,
                auto_calculate=True
            )
        ),
        BeamformingPreset(
            name="Steering +15 degrees",
            config=BeamformingConfig(
                focal_point_x_mm=0.0,
                focal_point_z_mm=15.0,
                steering_angle_deg=15.0,
                speed_of_sound=1500,
                auto_calculate=False
            )
        ),
        BeamformingPreset(
            name="Steering -15 degrees",
            config=BeamformingConfig(
                focal_point_x_mm=0.0,
                focal_point_z_mm=15.0,
                steering_angle_deg=-15.0,
                speed_of_sound=1500,
                auto_calculate=False
            )
        )
    ]
    return presets

