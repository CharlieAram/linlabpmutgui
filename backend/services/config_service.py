"""Configuration management service."""
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class ConfigService:
    """Service for managing device configurations."""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def save_config(self, filename: str, config_data: dict) -> bool:
        """
        Save configuration to JSON file.
        
        Args:
            filename: Filename (without extension)
            config_data: Configuration dictionary
            
        Returns:
            True if successful
        """
        try:
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
            
            filepath = self.config_dir / filename
            
            # Add timestamp if not present
            if 'timestamp' not in config_data:
                config_data['timestamp'] = datetime.now().isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self, filename: str) -> Optional[dict]:
        """
        Load configuration from JSON file.
        
        Args:
            filename: Filename (with or without .json extension)
            
        Returns:
            Configuration dictionary or None if not found
        """
        try:
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
            
            filepath = self.config_dir / filename
            
            if not filepath.exists():
                return None
            
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            
            return config_data
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
    
    def list_configs(self) -> List[dict]:
        """
        List all saved configurations.
        
        Returns:
            List of configuration metadata
        """
        configs = []
        
        try:
            for filepath in self.config_dir.glob('*.json'):
                try:
                    with open(filepath, 'r') as f:
                        config_data = json.load(f)
                    
                    metadata = config_data.get('metadata', {})
                    
                    configs.append({
                        'filename': filepath.name,
                        'name': metadata.get('name', filepath.stem),
                        'description': metadata.get('description', ''),
                        'created_at': config_data.get('timestamp'),
                        'device_type': config_data.get('device_type', 'Unknown')
                    })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue
        except Exception as e:
            print(f"Error listing configs: {e}")
        
        # Sort by created_at (most recent first)
        configs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return configs
    
    def delete_config(self, filename: str) -> bool:
        """
        Delete a configuration file.
        
        Args:
            filename: Filename (with or without .json extension)
            
        Returns:
            True if successful
        """
        try:
            if not filename.endswith('.json'):
                filename = f"{filename}.json"
            
            filepath = self.config_dir / filename
            
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False

