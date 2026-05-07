from __future__ import annotations

import logging
from typing import AsyncGenerator

from intents import AgentRequest, BaseIntentHandler

logger = logging.getLogger(__name__)


class SystemIntentHandler(BaseIntentHandler):
    """系統診斷工作流的 Intent Handler。
    
    預留供未來進行系統檢查、硬體監控及效能診斷使用。
    """

    async def handle_stream(self, request: AgentRequest) -> AsyncGenerator[str, None]:
        logger.info(f"SystemIntentHandler 接收到請求 (長度: {len(request.user_input)})")
        logger.debug(f"SystemIntentHandler 請求內容: {request.user_input}")
        yield "[System Diagnostic] 正在啟動系統診斷...\n"
        yield f"處理請求：{request.user_input}\n"
        # 未來整合: wmi, psutil 或其他系統層級的診斷指令
        yield "[System Diagnostic] 診斷完畢。"
