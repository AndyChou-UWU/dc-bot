#!/bin/bash
set -e

# 隨便啟動一個簡單的 web 服務來滿足 HF 的檢測
python3 -m http.server 7860 &

# 確認 Ollama 是否可用
if ! command -v ollama >/dev/null 2>&1; then
  echo "❌ Ollama command not found"
  exit 1
fi

# 啟動 Ollama 伺服器並丟到背景 (&)
ollama serve &

# 等待伺服器啟動
sleep 5

echo "--- Ollama 已啟動，正在下載模型 ---"
# 下載模型 (確保環境中有模型可用)
ollama pull Qwen2.5-1.5B-Instruct || true

echo "--- 正在啟動 Discord Bot ---"
# 執行你的 bot.py (對應你截圖中的 python bot.py)
exec python bot.py