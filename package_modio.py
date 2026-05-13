"""
打包成 NVIDIA mod.io 格式的外掛發布包
用法: python package_modio.py
產出物: ai_chinese_mode_v3.zip
"""

import os
import shutil
import zipfile

def create_package():
    print("📦 開始打包 [G-Assist 中文版 v3.0 Agentic MCP]")
    
    src_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(src_dir, "dist")
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    zip_filename = os.path.join(dist_dir, "ai_chinese_mode_v3.zip")
    
    # 允許放入 ZIP 的檔案與資料夾
    include_files = [
        "plugin.py",
        "manifest.json",
        "requirements.txt",
        "README_USER.md",
        "README_MODIO.md",
    ]
    include_dirs = ["libs"]
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in include_files:
            item_path = os.path.join(src_dir, item)
            if os.path.exists(item_path):
                print(f"  加入: {item}")
                zipf.write(item_path, arcname=item)
        
        for d in include_dirs:
            dir_path = os.path.join(src_dir, d)
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    # 過濾快取與編譯檔
                    # 透過修改 dirs 列表來避免進入不必要的子目錄 (Performance Optimization)
                    for skip_dir in ["__pycache__", ".pytest_cache"]:
                        if skip_dir in dirs:
                            dirs.remove(skip_dir)
                        
                    for file in files:
                        if file.endswith((".pyc", ".pyo")):
                            continue
                            
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, src_dir)
                        print(f"  加入: {arcname}")
                        zipf.write(file_path, arcname=arcname)
                        
    print(f"✅ 打包成功: {zip_filename}")
    print("你可以直接上傳此 ZIP 至 NVIDIA mod.io 社群平台。")

if __name__ == "__main__":
    create_package()
