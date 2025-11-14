"""Beamforming calculation service."""
import sys
from pathlib import Path
import numpy as np

# Add BeamformingSimulation to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "BeamformingSimulation"))

from cal_foc_point import compute_focus_delays


class BeamformingService:
    """Service for beamforming calculations."""
    
    # Element positions for 32-channel array (from existing code)
    ELEMENT_POSITIONS = [
        -0.00182, -0.00171, -0.0016, -0.00149, -0.00138, -0.00127, -0.00116, -0.00105,
        -0.000935, -0.000825, -0.000715, -0.000605, -0.000495, -0.000385, -0.000275, -0.000165,
        0.000165, 0.000275, 0.000385, 0.000495, 0.000605, 0.000715, 0.000825, 0.000935,
        0.00105, 0.00116, 0.00127, 0.00138, 0.00149, 0.0016, 0.00171, 0.00182
    ]
    
    @staticmethod
    def calculate_delays_from_focal_point(
        focal_x_mm: float = 0.0,
        focal_z_mm: float = 15.0,
        speed_of_sound: float = 1500,
        num_elements: int = 32,
        pitch_um: float = 110,
        delay_resolution_ns: float = 4
    ) -> list[int]:
        """
        Calculate delays for focusing at a specific point.
        
        Args:
            focal_x_mm: X position of focal point in mm
            focal_z_mm: Z position (depth) of focal point in mm
            speed_of_sound: Speed of sound in medium (m/s)
            num_elements: Number of array elements
            pitch_um: Element pitch in micrometers
            delay_resolution_ns: Delay resolution in nanoseconds
            
        Returns:
            List of 32 delay values in clock cycles
        """
        delays = compute_focus_delays(
            num_elements=num_elements,
            pitch_um=pitch_um,
            focus_point_mm=(focal_x_mm, focal_z_mm),
            c=speed_of_sound,
            delay_resolution_ns=delay_resolution_ns
        )
        
        return delays.tolist()
    
    @staticmethod
    def calculate_delays_from_angle(
        steering_angle_deg: float = 0.0,
        speed_of_sound: float = 1500,
        frequency_hz: float = 5.6e6
    ) -> list[int]:
        """
        Calculate delays for steering beam at a specific angle.
        
        Args:
            steering_angle_deg: Steering angle in degrees (-30 to +30)
            speed_of_sound: Speed of sound in medium (m/s)
            frequency_hz: Operating frequency in Hz
            
        Returns:
            List of 32 delay values in clock cycles
        """
        wavelength = speed_of_sound / frequency_hz
        angle_rad = np.deg2rad(steering_angle_deg)
        
        delays = []
        for pos in BeamformingService.ELEMENT_POSITIONS:
            # Calculate time delay for plane wave steering
            delay_time = pos * np.sin(angle_rad) / speed_of_sound
            # Convert to clock cycles (assuming 250 MHz clock = 4ns period)
            delay_cycles = int(np.round(delay_time / 4e-9))
            delays.append(max(0, delay_cycles))  # Ensure non-negative
        
        # Normalize to minimum delay
        min_delay = min(delays)
        delays = [d - min_delay for d in delays]
        
        return delays
    
    @staticmethod
    def encode_delay_to_hex(delay_cycles: int, fractional: bool = False) -> int:
        """
        Encode delay cycles to hex format for device.
        
        Args:
            delay_cycles: Number of delay cycles (0-16383)
            fractional: Whether to add 0.5 cycle delay
            
        Returns:
            Encoded hex value
        """
        # Delay format: [15]=0, [14]=FRAC_DEL, [13:0]=DEL
        value = delay_cycles & 0x3FFF
        if fractional:
            value |= 0x4000
        return value
    
    @staticmethod
    def combine_channel_delays(delays: list[int]) -> list[int]:
        """
        Combine pairs of channel delays into register values.
        Each register contains delays for 2 channels.
        
        Args:
            delays: List of 32 delay values
            
        Returns:
            List of 16 register values (pairs combined)
        """
        if len(delays) != 32:
            raise ValueError("Must provide exactly 32 delay values")
        
        combined = []
        for i in range(0, 32, 2):
            # Each register: [31:16] = even channel, [15:0] = odd channel
            # Based on TX7364 format: ch(2N-1), ch(2N)
            delay_odd = BeamformingService.encode_delay_to_hex(delays[i])
            delay_even = BeamformingService.encode_delay_to_hex(delays[i + 1])
            combined_value = (delay_even << 16) | delay_odd
            combined.append(combined_value)
        
        return combined

