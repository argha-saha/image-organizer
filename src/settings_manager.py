import json
from pathlib import Path

class SettingsManager:
    def __init__(self, settings_path: str):
        self.settings_path = Path(settings_path)
        
        
    def load_settings(self) -> dict:
        """Load settings from JSON file"""
        try:
            if self.settings_path.exists():
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading settings: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        return {
            "source_folder": "",
            "destination_folder": "",
            "prefix": "",
            "extension": "",
            "appearance_mode": "System",
            "retain_fields": True
        }
        
    
    def save_settings(self, settings: dict) -> bool:
        """Save settings to JSON file"""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False