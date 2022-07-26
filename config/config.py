from typing import Any, Dict
from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    jwt_secret: SecretStr = Field(..., env="JWT_SECRET")
    user_agent: SecretStr = Field(..., env="USER_AGENT")
    path_file: SecretStr = Field(..., env="PATH_FILE")
    
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
    
      
    class Config:
        env_file = '.env'