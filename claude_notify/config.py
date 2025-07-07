"""Configuration management for Claude Notify"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any


def get_config_dir() -> Path:
    """Get the configuration directory path"""
    if os.name == "nt":  # Windows
        config_dir = Path(os.environ.get("APPDATA", "")) / "claude-notify"
    else:  # Unix-like (macOS, Linux)
        config_dir = Path.home() / ".config" / "claude-notify"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the configuration file path"""
    return get_config_dir() / "config.yaml"


def get_default_config() -> Dict[str, Any]:
    """Get default configuration values"""
    return {
        "timeout": 10,
        "sound": True,
        "urgency": "normal",
        "interval": 300,
        "title": "Claude needs your attention",
        "message": "Claude is waiting for your response",
        "app_name": "Claude"
    }


def load_config() -> Dict[str, Any]:
    """Load configuration from file or create default"""
    config_file = get_config_file()
    
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f) or {}
                # Merge with defaults for any missing keys
                default_config = get_default_config()
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return get_default_config()
    else:
        # Create default config
        default_config = get_default_config()
        save_config(default_config)
        return default_config


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    config_file = get_config_file()
    
    try:
        with open(config_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        print(f"Error saving config: {e}")