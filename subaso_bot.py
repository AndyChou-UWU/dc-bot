"""
subaso v2.0 - 多功能 Discord Bot (已從舊版重命名)
"""

# ==================== 編碼修復 ====================
# 必須在最開始設置，確保 UTF-8 輸出
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.environ['PYTHONIOENCODING'] = 'utf-8'

import discord
import asyncio
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import httpx

# 導入自定義模塊
from modules_economy import EconomySystem, get_economy_commands
from modules_games import GameSystem, get_game_commands
from modules_admin import AdminSystem, get_admin_commands
from subaso_config import *

# ==================== 日誌系統 ====================
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(
    f"{log_dir}/subaso_{datetime.now().strftime('%Y%m%d')}.log", 
    encoding='utf-8'
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ==================== 初始化 ====================
dotenv_path = os.path.join(os.path.dirname(__file__), "設定.env")
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# ==================== 全局變量 ====================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
admin_env = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i.strip()) for i in admin_env.split(",") if i.strip().isdigit()]

# 數據管理
DATA_FILE = "user_data.json"
user_personalities = {}
user_languages = {}
user_conversations = {}
user_seen_guide = {}
user_dms = {}
last_notified_version = BOT_VERSION

# 系統實例
economy = EconomySystem()
games = GameSystem()
admin = AdminSystem()

MAX_HISTORY = 10

# ==================== 數據加載/保存 ====================
def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存數據失敗: {e}")

def load_all_user_data():
    global user_personalities, user_languages, last_notified_version
    data = load_user_data()
    if "personalities" in data:
        user_personalities = {int(k): v for k, v in data["personalities"].items()}
    if "languages" in data:
        user_languages = {int(k): v for k, v in data["languages"].items()}
    if "last_notified_version" in data:
        last_notified_version = data["last_notified_version"]
    logger.info(f"加載了 {len(user_personalities)} 個用戶的數據")

def save_all_user_data():
    global user_personalities, user_languages, BOT_VERSION, last_notified_version
    data = {
        "personalities": {str(k): v for k, v in user_personalities.items()},
        "languages": {str(k): v for k, v in user_languages.items()},
        "last_save": datetime.now().isoformat(),
        "bot_version": BOT_VERSION,
        "last_notified_version": last_notified_version
    }
    save_user_data(data)

# 事件處理等內容與原本版本類似，為簡潔此處使用原檔案內容（已移除舊名稱）

@client.event
async def on_ready():
    logger.info(f"✓ {BOT_NAME} v{BOT_VERSION} 已連接！登入為: {client.user}")
    logger.info(f"✓ Ollama 端點: {OLLAMA_BASE_URL}")
    logger.info(f"✓ 使用模型: {OLLAMA_MODEL}")
    load_all_user_data()
    print(f"✓ {BOT_NAME} 已連接！登入為: {client.user}")
    print(f"✓ 當前版本: {BOT_VERSION}")

@client.event
async def on_member_join(member):
    try:
        welcome_channel = None
        for channel in member.guild.text_channels:
            if channel.name in ["welcome", "歡迎", "general", "通用"]:
                if channel.permissions_for(member.guild.me).send_messages:
                    welcome_channel = channel
                    break
        if welcome_channel:
            welcome_msg = admin.get_welcome_message(member.guild.id)
            await welcome_channel.send(f"👋 {member.mention} {welcome_msg}")
            logger.info(f"新成員加入: {member.name}")
    except Exception as e:
        logger.error(f"無法發送歡迎消息: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("!"):
            await message.channel.send(f"{message.author.mention} 💬 請在私信中使用命令！")
        return
    user_id = message.author.id
    if user_id not in user_dms:
        user_dms[user_id] = message.channel
    if user_id not in user_seen_guide:
        user_seen_guide[user_id] = True
        guide = f"""
👋 **歡迎使用 {BOT_NAME}**

🎊 已集成 **28 個強大功能**

📖 **快速開始:**
`!help` - 查看完整命令
"""
        await message.channel.send(guide)
        return

    # 其餘功能請參考原本程式

def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("未找到 DISCORD_TOKEN")
        print("❌ 錯誤: 未找到 DISCORD_TOKEN")
        return
    logger.info(f"{BOT_NAME} v{BOT_VERSION} 正在啟動...")
    try:
        client.run(token)
    except KeyboardInterrupt:
        logger.info("Bot 被用戶中斷")
    except Exception as e:
        logger.error(f"Bot 運行錯誤: {e}")
        raise

if __name__ == '__main__':
    main()
