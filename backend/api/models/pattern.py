"""Pattern/waveform configuration models."""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class PatternConfig(BaseModel):
    """Pattern/waveform configuration."""
    pattern_type: str = Field(description="Pattern identifier")
    frequency_mhz: float = Field(ge=0.1, le=10.0, description="Frequency in MHz")
    cycles: int = Field(ge=1, le=100, default=2, description="Number of cycles")
    custom_hex: Optional[list[str]] = Field(default=None, description="Custom hex pattern values")
    description: str = Field(default="", description="Pattern description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pattern_type": "5.6MHz_3LVL_A",
                "frequency_mhz": 5.6,
                "cycles": 2,
                "custom_hex": None,
                "description": "5.6 MHz 3-level wave"
            }
        }


class PatternPreset(BaseModel):
    """Predefined pattern configuration."""
    name: str = Field(description="Preset name")
    pattern_type: str = Field(description="Pattern type identifier")
    frequency_mhz: float = Field(description="Frequency in MHz")
    cycles: int = Field(description="Number of cycles")
    pattern_hex: list[int] = Field(description="Hex values for pattern")
    description: str = Field(description="Pattern description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "5.6 MHz 3-Level A",
                "pattern_type": "5.6MHz_3LVL_A",
                "frequency_mhz": 5.6,
                "cycles": 2,
                "pattern_hex": [0x00020002, 0x0000B5B1],
                "description": "Standard 5.6 MHz 3-level waveform"
            }
        }


class PatternListResponse(BaseModel):
    """List of available patterns."""
    patterns: list[PatternPreset] = Field(description="Available pattern presets")

