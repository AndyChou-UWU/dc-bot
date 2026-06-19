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
PYTHON_CMD="$(command -v python || command -v python3 || true)"
if [ -z "$PYTHON_CMD" ]; then
  echo "❌ 找不到 Python 執行檔。請先安裝 Python。"
  exit 1
fi
$PYTHON_CMD --version
echo ""

# 安裝依賴
echo "[2/5] 安裝 Python 套件"
"$PYTHON_CMD" -m pip install --upgrade pip
"$PYTHON_CMD" -m pip install -r requirements.txt -q
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
  MODEL_NAME="qwen2.5:7b-instruct"
  echo "   📥 確認/下載推薦模型 ${MODEL_NAME}..."
  if command -v timeout >/dev/null 2>&1; then
    timeout 300 ollama pull "$MODEL_NAME" || true
  else
    ollama pull "$MODEL_NAME" || true
  fi
  echo "   ✅ 模型準備完成（若無法拉取，可手動安裝或更換模型名稱）"
else
  echo "⚠️  未找到 Ollama；Bot 仍可啟動，但 AI 回答需要先安裝 Ollama"
  echo "   💡 下載: https://ollama.ai"
fi
echo ""
# 啟動 GUI 監控
echo "[4/5] 啟動 GUI 監控 (新視窗)"
if [ -f "gui_monitor.py" ]; then
  echo "   📊 啟動 GUI 監控..."
  
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "   🔧 Windows bash 環境，直接啟動 GUI 並 background 執行..."
    "$PYTHON_CMD" gui_monitor.py >/dev/null 2>&1 &
    GUI_PID=$!
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    nohup "$PYTHON_CMD" gui_monitor.py >/dev/null 2>&1 &
    GUI_PID=$!
  else
    # Linux
    nohup "$PYTHON_CMD" gui_monitor.py >/dev/null 2>&1 &
    GUI_PID=$!
  fi
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

exec "$PYTHON_CMD" subaso_bot.py
