"""
Configuration management for OneLogin SSO Integration
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Configuration handler for OneLogin SSO Integration"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self._config = {
            "onelogin": {
                "client_id": os.getenv("ONELOGIN_CLIENT_ID", ""),
                "client_secret": os.getenv("ONELOGIN_CLIENT_SECRET", ""),
                "region": os.getenv("ONELOGIN_REGION", "us"),
                "subdomain": os.getenv("ONELOGIN_SUBDOMAIN", "")
            },
            "saml": {
                "entity_id": "https://localhost:5000/saml/metadata",
                "acs_url": "https://localhost:5000/saml/acs",
                "sls_url": "https://localhost:5000/saml/sls"
            },
            "database": {
                "path": str(self.base_dir / "data" / "users.db")
            },
            "logging": {
                "level": "INFO",
                "file": str(self.logs_dir / "sso_integration.log")
            },
            "applications": {
                "app1": {
                    "name": "HR Management System",
                    "url": "https://hr.example.com",
                    "enabled": True
                },
                "app2": {
                    "name": "Payroll System", 
                    "url": "https://payroll.example.com",
                    "enabled": True
                },
                "app3": {
                    "name": "Employee Portal",
                    "url": "https://portal.example.com", 
                    "enabled": True
                }
            }
        }
        
        # Load configuration from file if it exists
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from JSON file"""
        config_file = self.config_dir / "saml_settings.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
                logger.info(f"Configuration loaded from {config_file}")
            except Exception as e:
                logger.warning(f"Could not load config file: {e}")
        else:
            logger.info("No config file found, using defaults")
    
    def _merge_config(self, file_config: Dict[str, Any]) -> None:
        """Merge file configuration with defaults"""
        for key, value in file_config.items():
            if key in self._config and isinstance(value, dict):
                self._config[key].update(value)
            else:
                self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_onelogin_config(self) -> Dict[str, str]:
        """Get OneLogin specific configuration"""
        return self._config.get("onelogin", {})
    
    def get_saml_config(self) -> Dict[str, str]:
        """Get SAML specific configuration"""
        return self._config.get("saml", {})
    
    def get_database_path(self) -> str:
        """Get database file path"""
        return self._config.get("database", {}).get("path", "")
    
    def get_enabled_applications(self) -> Dict[str, Dict[str, Any]]:
        """Get list of enabled applications"""
        apps = self._config.get("applications", {})
        return {k: v for k, v in apps.items() if v.get("enabled", False)}
    
    def is_configured(self) -> bool:
        """Check if minimum configuration is present"""
        onelogin_config = self.get_onelogin_config()
        required_fields = ["client_id", "client_secret", "subdomain"]
        
        return all(onelogin_config.get(field) for field in required_fields)
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate configuration and return status"""
        validation = {
            "onelogin_configured": bool(self.get("onelogin.client_id") and 
                                     self.get("onelogin.client_secret")),
            "saml_configured": bool(self.get("saml.entity_id")),
            "applications_configured": len(self.get_enabled_applications()) > 0,
            "directories_exist": all([
                self.config_dir.exists(),
                self.logs_dir.exists()
            ])
        }
        
        validation["all_configured"] = all(validation.values())
        return validation

# Global configuration instance
config = Config()