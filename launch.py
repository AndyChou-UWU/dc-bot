#!/usr/bin/env python3
"""
subaso Discord Bot 啟動器
跨平台啟動：Ollama + GUI 監控 + 主 Bot
"""

import os
import sys
import subprocess
import time
import threading
import platform
from pathlib import Path

# 編碼修復
os.environ['PYTHONIOENCODING'] = 'utf-8'

PROJECT_DIR = Path(__file__).parent

def print_header(text):
    """打印標題"""
    print("\n" + "=" * 50)
    print(f"🚀 {text}")
    print("=" * 50)

def print_step(step_num, total, text):
    """打印步驟"""
    print(f"\n[{step_num}/{total}] {text}")

def check_python():
    """檢查 Python 環境"""
    print_step(1, 5, "檢查 Python 環境")
    print(f"✅ Python {sys.version}")
    print(f"   位置: {sys.executable}")

def install_requirements():
    """安裝依賴"""
    print_step(2, 5, "安裝 Python 套件")
    req_file = PROJECT_DIR / "requirements.txt"
    
    if req_file.exists():
        print(f"📦 從 {req_file} 安裝依賴...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ 依賴安裝完成")
        else:
            print(f"⚠️ 安裝過程中有警告：\n{result.stderr}")
    else:
        print(f"⚠️ 找不到 requirements.txt")

def start_ollama():
    """啟動 Ollama 服務"""
    print_step(3, 5, "啟動 Ollama AI 引擎")
    
    # 檢查 Ollama 是否已安裝
    ollama_cmd = "ollama" if platform.system() != "Windows" else "ollama.exe"
    
    try:
        # 嘗試檢查 ollama 版本
        result = subprocess.run(
            [ollama_cmd, "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ 找到 Ollama: {result.stdout.decode().strip()}")
            
            # 在後台啟動 ollama serve
            print("   🔄 啟動 Ollama 伺服器...")
            if platform.system() == "Windows":
                # Windows: 使用 CREATE_NEW_CONSOLE
                subprocess.Popen(
                    [ollama_cmd, "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                )
            else:
                # Linux/Mac: 使用 nohup
                subprocess.Popen(
                    ["nohup", ollama_cmd, "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            time.sleep(3)  # 等待 Ollama 啟動
            
            # 嘗試下載模型
            print("   📥 確認/下載推薦模型 Qwen2.5-1.5B...")
            result = subprocess.run(
                [ollama_cmd, "pull", "Qwen2.5-1.5B"],
                capture_output=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"   ✅ 模型準備完成")
            else:
                print(f"   ⚠️ 模型下載可能在進行中，繼續啟動...")
        else:
            print(f"⚠️ Ollama 命令執行失敗")
            print("   💡 請先安裝 Ollama: https://ollama.ai")
    except FileNotFoundError:
        print(f"⚠️ 未找到 Ollama；Bot 仍可啟動，但 AI 回答需要先安裝 Ollama")
        print("   💡 下載: https://ollama.ai")
    except Exception as e:
        print(f"⚠️ Ollama 啟動失敗: {e}")

def start_gui():
    """啟動 GUI 監控"""
    print_step(4, 5, "啟動 GUI 監控 (後台)")
    
    gui_file = PROJECT_DIR / "gui_monitor.py"
    if gui_file.exists():
        print(f"📊 啟動 GUI 監控...")
        try:
            if platform.system() == "Windows":
                # Windows: 使用新視窗
                subprocess.Popen(
                    [sys.executable, str(gui_file)],
                    cwd=str(PROJECT_DIR),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                )
            else:
                # Linux/Mac: 使用後台程序
                subprocess.Popen(
                    [sys.executable, str(gui_file)],
                    cwd=str(PROJECT_DIR),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            print("   ✅ GUI 已在後台啟動 (新視窗)")
        except Exception as e:
            print(f"   ⚠️ GUI 啟動失敗: {e}")
    else:
        print(f"   ⚠️ gui_monitor.py 不存在，跳過 GUI")

def start_bot():
    """啟動主 Bot（前景執行）"""
    print_step(5, 5, "啟動 Discord Bot (前景)")
    
    bot_file = PROJECT_DIR / "subaso_bot.py"
    if not bot_file.exists():
        print(f"❌ 找不到 {bot_file}")
        return False
    
    print("=" * 50)
    print("🤖 subaso-俗北ㄙㄡˊ 正在啟動...")
    print("=" * 50)
    print()
    
    try:
        # 前景運行 Bot（會阻止程序）
        subprocess.run(
            [sys.executable, str(bot_file)],
            cwd=str(PROJECT_DIR)
        )
    except KeyboardInterrupt:
        print("\n\n⏹️ Bot 被用戶中斷")
    except Exception as e:
        print(f"\n❌ Bot 運行錯誤: {e}")
    
    return True

def main():
    """主啟動流程"""
    print_header("subaso-俗北ㄙㄡˊ 啟動器 v1.0")
    print(f"系統: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    try:
        # 檢查 Python
        check_python()
        
        # 安裝依賴
        install_requirements()
        
        # 啟動 Ollama（如果可用）
        start_ollama()
        
        # 啟動 GUI（後台）
        start_gui()
        
        # 啟動 Bot（前景）
        start_bot()
        
        print("\n✅ 啟動流程完成")
    except KeyboardInterrupt:
        print("\n\n⏹️ 啟動中斷")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
