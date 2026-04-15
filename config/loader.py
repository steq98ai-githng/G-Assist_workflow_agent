import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "gemini_model": "gemini-2.0-flash",
    "mcp_servers": [
        {"name": "GitKraken", "command": "npx", "args": ["-y", "@gitkraken/mcp-server"]}
    ]
}

def _validate_config(config: Dict[str, Any]) -> bool:
    """Validate config using basic checks instead of jsonschema to avoid extra dependencies."""
    if not isinstance(config.get("gemini_model"), str):
        return False
    if not isinstance(config.get("mcp_servers"), list):
        return False

    for server in config["mcp_servers"]:
        if not isinstance(server, dict):
            return False
        if not all(k in server for k in ["name", "command", "args"]):
            return False
        if not isinstance(server["args"], list):
            return False

    return True

def load_config(config_file_path: str) -> Dict[str, Any]:
    """Loads configuration from file and validates it."""
    cfg = DEFAULT_CONFIG.copy()
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r", encoding="utf-8") as f:
                loaded_cfg = json.load(f)

            # Merge and validate
            temp_cfg = cfg.copy()
            temp_cfg.update(loaded_cfg)

            if _validate_config(temp_cfg):
                cfg = temp_cfg
            else:
                logger.warning("Config validation failed, using default values where possible.")

        except Exception as e:
            logger.error(f"Config load error: {e}")

    return cfg
