#!/usr/bin/env python3
"""
后台运行脚本 - 使用 screen 或 nohup 在 Linux/Mac 上运行
"""
import subprocess
import sys
import os

def run_bot():
    """运行 Bot"""
    print("🚀 启动 Discord AI Bot...")
    print("📝 日志将保存到 logs/ 文件夹")
    print()
    
    # 启动 Bot
    subprocess.run([sys.executable, "bot.py"])

if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n✋ Bot 已停止")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
