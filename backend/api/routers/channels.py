"""Channel configuration API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.api.models.channel import ChannelConfig, ChannelBulkUpdate, ChannelPreset
from backend.api.models.device import ApiResponse
from backend.device.controller import get_controller


router = APIRouter(prefix="/api/channels", tags=["channels"])


# In-memory channel state (could be persisted later)
_channel_state: List[ChannelConfig] = []


def _initialize_channel_state():
    """Initialize default channel state."""
    global _channel_state
    if not _channel_state:
        _channel_state = [
            ChannelConfig(
                channel_id=i,
                enabled=True,
                mode="TX",
                delay_cycles=0,
                delay_fractional=False,
                power_down=False
            )
            for i in range(1, 33)
        ]


@router.get("", response_model=List[ChannelConfig])
async def get_all_channels():
    """Get all channel configurations."""
    _initialize_channel_state()
    return _channel_state


@router.get("/{channel_id}", response_model=ChannelConfig)
async def get_channel(channel_id: int):
    """Get single channel configuration."""
    _initialize_channel_state()
    
    if channel_id < 1 or channel_id > 32:
        raise HTTPException(status_code=400, detail="Channel ID must be 1-32")
    
    return _channel_state[channel_id - 1]


@router.put("/{channel_id}", response_model=ChannelConfig)
async def update_channel(channel_id: int, channel: ChannelConfig):
    """Update single channel configuration."""
    _initialize_channel_state()
    
    if channel_id < 1 or channel_id > 32:
        raise HTTPException(status_code=400, detail="Channel ID must be 1-32")
    
    if channel.channel_id != channel_id:
        raise HTTPException(status_code=400, detail="Channel ID mismatch")
    
    _channel_state[channel_id - 1] = channel
    return channel


@router.put("/bulk", response_model=List[ChannelConfig])
async def update_channels_bulk(update: ChannelBulkUpdate):
    """Update multiple channels at once."""
    _initialize_channel_state()
    
    for channel in update.channels:
        if 1 <= channel.channel_id <= 32:
            _channel_state[channel.channel_id - 1] = channel
    
    return _channel_state


@router.post("/preset", response_model=List[ChannelConfig])
async def apply_preset(preset: ChannelPreset):
    """Apply a channel preset configuration."""
    _initialize_channel_state()
    
    if preset.preset == "all_tx":
        for i in range(32):
            _channel_state[i].mode = "TX"
            _channel_state[i].enabled = True
    elif preset.preset == "all_rx":
        for i in range(32):
            _channel_state[i].mode = "RX"
            _channel_state[i].enabled = True
    elif preset.preset == "half_tx_half_rx":
        for i in range(16):
            _channel_state[i].mode = "TX"
            _channel_state[i].enabled = True
        for i in range(16, 32):
            _channel_state[i].mode = "RX"
            _channel_state[i].enabled = True
    
    return _channel_state


@router.post("/apply", response_model=ApiResponse)
async def apply_channel_config():
    """Apply current channel configuration to the device."""
    controller = get_controller()
    
    try:
        if not controller.is_connected():
            raise HTTPException(status_code=400, detail="Device not connected")
        
        _initialize_channel_state()
        
        # Disable sync before writing
        controller.enable_sync(False)
        
        # Build power-down mask for disabled channels
        # Register 0x07: T/R switch and power down control
        power_down_mask = 0
        for i, channel in enumerate(_channel_state):
            if channel.power_down or not channel.enabled:
                power_down_mask |= (1 << i)
        
        # Apply power down configuration
        # Upper 16 bits: T/R switch control, Lower 16 bits: power down
        controller.write_reg(0x07, (0xFFFF << 16) | power_down_mask)
        
        # Note: TX/RX mode switching would require additional register configuration
        # This is device-specific and may need clarification from datasheet
        
        return ApiResponse(
            success=True,
            message="Channel configuration applied to device",
            data={"channels_configured": 32}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying configuration: {str(e)}")

