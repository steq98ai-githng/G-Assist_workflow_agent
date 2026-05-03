"""
conftest.py — pytest 根配置

確保本地 mcp/ 目錄優先於系統安裝的 mcp 套件（C:\\Python313\\Lib\\site-packages\\mcp）。
透過 sys.path 注入解決命名空間衝突。
"""
import sys
import os

_project_root = os.path.dirname(os.path.abspath(__file__))

# 確保專案根目錄在 sys.path[0]，在任何其他 import 發生前
if _project_root in sys.path:
    sys.path.remove(_project_root)
sys.path.insert(0, _project_root)

# 清除已被系統 mcp 套件佔用的快取
for key in list(sys.modules.keys()):
    if key == "mcp" or key.startswith("mcp."):
        del sys.modules[key]
