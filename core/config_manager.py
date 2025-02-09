from configparser import ConfigParser
import os
import yaml
from typing import Dict, Any

class ConfigManager:
    def __init__(self, yaml_file: str):
        self._config = {}
        self._load_config(yaml_file)
    
    def _load_config(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found at: {file_path}")
            
        try:
            with open(file_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error reading configuration file: {str(e)}")
    
    def get(self, key: str, default: str = '') -> str:
        try:
            return self._config.get(key, default)
        except:
            return default
    
    def get_section(self, section_name: str) -> dict:
        if section_name not in self._config:
            raise KeyError(f"Section '{section_name}' not found in configuration")
        return self._config[section_name]
    
    def __getattr__(self, name: str) -> str:
        return self.get(name)
    
    def as_dict(self) -> dict:
        return self._config or {}

settings= ConfigManager('../settings.yaml')