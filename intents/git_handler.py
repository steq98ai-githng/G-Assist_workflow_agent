from __future__ import annotations

import logging
from typing import AsyncGenerator

from intents import AgentRequest, BaseIntentHandler

logger = logging.getLogger(__name__)


class GitIntentHandler(BaseIntentHandler):
    """Git 工作流的 Intent Handler。
    
    預留供未來整合 GitKraken MCP 或自訂 Git 腳本使用。
    """

    async def handle_stream(self, request: AgentRequest) -> AsyncGenerator[str, None]:
        logger.info(f"GitIntentHandler 接收到請求: {request.user_input}")
        yield "[Git Workflow] 正在查詢 Git 狀態...\n"
        yield f"處理請求：{request.user_input}\n"
        # 未來整合: mcp client calls or local git subprocess
        yield "[Git Workflow] 執行完畢。"
