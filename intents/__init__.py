"""
intents/ — Intent Handler 擴充點模組

架構設計：
  此模組為 G-Assist agent 的 Intent 分發系統提供標準介面。
  所有自訂 Intent Handler 必須繼承 BaseIntentHandler 並實作 handle_stream()。

擴充方式：
  1. 在此目錄建立新的 handler 模組（如 git_handler.py）
  2. 繼承 BaseIntentHandler 並實作所需方法
  3. 在 core/intent_router.py 中掛載新的 handler
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional


class AgentRequest:
    """統一的 Agent 請求格式（統一入口 I/O 契約）。"""

    __slots__ = ("user_input", "session_id", "tool_context", "timestamp")

    def __init__(
        self,
        user_input: str,
        session_id: str = "",
        tool_context: Optional[dict] = None,
        timestamp: float = 0.0,
    ) -> None:
        if not isinstance(user_input, str):
            raise TypeError(f"user_input must be str, got {type(user_input)}")
        self.user_input = user_input
        self.session_id = session_id
        self.tool_context = tool_context or {}
        self.timestamp = timestamp


class BaseIntentHandler(ABC):
    """所有 Intent Handler 的標準介面（擴充點）。

    高負載掛載點設計：
      - handle_stream()：非同步生成器，支援即時渲染與影片升頻的高頻串流輸出。
      - resolve_data_path()：NTFS Junction Point 相容的路徑解析器。

    子類別實作範例：
        class GitIntentHandler(BaseIntentHandler):
            async def handle_stream(self, request):
                yield "正在查詢 Git 狀態..."
    """

    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir

    @abstractmethod
    async def handle_stream(
        self, request: AgentRequest
    ) -> AsyncGenerator[str, None]:
        """非同步生成器，支援高頻串流輸出（影片升頻 / 即時渲染用）。

        子類別必須實作此方法，使用 yield 回傳串流片段。
        """
        yield ""  # pragma: no cover

    def resolve_data_path(self, relative: str) -> str:
        """路徑解析器：自動處理 NTFS Junction Points 與符號連結。

        使用 os.path.realpath() 而非 os.path.abspath()，確保：
          1. NTFS Junction Points（/J）的目標路徑被正確展開。
          2. 跨磁碟 Junction（如 D: → O:）不產生路徑解析錯誤。
          3. 避免 pathlib.Path.resolve(strict=True) 在 Junction 目標
             不存在時拋出 FileNotFoundError 的問題。
        """
        return os.path.realpath(os.path.join(self.data_dir, relative))


__all__ = ["AgentRequest", "BaseIntentHandler"]
