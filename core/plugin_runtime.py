import os
import sys
import logging
import threading
from typing import Optional

# Setup SDK Path early
_plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_libs_path = os.path.join(_plugin_dir, "libs")
if os.path.exists(_libs_path) and _libs_path not in sys.path:
    sys.path.insert(0, _libs_path)

try:
    from gassist_sdk import Plugin, Context
    from gassist_sdk.mcp import FunctionRegistry
except ImportError:
    sys.stderr.write("V2 SDK Error: ImportError occurred\n")
    sys.exit(1)

from config.loader import load_config
from mcp.client import MCPManager
from mcp.registry import discover_and_register_tools
from core.intent_router import IntentRouter

PLUGIN_NAME = "system_workflow_agent"

def _get_secure_data_dir() -> str:
    prog_data = os.environ.get("PROGRAMDATA", "")
    if prog_data:
        primary = os.path.join(prog_data, "NVIDIA Corporation", "nvtopps", "rise", "plugins", PLUGIN_NAME)
        try:
            os.makedirs(primary, exist_ok=True)
            return primary
        except Exception:
            logging.getLogger(__name__).warning("Failed to create primary directory", exc_info=True)

    fallback = os.path.join(_plugin_dir, "agent_data")
    os.makedirs(fallback, exist_ok=True)
    return fallback

class PluginRuntime:
    """Manages the lifecycle of the G-Assist plugin, avoiding global states."""
    def __init__(self):
        self.data_dir = _get_secure_data_dir()
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.log_file = os.path.join(self.data_dir, f"{PLUGIN_NAME}.log")

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        self.config = load_config(self.config_file)
        self.plugin = Plugin(name=PLUGIN_NAME, version="4.0.4", description="Professional Workflow Specialist")
        self.registry = FunctionRegistry(PLUGIN_NAME, plugin_dir=self.data_dir, source_dir=_plugin_dir)

        self.mcp_manager = MCPManager()
        self.intent_router = IntentRouter(self.config, self.mcp_manager, self.registry)

        self._setup_commands()

    def _init_background_services(self):
        def _starter():
            self.mcp_manager.start_clients(self.config.get("mcp_servers", []))
            discovered = discover_and_register_tools(self.mcp_manager, self.registry)

            if discovered:
                self.registry.save_cache()
                self.registry.update_manifest(self.plugin.version, self.plugin.description)
                self.logger.info(f"[SDK] Manifest updated with {len(discovered)} discovered functions.")

        threading.Thread(target=_starter, daemon=True).start()

    def _setup_commands(self):
        @self.plugin.command("system_workflow_agent")
        def handle_agent(user_input: str = None, context: Context = None):
            if not user_input or not user_input.strip():
                self.plugin.set_keep_session(True)
                self.plugin.stream(
                    "💠 **Antigravity DevCore System Agent v4.0.4**\n"
                    "工程指令就緒，請輸入查詢事項。\n\n"
                    "使用常見指令範例：\n"
                    "1. 「系統效能診斷」 (multi-modal vision for diagnostics)\n"
                    "2. 「Git 工作流優化」 (GitKraken MCP integration)\n"
                    "3. 「代碼自動重構分析」 (semantic code refactoring and error correction)\n"
                    "4. 「列出目前可用的工具」 (list all registered MCP tools and functions)"
                )
                return ""

            error = self.intent_router.process_query(user_input, self.plugin.stream)
            self.plugin.set_keep_session(True)
            if error:
                self.plugin.set_keep_session(False)
                return error
            return ""

    def run(self):
        self.logger.info(f"Starting Plugin Runtime for {PLUGIN_NAME}")
        self._init_background_services()
        self.plugin.run()
