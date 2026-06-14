FROM python:3.10-slim

# 安裝系統工具與 Ollama
RUN apt-get update && apt-get install -y curl zstd && \
    curl -fsSL https://ollama.ai/install.sh | sh

WORKDIR /app

# 複製所有檔案 (包含 bot.py, requirements.txt, entrypoint.sh)
COPY . .

# 安裝 Python 依賴 (對應你 .bat 裡的 pip install)
RUN pip install --no-cache-dir -r requirements.txt

# 修正 Linux 權限
RUN chmod +x entrypoint.sh

# 暴露 Hugging Face Spaces 需要的 HTTP 端口
EXPOSE 7860

# 執行啟動腳本
ENTRYPOINT ["./entrypoint.sh"]
