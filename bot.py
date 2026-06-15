import os
import sys
import discord
import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import httpx
# 引入 prism_config 中的全局設定
from prism_config import *
# 確保 PERSONALITIES 已正確載入（防止 import * 未帶入）
if 'PERSONALITIES' not in globals():
    from prism_config import PERSONALITIES  # pragma: no cover


# 解决 Windows 编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ==================== 日志系统 ====================
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 配置日志（使用 UTF-8 编码）
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 文件处理器
file_handler = logging.FileHandler(
    f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d')}.log", 
    encoding='utf-8'
)
file_handler.setFormatter(formatter)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 記錄可用角色（方便除錯）
logger.debug(f"已載入角色: {list(PERSONALITIES.keys())}")

# ==================== 初始化 ====================
dotenv_path = os.path.join(os.path.dirname(__file__), "設定.env")
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
admin_env = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i.strip()) for i in admin_env.split(",") if i.strip().isdigit()]

# ==================== 版本管理 ====================
# 使用 prism_config 中的版本資訊
BOT_VERSION = "2.0.0"
last_notified_version = "2.0.0"
# Bot 名称（用于问候）
BOT_NAME = "subaso-俗北ㄙㄡˊ"
# 额外描述（来自 prism_config）
BOT_DESCRIPTION = "subaso-俗北ㄙㄡˊ - 多功能 AI Discord Bot"

# ==================== 数据文件 ====================
DATA_FILE = "user_data.json"

def load_user_data():
    """加载用户数据"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    """保存用户数据"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存数据失败: {e}")

# ==================== 角色和数据 ====================
# PERSONALITIES 已從 prism_config 引入，以下保持空白以避免覆寫

user_personalities = {}
user_languages = {}
user_conversations = {}
user_seen_guide = {}
user_dms = {}  # 存储用户的 DM 频道用于广播
MAX_HISTORY = 10

LANGUAGE_OPTIONS = {
    "chinese": "繁體中文",
    "english": "English",
    "japanese": "日本語",
    "korean": "한국어",
    "spanish": "Español"
}

LANGUAGE_PROMPTS = {
    "chinese": "請使用繁體中文回答。",
    "english": "Please answer in English.",
    "japanese": "日本語で回答してください。",
    "korean": "한국어로 대답해 주세요.",
    "spanish": "Por favor responde en Español."
}

# 加载已保存的用户数据
def load_all_user_data():
    """从文件加载所有用户数据"""
    global user_personalities, user_languages, user_conversations
    data = load_user_data()
    if "personalities" in data:
        user_personalities = {int(k): v for k, v in data["personalities"].items()}
    if "languages" in data:
        user_languages = {int(k): v for k, v in data["languages"].items()}
    if "conversations" in data:
        user_conversations = data["conversations"]
    logger.info(f"加载了 {len(user_personalities)} 个用户的数据")

def save_all_user_data():
    """保存所有用户数据到文件"""
    global user_personalities, user_languages, user_conversations, BOT_VERSION, last_notified_version
    data = {
        "personalities": {str(k): v for k, v in user_personalities.items()},
        "languages": {str(k): v for k, v in user_languages.items()},
        "conversations": user_conversations,
        "last_save": datetime.now().isoformat(),
        "bot_version": BOT_VERSION,
        "last_notified_version": last_notified_version
    }
    save_user_data(data)

def load_version_info():
    """加载版本信息"""
    global BOT_VERSION, last_notified_version
    data = load_user_data()
    if "bot_version" in data:
        BOT_VERSION = data["bot_version"]
    if "last_notified_version" in data:
        last_notified_version = data["last_notified_version"]

# ==================== 事件处理 ====================
@client.event
async def on_ready():
    logger.info(f"✓ Bot 已連接！登入為: {client.user}")
    logger.info(f"✓ Ollama 端點: {OLLAMA_BASE_URL}")
    logger.info(f"✓ 使用模型: {OLLAMA_MODEL}")
    
    # 加载用户数据
    load_all_user_data()
    load_version_info()
    
    # 检查版本更新
    await check_and_notify_updates()
    
    print(f"✓ Bot 已連接！登入為: {client.user}")
    print(f"✓ 當前版本: {BOT_VERSION}")

@client.event
async def on_member_join(member):
    """新成員加入時发送欢迎消息"""
    try:
        welcome_channel = None
        for channel in member.guild.text_channels:
            if channel.name in ["welcome", "歡迎", "general", "通用"]:
                if channel.permissions_for(member.guild.me).send_messages:
                    welcome_channel = channel
                    break
        
        if welcome_channel:
            welcome_msg = f"""
👋 **歡迎 {member.mention}！**

🤖 這是 AI 聊天助手機器人。

🚀 **快速開始:**
在私信中輸入任何消息，我會自動發送完整說明。

💬 **常用命令:**
`!mode 角色名` - 切換角色
`!ask 問題` - 提問
`!help` - 幫助

祝使用愉快！😊
"""
            await welcome_channel.send(welcome_msg)
            logger.info(f"新成員加入: {member.name}")
    except Exception as e:
        logger.error(f"無法發送歡迎消息: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # 只在 DM 中回應
    if not isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("!"):
            await message.channel.send(f"{message.author.mention} 💬 請在私信中使用命令！")
        return
    
    user_id = message.author.id
    
    # 保存用户 DM 频道用于广播
    if user_id not in user_dms:
        user_dms[user_id] = message.channel
    
    # 首次发送时显示 guide
    if user_id not in user_seen_guide:
        user_seen_guide[user_id] = True
        guide = """
👋 **歡迎使用 AI 聊天助手！**

🎭 **5 種角色:**
✅ 閒談 | 🔢 數理 | 📚 語文 | 💻 程式 | 🏠 家務

📖 **使用方法:**
`!mode 角色名` - 切換角色 (例: !mode 程式)
`!ask 你的問題` - 提問
`!lan [語言]` - 選擇回答語言 (例: !lan english)
`!clear` - 清除對話
`!help` - 幫助

🚀 **試試看:**
`!mode 閒談` 然後 `!ask 你好！`
"""
        await message.channel.send(guide)
        return
    
    # 处理管理员命令
    if message.content.startswith("!admin") and user_id in ADMIN_IDS:
        await handle_admin_command(message)
        return
    
    current_personality = user_personalities.get(user_id, "閒談")
    
    # 处理其他命令
    if message.content.startswith("!mode"):
        args = message.content[5:].strip().split()
        if not args:
            available = ", ".join(f"**{k}**" for k in PERSONALITIES.keys())
            await message.channel.send(
                f"目前角色: **{current_personality}**\n可用角色: {available}"
            )
            return

        # 取得使用者輸入的角色字串，允許前後空白與大小寫差異
        raw_input = args[0].strip()
        normalized = raw_input

        # 直接匹配（完全相同）
        if normalized not in PERSONALITIES:
            # 別名映射（常見英文或簡體中文別名）
            alias_map = {
                "chat": "閒談",
                "闲谈": "閒談",
                "chatting": "閒談",
                "math": "數理",
                "science": "數理",
                "language": "語文",
                "lang": "語文",
                "code": "程式",
                "programming": "程式",
                "home": "家務",
                "house": "家務"
            }
            lowered = raw_input.lower()
            if lowered in alias_map:
                normalized = alias_map[lowered]
            else:
                # 不區分大小寫的直接比對
                matches = [k for k in PERSONALITIES.keys() if k.lower() == lowered]
                if matches:
                    normalized = matches[0]
                else:
                    # 簡單的關鍵字模糊匹配（例如只輸入 "閒"）
                    fuzzy = [k for k in PERSONALITIES.keys() if lowered in k.lower()]
                    if fuzzy:
                        normalized = fuzzy[0]

        if normalized in PERSONALITIES:
            user_personalities[user_id] = normalized
            save_all_user_data()
            await message.channel.send(f"✅ 已切換到 **{normalized}** 模式")
            logger.info(f"用戶 {user_id} 切換角色: {normalized}")
        else:
            available = ", ".join(f"**{k}**" for k in PERSONALITIES.keys())
            await message.channel.send(f"❌ 不存在的角色類型。可用角色: {available}")

    elif message.content.startswith("!lan"):
        args = message.content[4:].strip().split()
        if not args:
            current_lang = user_languages.get(user_id, "chinese")
            available = ", ".join(f"**{k}**" for k in LANGUAGE_OPTIONS.keys())
            await message.channel.send(
                f"目前語言: **{current_lang}**\n可用語言: {available}"
            )
        else:
            selected = args[0].strip('"\'').lower()
            if selected in LANGUAGE_OPTIONS:
                user_languages[user_id] = selected
                save_all_user_data()
                await message.channel.send(f"✅ 已切換語言為 **{LANGUAGE_OPTIONS[selected]}**")
                logger.info(f"用戶 {user_id} 切換語言: {selected}")
            else:
                available = ", ".join(f"**{k}**" for k in LANGUAGE_OPTIONS.keys())
                await message.channel.send(f"❌ 不支持的語言。可選: {available}")

    elif message.content.startswith("!ask"):
        question = message.content[5:].strip()
        if not question:
            await message.channel.send("請輸入問題 (!ask [你的問題])")
            return
        
        await handle_ai_request(message, question, current_personality)
    
    elif message.content.startswith("!clear"):
        if user_id in user_conversations:
            del user_conversations[user_id]
        save_all_user_data()
        await message.channel.send("✅ 已清除對話歷史")
        logger.info(f"用戶 {user_id} 清除對話")
    
    elif message.content.startswith("!deleteall"):
        # 删除对话历史和 Bot 消息
        deleted_count = 0
        try:
            # 清除内存中的对话
            if user_id in user_conversations:
                del user_conversations[user_id]
            
            # 清除 JSON 存储的数据
            try:
                data = json.load(open("user_data.json", "r", encoding="utf-8"))
                if str(user_id) in data.get("personalities", {}):
                    del data["personalities"][str(user_id)]
                if str(user_id) in data.get("languages", {}):
                    del data["languages"][str(user_id)]
                if str(user_id) in data.get("conversations", {}):
                    del data["conversations"][str(user_id)]
                data["last_save"] = datetime.now().isoformat()
                json.dump(data, open("user_data.json", "w", encoding="utf-8"), ensure_ascii=False)
            except:
                pass
            
            # 删除 Bot 发送的消息
            async for msg in message.channel.history(limit=None):
                if msg.author == client.user and msg.id != message.id:
                    try:
                        await msg.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.2)  # 避免速率限制
                    except:
                        pass
            
            await message.channel.send(f"✅ 已清除所有数据和 {deleted_count} 条对话消息")
            logger.info(f"用户 {user_id} 完全删除了数据和 {deleted_count} 条消息")
        except Exception as e:
            await message.channel.send(f"❌ 清除失败: {str(e)}")
            logger.error(f"清除失败: {e}")
    
    elif message.content.startswith("!help"):
        help_text = """
```
命令列表:
!mode [角色] - 切換角色
!ask [問題] - 提問 (支援連續對話)
!lan [語言] - 選擇回答語言
!clear - 清除對話記錄
!deleteall - 刪除所有訊息
!guide - 顯示引導
!help - 顯示此幫助

角色: 閒談、數理、語文、程式、家務
```
"""
        await message.channel.send(help_text)
    
    elif message.content.startswith("!guide"):
        await message.channel.send("""
🎭 5 種 AI 角色 - 隨意切換！

✅ 閒談 - 友善聊天
🔢 數理 - 數學科學
📚 語文 - 語言文學
💻 程式 - 編程技術
🏠 家務 - 生活建議

使用: !mode [角色] → !ask [問題]
""")

    # 默认回复：非命令的私信消息
    else:
        # 若用户在私信中发送非命令内容，回复问候并使用 BOT_NAME
        await message.channel.send(
            f"嗨 {message.author.name}，我是 {BOT_NAME}，很高興認識你！"
        )

async def handle_ai_request(message, question, personality):
    user_id = message.author.id
    # 確保對話歷史存在
    if user_id not in user_conversations:
        user_conversations[user_id] = []

    try:
        async with message.channel.typing():
            language = user_languages.get(user_id, "chinese")
            system_prompt = PERSONALITIES[personality]["system"] + " " + LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS["chinese"])
            
            # 建構消息序列
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend(user_conversations[user_id])
            api_messages.append({"role": "user", "content": question})

            # 使用已導入的 httpx 進行非同步請求
            async with httpx.AsyncClient(timeout=None) as client_http:
                payload = {
                    "model": OLLAMA_MODEL,
                    "messages": api_messages,
                    "stream": False,
                    "options": {"num_ctx": 4096} # 確保上下文長度足夠
                }
                response = await client_http.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
                response.raise_for_status()
                result = response.json()
                answer = result.get("message", {}).get("content", "⚠️ AI 未返回內容")

            # 更新歷史紀錄
            user_conversations[user_id].append({"role": "user", "content": question})
            user_conversations[user_id].append({"role": "assistant", "content": answer})

            # 限制歷史長度
            if len(user_conversations[user_id]) > MAX_HISTORY * 2:
                user_conversations[user_id] = user_conversations[user_id][-(MAX_HISTORY * 2):]

            # 保存對話記錄
            save_all_user_data()

            # 輸出 (加上簡單的長度處理)
            label = f"**【{personality} 助手】**\n"
            if len(answer) + len(label) > 2000:
                await message.channel.send(f"{label} (訊息過長，分段發送中...)")
                for i in range(0, len(answer), 1900):
                    await message.channel.send(answer[i:i+1900])
            else:
                await message.channel.send(f"{label}{answer}")

    except Exception as e:
        logger.error(f"AI 處理錯誤: {e}")
        await message.channel.send(f"❌ 發生錯誤: {str(e)}")

async def check_and_notify_updates():
    """检查版本更新并通知用户"""
    global BOT_VERSION, last_notified_version
    # 如果有新版本需要通知
    if BOT_VERSION != last_notified_version and len(user_dms) > 0:
        await broadcast_update_notification(BOT_VERSION)

async def broadcast_update_notification(new_version):
    """向所有用户广播更新通知"""
    global BOT_VERSION, last_notified_version
    BOT_VERSION = new_version
    last_notified_version = new_version
    save_all_user_data()
    
    update_message = f"""
🎉 **系統更新通知** 🎉

✅ 已更新成 **{new_version}**

新版本已推送，感謝使用！
"""
    
    success_count = 0
    failed_count = 0
    
    for user_id, dm_channel in list(user_dms.items()):
        try:
            await dm_channel.send(update_message)
            success_count += 1
            await asyncio.sleep(0.5)  # 避免速率限制
        except Exception as e:
            logger.error(f"無法向用戶 {user_id} 發送更新通知: {e}")
            failed_count += 1
    
    logger.info(f"更新通知已發送: 成功 {success_count}, 失敗 {failed_count}")

async def handle_admin_command(message):
    """处理管理员命令"""
    user_id = message.author.id
    cmd = message.content[6:].strip().split()
    
    if not cmd:
        await message.channel.send("""
```
管理員命令:
!admin stats - 查看統計
!admin clear_user [user_id] - 清除用戶數據
!admin backup - 備份數據
!admin update [版本號] - 發送更新通知 (例: !admin update 1.0.1)
!admin restart - 重啟 Bot
```
""")
        return
    
    if cmd[0] == "stats":
        stats = f"""
📊 **Bot 統計**
總用戶: {len(user_personalities)}
在線: {len(client.guilds)} 個伺服器
"""
        await message.channel.send(stats)
        logger.info(f"管理員 {user_id} 查看統計")
    
    elif cmd[0] == "clear_user" and len(cmd) > 1:
        target_id = int(cmd[1])
        if target_id in user_personalities:
            del user_personalities[target_id]
            save_all_user_data()
            await message.channel.send(f"✅ 已清除用戶 {target_id} 的數據")
            logger.warning(f"管理員 {user_id} 清除了用戶 {target_id} 的數據")
        else:
            await message.channel.send("❌ 用戶不存在")
    
    elif cmd[0] == "backup":
        save_all_user_data()
        await message.channel.send("✅ 已備份數據")
        logger.info(f"管理員 {user_id} 執行備份")
    
    elif cmd[0] == "restart":
        await message.channel.send("🔄 Bot 即將重啟...")
        logger.warning(f"管理員 {user_id} 觸發重啟")
        await client.close()
    
    elif cmd[0] == "update" and len(cmd) > 1:
        new_version = cmd[1]
        await broadcast_update_notification(new_version)
        await message.channel.send(f"✅ 已發送更新通知至所有用戶: 版本 {new_version}")
        logger.warning(f"管理員 {user_id} 觸發更新至版本 {new_version}")

# ==================== 启动 ====================
def main():
    """主函数"""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("未找到 DISCORD_TOKEN")
        print("❌ 錯誤: 未找到 DISCORD_TOKEN")
        return
    
    logger.info("Bot 正在啟動...")
    
    try:
        client.run(token)
    except KeyboardInterrupt:
        logger.info("Bot 被用戶中斷")
    except Exception as e:
        logger.error(f"Bot 運行錯誤: {e}")
        raise

if __name__ == "__main__":
    main()
