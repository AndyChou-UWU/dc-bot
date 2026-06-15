#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "🚀 subaso-俗北ㄙㄡˊ 啟動器"
echo "=================================================="

echo "[1/4] 檢查 Python 環境"
python --version

echo "[2/4] 安裝 Python 套件"
pip install -r requirements.txt

echo "[3/4] 檢查 Ollama 與模型"
if command -v ollama >/dev/null 2>&1; then
  echo "✅ 找到 Ollama，啟動本地服務..."
  ollama serve >/dev/null 2>&1 &
  sleep 5
  echo "📦 確認/下載推薦模型 Qwen2.5-1.5B..."
  ollama pull Qwen2.5-1.5B || true
else
  echo "⚠️  未偵測到 Ollama；Bot 仍可啟動，但 AI 回答需要先安裝 Ollama。"
fi

echo "[4/4] 啟動 Discord Bot"
exec python bot.py
