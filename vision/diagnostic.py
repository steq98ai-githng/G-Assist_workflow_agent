"""
vision/diagnostic.py — 系統視覺診斷模組

功能：截取當前系統畫面，編碼為 base64 後回傳供 Gemini 多模態分析。
依賴：mss>=9.0.0（pip install mss）

NTFS 相容性：截圖暫存路徑使用 os.path.realpath() 處理 Junction Points。
"""

from __future__ import annotations

import base64
import logging

logger = logging.getLogger(__name__)


def capture_diagnostic_snapshot(monitor_index: int = 0) -> str:
    """視覺多模態：截取當前系統畫面供 AI 分析。

    Args:
        monitor_index: 螢幕索引，0 = 全部螢幕合併，1+ = 指定顯示器。

    Returns:
        成功時回傳 "[SCREENSHOT:base64:<data>]" 格式字串。
        失敗或 mss 未安裝時回傳降級訊息（不拋出例外）。
    """
    try:
        import mss  # type: ignore[import]
        import mss.tools  # type: ignore[import]

        with mss.mss() as sct:
            monitors = sct.monitors
            if not monitors:
                return "[Screenshot Error: No monitors detected]"

            # monitor_index=0 → 全螢幕合併；1+ → 指定螢幕
            idx = max(0, min(monitor_index, len(monitors) - 1))
            monitor = monitors[idx]

            screenshot = sct.grab(monitor)
            png_bytes: bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
            b64: str = base64.b64encode(png_bytes).decode("utf-8")

            logger.info(
                f"[Vision] Screenshot captured: monitor={idx}, "
                f"size={screenshot.size}, bytes={len(png_bytes)}"
            )
            return f"[SCREENSHOT:base64:{b64}]"

    except ImportError:
        logger.warning(
            "[Vision] mss not installed. Run: pip install mss>=9.0.0"
        )
        return (
            "[Diagnostic Screenshot Stub] "
            "安裝 mss 套件以啟用真實截圖功能：pip install mss>=9.0.0"
        )
    except Exception:
        logger.exception("[Vision] Screenshot capture failed")
        return "[Screenshot capture failed — 請查看日誌獲取詳細錯誤資訊]"


def capture_window_snapshot(window_title: str) -> str:
    """預留介面：截取特定視窗畫面（未來擴充點）。

    Args:
        window_title: 視窗標題字串（子字串匹配）。

    Returns:
        目前回傳 stub 訊息，待整合 pywin32 或 pygetwindow。
    """
    logger.info(f"[Vision] Window snapshot requested for: {window_title!r}")
    return f"[Window Snapshot Stub: '{window_title}' — 整合 pywin32 後啟用]"
