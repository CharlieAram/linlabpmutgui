"""Pattern/waveform API endpoints."""
from fastapi import APIRouter, HTTPException
from backend.api.models.pattern import PatternConfig, PatternPreset, PatternListResponse
from backend.api.models.device import ApiResponse
from backend.device.controller import get_controller
from backend.services.pattern_service import PatternService


router = APIRouter(prefix="/api/patterns", tags=["patterns"])


# Current pattern configuration
_current_pattern: PatternConfig = PatternConfig(
    pattern_type="5.6MHz_3LVL_A",
    frequency_mhz=5.6,
    cycles=2,
    description="5.6 MHz 3-level wave"
)


@router.get("", response_model=PatternListResponse)
async def get_patterns():
    """Get all available pattern presets."""
    presets = PatternService.get_presets()
    return PatternListResponse(patterns=[PatternPreset(**preset) for preset in presets])


@router.get("/current", response_model=PatternConfig)
async def get_current_pattern():
    """Get current pattern configuration."""
    return _current_pattern


@router.put("/current", response_model=PatternConfig)
async def update_current_pattern(pattern: PatternConfig):
    """Update current pattern configuration."""
    global _current_pattern
    _current_pattern = pattern
    return pattern


@router.post("/apply", response_model=ApiResponse)
async def apply_pattern():
    """Apply current pattern to device."""
    controller = get_controller()
    
    try:
        if not controller.is_connected():
            raise HTTPException(status_code=400, detail="Device not connected")
        
        # Get pattern data
        if _current_pattern.custom_hex:
            # Use custom pattern
            pattern_hex = [int(h, 16) if isinstance(h, str) else h for h in _current_pattern.custom_hex]
            pattern_start_word = 0x001E  # Default
        else:
            # Use preset pattern
            preset = PatternService.get_preset_by_type(_current_pattern.pattern_type)
            if not preset:
                raise HTTPException(status_code=400, detail="Pattern type not found")
            pattern_hex = preset["pattern_hex"]
            pattern_start_word = preset["pattern_start_word"]
        
        # Disable sync before writing
        controller.enable_sync(False)
        controller.write_reg(0x08, 0x00000000)  # Disable clock sync detection
        
        # Set pattern start word for all channels (registers 0x0C to 0x13)
        for reg_index in range(0x0C, 0x14):
            controller.write_reg(
                reg_index,
                (pattern_start_word << 16) | pattern_start_word
            )
        
        # Write pattern to memory (all 16 channels, page select 0x0000FFFF)
        for i, pat in enumerate(pattern_hex):
            controller.write_reg(
                0x40 + pattern_start_word + i,
                pat,
                page_select=0x0000FFFF
            )
        
        return ApiResponse(
            success=True,
            message="Pattern applied to device",
            data={
                "pattern_type": _current_pattern.pattern_type,
                "frequency_mhz": _current_pattern.frequency_mhz,
                "pattern_words": len(pattern_hex)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying pattern: {str(e)}")


@router.post("/apply-preset/{pattern_type}", response_model=ApiResponse)
async def apply_preset_pattern(pattern_type: str):
    """Apply a preset pattern directly to device."""
    global _current_pattern
    
    preset = PatternService.get_preset_by_type(pattern_type)
    if not preset:
        raise HTTPException(status_code=404, detail="Pattern preset not found")
    
    # Update current pattern
    _current_pattern = PatternConfig(
        pattern_type=preset["pattern_type"],
        frequency_mhz=preset["frequency_mhz"],
        cycles=preset["cycles"],
        custom_hex=None,
        description=preset["description"]
    )
    
    # Apply to device
    return await apply_pattern()


@router.post("/custom", response_model=PatternConfig)
async def create_custom_pattern(pattern: PatternConfig):
    """Create and set a custom pattern."""
    if pattern.custom_hex:
        # Validate custom pattern
        pattern_hex = [int(h, 16) if isinstance(h, str) else h for h in pattern.custom_hex]
        if not PatternService.validate_custom_pattern(pattern_hex):
            raise HTTPException(status_code=400, detail="Invalid custom pattern")
    
    global _current_pattern
    _current_pattern = pattern
    return pattern

