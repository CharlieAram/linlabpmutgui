"""Channel configuration models."""
from pydantic import BaseModel, Field
from typing import Literal


class ChannelConfig(BaseModel):
    """Configuration for a single channel."""
    channel_id: int = Field(ge=1, le=32, description="Channel ID (1-32)")
    enabled: bool = Field(default=True, description="Channel enabled/disabled")
    mode: Literal["TX", "RX"] = Field(default="TX", description="Transmit or Receive mode")
    delay_cycles: int = Field(ge=0, le=16383, default=0, description="Delay in clock cycles (0-16383)")
    delay_fractional: bool = Field(default=False, description="Add 0.5 cycle delay")
    power_down: bool = Field(default=False, description="Power down this channel")

    class Config:
        json_schema_extra = {
            "example": {
                "channel_id": 1,
                "enabled": True,
                "mode": "TX",
                "delay_cycles": 100,
                "delay_fractional": False,
                "power_down": False
            }
        }


class ChannelBulkUpdate(BaseModel):
    """Bulk update for multiple channels."""
    channels: list[ChannelConfig] = Field(description="List of channel configurations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "channels": [
                    {"channel_id": 1, "enabled": True, "mode": "TX", "delay_cycles": 0, "delay_fractional": False, "power_down": False},
                    {"channel_id": 2, "enabled": True, "mode": "TX", "delay_cycles": 10, "delay_fractional": False, "power_down": False}
                ]
            }
        }


class ChannelPreset(BaseModel):
    """Quick preset for channel configuration."""
    preset: Literal["all_tx", "all_rx", "half_tx_half_rx", "custom"] = Field(description="Preset type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "preset": "all_tx"
            }
        }

