import os
import sys
import json
from utils.config_loader import load_config
from langchain_google_genai import load_config
from langchain_groq import ChatGroq
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentPortalException

class ApiKeyManager:
    REQUIRED_KEYS= ["GROQ_API_KEY", "GOOGLE_API_KEY"]

    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("API_KEYS")

        """This si when trying to load them from ECS secrets"""
        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys= parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to load API keys as JSON", error=str(e))

            """When trying to load them from environment variables"""
            for key in self.REQUIRED_KEYS:
                if not self.api_keys.get(key):
                    env_val = os.getenv(key)
                    if env_val:
                        self.api_keys = env_val
                        log.info(f"loaded {key} from individual environment variable")

            #Final check
            missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
            if missing:
                log.error("Missing required API keys", missing_keys = missing)
                raise DocumentPortalException("missing API keys", sys)
            
            log.info("API keys laoded", keys={k:v[:6] +"..." for k,v in self.api_keys.items()})

    def get(self, key:str)->str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val
