#!/bin/bash
set -euo pipefail

echo "--- 啟動簡易健康檢查服務 ---"
python -m http.server 7860 >/dev/null 2>&1 &

if command -v ollama >/dev/null 2>&1; then
  echo "--- 檢測到 Ollama，啟動本地模型服務 ---"
  ollama serve >/dev/null 2>&1 &
  sleep 5
  echo "--- 正在確認/下載模型 ---"
  ollama pull Qwen2.5-1.5B || true
else
  echo "⚠️  未偵測到 Ollama；將直接啟動 Bot，但 AI 回答功能需在環境中安裝 Ollama 後再使用。"
fi

echo "--- 正在啟動 Discord Bot ---"
exec python bot.py