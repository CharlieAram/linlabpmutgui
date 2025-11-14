"""Pattern/waveform management service."""
from typing import List, Dict


class PatternService:
    """Service for managing waveform patterns."""
    
    # Predefined patterns based on existing config files
    PRESET_PATTERNS = {
        "5.6MHz_3LVL_A": {
            "name": "5.6 MHz 3-Level A",
            "pattern_type": "5.6MHz_3LVL_A",
            "frequency_mhz": 5.6,
            "cycles": 2,
            "pattern_hex": [0x00020002, 0x0000B5B1],
            "pattern_start_word": 0x001E,
            "description": "Standard 5.6 MHz 3-level waveform. "
                          "Under 250MHz clock, each transition = 22 cycles. "
                          "0xB1: 22 cycles PHV (positive high voltage), "
                          "0xB5: 22 cycles MHV (negative high voltage)"
        },
        "5.6MHz_3LVL_extended": {
            "name": "5.6 MHz 3-Level Extended",
            "pattern_type": "5.6MHz_3LVL_extended",
            "frequency_mhz": 5.6,
            "cycles": 2,
            "pattern_hex": [0xB5B10100, 0xC8C80500, 0x0000FF00],
            "pattern_start_word": 0x001E,
            "description": "Extended 5.6 MHz with guard bands. "
                          "Includes GND transitions for safety."
        },
        "3.4MHz_2LVL_A": {
            "name": "3.4 MHz 2-Level A",
            "pattern_type": "3.4MHz_2LVL_A",
            "frequency_mhz": 3.4,
            "cycles": 2,
            "pattern_hex": [0x31F90300, 0x050035FD, 0xFF00C8C8],
            "pattern_start_word": 0x001E,
            "description": "3.4 MHz 2-level waveform. "
                          "250MHz / (2*37) = 3.38 MHz. "
                          "Uses PHV and MHV levels only."
        },
        "test_glitch": {
            "name": "Test Glitch Pattern",
            "pattern_type": "test_glitch",
            "frequency_mhz": 0,
            "cycles": 0,
            "pattern_hex": [0xA0A00000],
            "pattern_start_word": 0x001E,
            "description": "Test pattern for T/R switch glitch testing"
        }
    }
    
    @staticmethod
    def get_presets() -> List[Dict]:
        """
        Get all available pattern presets.
        
        Returns:
            List of pattern preset dictionaries
        """
        return list(PatternService.PRESET_PATTERNS.values())
    
    @staticmethod
    def get_preset_by_type(pattern_type: str) -> Dict:
        """
        Get a specific pattern preset.
        
        Args:
            pattern_type: Pattern type identifier
            
        Returns:
            Pattern preset dictionary or None
        """
        return PatternService.PRESET_PATTERNS.get(pattern_type)
    
    @staticmethod
    def validate_custom_pattern(pattern_hex: List[int]) -> bool:
        """
        Validate a custom pattern.
        
        Args:
            pattern_hex: List of hex values
            
        Returns:
            True if valid
        """
        if not pattern_hex or len(pattern_hex) == 0:
            return False
        
        # Check that all values are valid 32-bit integers
        for val in pattern_hex:
            if not isinstance(val, int) or val < 0 or val > 0xFFFFFFFF:
                return False
        
        return True
    
    @staticmethod
    def create_custom_pattern(
        frequency_mhz: float,
        cycles: int,
        pattern_hex: List[int],
        description: str = ""
    ) -> Dict:
        """
        Create a custom pattern configuration.
        
        Args:
            frequency_mhz: Frequency in MHz
            cycles: Number of cycles
            pattern_hex: List of hex pattern values
            description: Pattern description
            
        Returns:
            Custom pattern dictionary
        """
        return {
            "name": f"Custom {frequency_mhz} MHz",
            "pattern_type": "custom",
            "frequency_mhz": frequency_mhz,
            "cycles": cycles,
            "pattern_hex": pattern_hex,
            "pattern_start_word": 0x001E,  # Default start word
            "description": description or f"Custom pattern at {frequency_mhz} MHz"
        }

