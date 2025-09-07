import os
from typing import Optional

class Config:
    """Configuration for Document360 MCP Server"""
    
    def __init__(self):
        self.api_key = os.getenv("DOCUMENT360_API_KEY", "")
        self.base_url = os.getenv("DOCUMENT360_BASE_URL", "https://apihub.us.document360.io")
        self.timeout = int(os.getenv("DOCUMENT360_TIMEOUT", "30"))
        self.langcode = os.getenv("DOCUMENT360_LANGCODE", "en")
        self.only_published = os.getenv("DOCUMENT360_ONLYPUBLISHED", "true")

    def validate(self) -> bool:
        """Validate configuration"""
        return bool(self.api_key and self.base_url)
    
    @property
    def headers(self) -> dict:
        """Return headers for Document360 API requests"""
        return {
            "api_token": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "Document360-MCP-Server/1.0"
        }

# Global config instance
config = Config()