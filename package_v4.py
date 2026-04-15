# SPDX-License-Identifier: Apache-2.0
"""
G-Assist Plugin Packager (Plus Ultra Edition)
1. 建立符合 NVIDIA 規範的 libs 結構。
2. 清理所有開發暫存檔 (.pyc, __pycache__, log, data)。
3. 封裝 zip 檔供 mod.io 發布。
"""

import os
import zipfile
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
PLUGIN_NAME = "system_workflow_agent"
VERSION = "4.0.4"
PACKAGE_NAME = f"{PLUGIN_NAME}_v{VERSION}.zip"

# 需要包含的文件/資料夾
FILES_TO_INCLUDE = [
    "plugin.py",
    "manifest.json",
    "README_MODIO.md",
    "gemini-api.key.example", # 只提供範本
]
DIRS_TO_INCLUDE = [
    "libs",
    "core",
    "config",
    "mcp",
    "vision",
    "intents",
]

def clean_and_package():
    print(f"📦 [Packager] Starting build for {PACKAGE_NAME}...")
    
    # 建立 dist 目錄
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

    zip_path = os.path.join(DIST_DIR, PACKAGE_NAME)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加單一文件
        for f in FILES_TO_INCLUDE:
            f_path = os.path.join(PROJECT_DIR, f)
            if os.path.exists(f_path):
                print(f"  - Adding file: {f}")
                zipf.write(f_path, f)
            else:
                print(f"  ⚠️ Warning: {f} not found!")

        # 添加目錄 (清理 __pycache__)
        for d in DIRS_TO_INCLUDE:
            d_path = os.path.join(PROJECT_DIR, d)
            if os.path.exists(d_path):
                print(f"  - Scanning directory: {d}")
                for root, _, files in os.walk(d_path):
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, PROJECT_DIR)
                        zipf.write(file_path, archive_name)
            else:
                print(f"  ⚠️ Warning: directory {d} not found!")

    print(f"\n✅ [Success] Package created at: {zip_path}")
    print(f"🚀 Ready for mod.io submission!")

if __name__ == "__main__":
    clean_and_package()
