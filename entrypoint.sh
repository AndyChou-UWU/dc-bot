#!/usr/bin/env bash
set -euo pipefail

# 設置 UTF-8 編碼
export PYTHONIOENCODING=utf-8
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# 取得腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "🚀 subaso-俗北ㄙㄡˊ 啟動器"
echo "=================================================="
echo ""

# 檢查 Python
echo "[1/5] 檢查 Python 環境"
python --version
echo ""

# 安裝依賴
echo "[2/5] 安裝 Python 套件"
pip install -r requirements.txt -q
echo "✅ 依賴安裝完成"
echo ""

# 啟動 Ollama
echo "[3/5] 啟動 Ollama AI 引擎"
if command -v ollama >/dev/null 2>&1; then
  echo "✅ 找到 Ollama"
  echo "   🔄 啟動 Ollama 伺服器..."
  nohup ollama serve >/dev/null 2>&1 &
  OLLAMA_PID=$!
  echo "   📍 Ollama PID: $OLLAMA_PID"
  sleep 3
  echo "   📥 確認/下載推薦模型 Qwen2.5-1.5B..."
  timeout 300 ollama pull Qwen2.5-1.5B || true
  echo "   ✅ 模型準備完成"
else
  echo "⚠️  未找到 Ollama；Bot 仍可啟動，但 AI 回答需要先安裝 Ollama"
  echo "   💡 下載: https://ollama.ai"
fi
echo ""

# 啟動 GUI 監控
echo "[4/5] 啟動 GUI 監控 (後台)"
if [ -f "gui_monitor.py" ]; then
  echo "   📊 啟動 GUI 監控..."
  nohup python gui_monitor.py >/dev/null 2>&1 &
  GUI_PID=$!
  echo "   📍 GUI 監控 PID: $GUI_PID"
else
  echo "   ⚠️  gui_monitor.py 不存在，跳過 GUI"
fi
echo ""

# 啟動主 Bot
echo "[5/5] 啟動 Discord Bot (前景)"
echo "=================================================="
echo "🤖 subaso-俗北ㄙㄡˊ 正在啟動..."
echo "=================================================="
echo ""

exec python subaso_bot.py
