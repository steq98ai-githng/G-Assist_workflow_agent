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
        if not isinstance(server["args"], list) or not all(isinstance(a, str) for a in server["args"]):
            return False

    return True

def load_config(config_file_path: str) -> Dict[str, Any]:
    """Loads configuration from file and validates it.

    mcp_servers 合併策略（深層合併）：
      - 使用者設定的 server（按 name）覆蓋對應的預設值。
      - 使用者未設定的預設 server 保留。
      - 防止淺層 update() 意外清除所有預設伺服器。
    """
    cfg = {k: (list(v) if isinstance(v, list) else v)
           for k, v in DEFAULT_CONFIG.items()}

    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, "r", encoding="utf-8") as f:
                loaded_cfg = json.load(f)

            # 深層合併：mcp_servers 按 name 合併，其餘欄位直接覆蓋
            temp_cfg = cfg.copy()
            temp_cfg.update({k: v for k, v in loaded_cfg.items()
                             if k != "mcp_servers"})

            if "mcp_servers" in loaded_cfg and isinstance(
                loaded_cfg["mcp_servers"], list
            ):
                user_servers: Dict[str, Dict] = {
                    s["name"]: s for s in loaded_cfg["mcp_servers"]
                    if isinstance(s, dict) and "name" in s
                }
                # 從預設開始，使用者設定覆蓋同名項，新增項追加
                merged: list = []
                for default_s in cfg.get("mcp_servers", []):
                    name = default_s.get("name")
                    merged.append(user_servers.pop(name, default_s))
                merged.extend(user_servers.values())  # 使用者新增的伺服器
                temp_cfg["mcp_servers"] = merged

            if _validate_config(temp_cfg):
                cfg = temp_cfg
            else:
                logger.warning("Config validation failed, using default values where possible.")

        except Exception:
            logger.error("Config load error", exc_info=True)

    return cfg
