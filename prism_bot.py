"""
PRISM Bot v2.0 - 多功能 Discord Bot
包含 28 個強大功能的完整實現

功能模塊:
🤖 AI 對話系統 (5個)
💰 經濟系統 (6個)
🎮 娛樂遊戲 (6個)
⚙️ 管理工具 (5個)
🎵 音樂系統 (可選, 6個)
"""

import os
import sys
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
from prism_config import *

# ==================== 日誌系統 ====================
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(
    f"{log_dir}/prism_{datetime.now().strftime('%Y%m%d')}.log", 
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

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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
    """加載用戶數據"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    """保存用戶數據"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存數據失敗: {e}")

def load_all_user_data():
    """從文件加載所有用戶數據"""
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
    """保存所有用戶數據到文件"""
    global user_personalities, user_languages, BOT_VERSION, last_notified_version
    data = {
        "personalities": {str(k): v for k, v in user_personalities.items()},
        "languages": {str(k): v for k, v in user_languages.items()},
        "last_save": datetime.now().isoformat(),
        "bot_version": BOT_VERSION,
        "last_notified_version": last_notified_version
    }
    save_user_data(data)

# ==================== 事件處理 ====================
@client.event
async def on_ready():
    logger.info(f"✓ PRISM Bot v{BOT_VERSION} 已連接！登入為: {client.user}")
    logger.info(f"✓ Ollama 端點: {OLLAMA_BASE_URL}")
    logger.info(f"✓ 使用模型: {OLLAMA_MODEL}")
    
    load_all_user_data()
    
    print(f"✓ PRISM 已連接！登入為: {client.user}")
    print(f"✓ 當前版本: {BOT_VERSION}")
    print(f"✓ 已加載 28 個強大功能")

@client.event
async def on_member_join(member):
    """新成員加入時發送歡迎消息"""
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
    
    # 只在 DM 中回應
    if not isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("!"):
            await message.channel.send(f"{message.author.mention} 💬 請在私信中使用命令！")
        return
    
    user_id = message.author.id
    
    # 保存用戶 DM 頻道
    if user_id not in user_dms:
        user_dms[user_id] = message.channel
    
    # 首次發送時顯示指南
    if user_id not in user_seen_guide:
        user_seen_guide[user_id] = True
        guide = """
👋 **歡迎使用 PRISM - 棱鏡 Bot**

🎊 已集成 **28 個強大功能**

🤖 **AI 対話** (5個) - 多角色、多語言、連續對話
💰 **經濟系統** (6個) - 挖礦、釣魚、賭博、寵物、市場
🎮 **娛樂遊戲** (6個) - Pokemon、Trivia、動漫、數字遊戲
⚙️ **管理工具** (5個) - 日誌、清理、歡迎、配置
🎵 **音樂系統** (6個) - 可選 (需額外設置)

📖 **快速開始:**
`!help` - 查看完整命令
`!mode` - 切換 AI 角色
`!balance` - 查看餘額
`!pokemon` - 玩遊戲

祝使用愉快！🌈
"""
        await message.channel.send(guide)
        return
    
    # 處理管理員命令
    if message.content.startswith("!admin") and user_id in ADMIN_IDS:
        await handle_admin_command(message)
        return
    
    # 新增問候觸發：如果用戶自我介紹爲 俗北，回覆問候並使用 bot 名稱
    if "我叫 俗北" in message.content or "我叫俗北" in message.content:
        await message.channel.send(f"嗨 俗北！我是 {BOT_NAME}，很高興認識你！今天心情如何？")
        return
    
    current_personality = user_personalities.get(user_id, "閒談")
    
    # ==================== AI 命令 ====================
    if message.content.startswith("!mode"):
        args = message.content[5:].strip().split()
        if not args:
            available = ", ".join(f"**{k}** {v['emoji']}" for k, v in PERSONALITIES.items())
            await message.channel.send(f"目前角色: **{current_personality}**\n可用角色: {available}")
            return

        # 取得使用者輸入的角色字串，允許前後空白與大小寫差異
        raw_input = args[0].strip()
        normalized = raw_input

        # 直接匹配（完全相同）
        if normalized not in PERSONALITIES:
            # 別名映射（常見英文或簡體中文別名）
            alias_map = {
                "chat": "閒談",
                "閒談": "閒談",
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
                    # 最後嘗試包含關鍵字的模糊匹配（例如使用者輸入 "閒"）
                    fuzzy = [k for k in PERSONALITIES.keys() if lowered in k.lower()]
                    if fuzzy:
                        normalized = fuzzy[0]

        if normalized in PERSONALITIES:
            user_personalities[user_id] = normalized
            save_all_user_data()
            emoji = PERSONALITIES[normalized]['emoji']
            await message.channel.send(f"✅ 已切換到 **{emoji} {normalized}** 模式")
            logger.info(f"用戶 {user_id} 切換角色: {normalized}")
        else:
            available = ", ".join(f"**{k}**" for k in PERSONALITIES.keys())
            await message.channel.send(f"❌ 不存在的角色類型。可用角色: {available}")
    
    elif message.content.startswith("!lan"):
        args = message.content[4:].strip().split()
        if not args:
            current_lang = user_languages.get(user_id, "chinese")
            available = ", ".join(f"**{k}**" for k in LANGUAGE_OPTIONS.keys())
            await message.channel.send(f"目前語言: **{current_lang}**\n可用語言: {available}")
        else:
            selected = args[0].strip('"\'').lower()
            if selected in LANGUAGE_OPTIONS:
                user_languages[user_id] = selected
                save_all_user_data()
                await message.channel.send(f"✅ 已切換語言為 **{LANGUAGE_OPTIONS[selected]}**")
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
        await message.channel.send("✅ 已清除對話歷史")
    
    # ==================== 經濟命令 ====================
    elif message.content.startswith("!balance"):
        balance = economy.get_balance(user_id)
        await message.channel.send(f"💎 **你的餘額:** {balance} {CURRENCY_NAME}")
    
    elif message.content.startswith("!mine"):
        can_mine, remaining = economy.can_mine(user_id)
        if not can_mine:
            await message.channel.send(f"⏳ 還要等 {remaining} 秒才能再次挖礦")
        else:
            ore, amount, emoji = economy.mine(user_id)
            await message.channel.send(f"{emoji} 你挖到了 **{ore}**！\n賺取 **{amount}** {CURRENCY_NAME}")
    
    elif message.content.startswith("!fish"):
        can_fish, remaining = economy.can_fish(user_id)
        if not can_fish:
            await message.channel.send(f"⏳ 還要等 {remaining} 秒才能再次釣魚")
        else:
            catch, amount, emoji = economy.fish(user_id)
            await message.channel.send(f"{emoji} 你釣到了 **{catch}**！\n賺取 **{amount}** {CURRENCY_NAME}")
    
    elif message.content.startswith("!hunt"):
        can_hunt, remaining = economy.can_hunt(user_id)
        if not can_hunt:
            await message.channel.send(f"⏳ 還要等 {remaining} 秒才能再次狩獵")
        else:
            animal, amount, emoji = economy.hunt(user_id)
            await message.channel.send(f"{emoji} 你獵到了 **{animal}**！\n賺取 **{amount}** {CURRENCY_NAME}")
    
    elif message.content.startswith("!gamble"):
        args = message.content[8:].strip().split()
        if not args:
            await message.channel.send("用法: !gamble [金額]")
        else:
            try:
                amount = int(args[0])
                won, winnings, msg = economy.gamble(user_id, amount)
                if won is False and msg == "餘額不足":
                    await message.channel.send(f"❌ 餘額不足")
                elif won:
                    await message.channel.send(f"🎉 {msg}\n獲得 {winnings} {CURRENCY_NAME}")
                else:
                    await message.channel.send(f"😢 {msg}")
            except:
                await message.channel.send("請輸入有效的金額")
    
    elif message.content.startswith("!slots"):
        args = message.content[7:].strip().split()
        if not args:
            await message.channel.send("用法: !slots [金額]")
        else:
            try:
                amount = int(args[0])
                won, winnings, result = economy.slots(user_id, amount)
                symbols = "".join(result)
                if won:
                    await message.channel.send(f"🎰 {symbols}\n🎉 中獎！獲得 {winnings} {CURRENCY_NAME}")
                else:
                    await message.channel.send(f"🎰 {symbols}\n😢 沒中獎...")
            except:
                await message.channel.send("請輸入有效的金額")
    
    elif message.content.startswith("!pet"):
        args = message.content[5:].strip().split()
        if not args:
            await message.channel.send("用法: !pet [list|adopt|info|feed]")
        elif args[0] == "list":
            pets_list = "\n".join([f"**{name}** {info['emoji']}" for name, info in PETS.items()])
            await message.channel.send(f"🐾 **可領養的寵物:**\n{pets_list}")
        elif args[0] == "adopt" and len(args) > 1:
            success, msg = economy.adopt_pet(user_id, args[1])
            await message.channel.send(msg)
        elif args[0] == "info":
            pet = economy.get_pet(user_id)
            if pet:
                await message.channel.send(f"🐾 **你的寵物:**\n{pet['emoji']} {pet['name']}\n心情: {pet['mood']}/100")
            else:
                await message.channel.send("你還沒有寵物")
        elif args[0] == "feed" and len(args) > 1:
            try:
                amount = int(args[1])
                success, msg = economy.feed_pet(user_id, amount)
                await message.channel.send(msg)
            except:
                await message.channel.send("請輸入有效的金額")
    
    # ==================== 遊戲命令 ====================
    elif message.content.startswith("!pokemon"):
        question = games.start_pokemon_game(user_id)
        await message.channel.send(question)
    
    elif message.content.startswith("!trivia"):
        question = games.start_trivia(user_id)
        await message.channel.send(question)
    
    elif message.content.startswith("!anime"):
        question = games.start_anime_guess(user_id)
        await message.channel.send(question)
    
    elif message.content.startswith("!number"):
        question = games.start_number_game(user_id)
        await message.channel.send(question)
    
    elif message.content.startswith("!guess"):
        args = message.content[7:].strip()
        success, msg = games.check_pokemon_answer(user_id, args)
        await message.channel.send(msg)
    
    elif message.content.startswith("!score"):
        score = games.get_user_score(user_id)
        await message.channel.send(f"🏆 **你的遊戲分數:** {score} 分")
    
    # ==================== 互動命令 ====================
    elif message.content.startswith("!hug"):
        target = message.mentions[0].mention if message.mentions else "大家"
        await message.channel.send(f"🤗 {message.author.mention} 擁抱了 {target}")
    
    elif message.content.startswith("!pat"):
        target = message.mentions[0].mention if message.mentions else "你"
        await message.channel.send(f"👋 {message.author.mention} 拍了拍 {target}")
    
    elif message.content.startswith("!dance"):
        await message.channel.send(f"🕺 {message.author.mention} 跳起舞來！")
    
    # ==================== 管理命令 ====================
    elif message.content.startswith("!deleteall"):
        deleted_count = 0
        try:
            if user_id in user_conversations:
                del user_conversations[user_id]
            
            try:
                data = json.load(open("user_data.json", "r", encoding="utf-8"))
                if str(user_id) in data.get("personalities", {}):
                    del data["personalities"][str(user_id)]
                if str(user_id) in data.get("languages", {}):
                    del data["languages"][str(user_id)]
                data["last_save"] = datetime.now().isoformat()
                json.dump(data, open("user_data.json", "w", encoding="utf-8"), ensure_ascii=False)
            except:
                pass
            
            async for msg in message.channel.history(limit=None):
                if msg.author == client.user and msg.id != message.id:
                    try:
                        await msg.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.2)
                    except:
                        pass
            
            await message.channel.send(f"✅ 已清除所有數據和 {deleted_count} 條對話消息")
            logger.info(f"用戶 {user_id} 完全刪除了數據和 {deleted_count} 條消息")
        except Exception as e:
            await message.channel.send(f"❌ 清除失敗: {str(e)}")
    
    elif message.content.startswith("!help"):
        help_text = """
```
╔════════════════════════════════════════╗
║          PRISM Bot 完整命令列表         ║
╚════════════════════════════════════════╝

🤖 AI 對話:
!mode [角色] - 切換 AI 角色
!lan [語言] - 切換回答語言
!ask [問題] - 提問

💰 經濟系統:
!balance - 查看餘額
!mine - 挖礦 (60秒冷卻)
!fish - 釣魚 (60秒冷卻)
!hunt - 狩獵 (120秒冷卻)
!gamble [金額] - 賭博
!slots [金額] - 老虎機
!pet [list|adopt|info|feed] - 寵物系統

🎮 娛樂遊戲:
!pokemon - Pokemon猜謎
!trivia - Trivia知識競賽
!anime - 動漫角色猜謎
!number - 數字猜測遊戲
!score - 查看遊戲分數

✨ 互動:
!hug [@用戶] - 擁抱
!pat [@用戶] - 拍拍
!dance - 跳舞
!help - 此幫助
```
"""
        await message.channel.send(help_text)
    
    elif message.content.startswith("!guide"):
        guide = """
🎊 **PRISM Bot - 功能概覽**

28 個強大功能已集成:

🤖 **AI 對話系統** (5個)
- 5 種角色 | 多語言 | 連續對話 | 版本管理 | 數據保存

💰 **經濟系統** (6個)
- 挖礦 | 釣魚 | 狩獵 | 賭博 | 寵物 | 市場

🎮 **娛樂遊戲** (6個)
- Pokémon | Trivia | 動漫 | 數字 | 查詢 | 互動

⚙️ **管理工具** (5個)
- 日誌 | 清理 | 歡迎 | 配置 | 自定義命令

🎵 **音樂系統** (6個)
- 播放 | 播放列表 | 控制 | DJ模式 | 直播 | 搜索

輸入 !help 查看完整命令
"""
        await message.channel.send(guide)
    else:
        # 未匹配任何已知指令，回覆提示
        await message.channel.send("❓ 未知指令，輸入 !help 查看指令列表。")

# ==================== AI 處理函數 ====================
async def handle_ai_request(message, question, personality):
    user_id = message.author.id
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []

    try:
        async with message.channel.typing():
            language = user_languages.get(user_id, "chinese")
            system_prompt = PERSONALITIES[personality]["system"] + " " + LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS["chinese"])
            
            api_messages = [{"role": "system", "content": system_prompt}]
            api_messages.extend(user_conversations[user_id])
            api_messages.append({"role": "user", "content": question})

            async with httpx.AsyncClient(timeout=None) as client_http:
                payload = {
                    "model": OLLAMA_MODEL,
                    "messages": api_messages,
                    "stream": False,
                    "options": {"num_ctx": 4096}
                }
                response = await client_http.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
                response.raise_for_status()
                result = response.json()
                answer = result.get("message", {}).get("content", "⚠️ AI 未返回內容")

            user_conversations[user_id].append({"role": "user", "content": question})
            user_conversations[user_id].append({"role": "assistant", "content": answer})

            if len(user_conversations[user_id]) > MAX_HISTORY * 2:
                user_conversations[user_id] = user_conversations[user_id][-(MAX_HISTORY * 2):]

            label = f"**【{PERSONALITIES[personality]['emoji']} {personality}】**\n"
            if len(answer) + len(label) > 2000:
                await message.channel.send(f"{label}(訊息過長，分段發送中...)")
                for i in range(0, len(answer), 1900):
                    await message.channel.send(answer[i:i+1900])
            else:
                await message.channel.send(f"{label}{answer}")

    except Exception as e:
        logger.error(f"AI 處理錯誤: {e}")
        await message.channel.send(f"❌ 發生錯誤: {str(e)}")

# ==================== 管理員命令 ====================
async def handle_admin_command(message):
    user_id = message.author.id
    cmd = message.content[6:].strip().split()
    
    if not cmd:
        await message.channel.send("""
```
🔑 管理員命令:
!admin stats - 查看統計
!admin update [版本號] - 發送更新通知
!admin clear_user [user_id] - 清除用戶數據
!admin backup - 備份數據
!admin restart - 重啟 Bot
```
""")
        return
    
    if cmd[0] == "stats":
        stats = f"""
📊 **PRISM Bot 統計**
總用戶: {len(user_personalities)}
在線: {len(client.guilds)} 個伺服器
版本: {BOT_VERSION}
"""
        await message.channel.send(stats)
    
    elif cmd[0] == "update" and len(cmd) > 1:
        new_version = cmd[1]
        await broadcast_update_notification(new_version)
        await message.channel.send(f"✅ 已發送更新通知至所有用戶: 版本 {new_version}")
    
    elif cmd[0] == "backup":
        save_all_user_data()
        await message.channel.send("✅ 已備份數據")
    
    elif cmd[0] == "restart":
        await message.channel.send("🔄 Bot 即將重啟...")
        await client.close()

async def broadcast_update_notification(new_version):
    """廣播更新通知"""
    global BOT_VERSION, last_notified_version
    BOT_VERSION = new_version
    last_notified_version = new_version
    save_all_user_data()
    
    update_message = f"""
🎉 **PRISM Bot 系統更新** 🎉

✅ 已更新成 **{new_version}**

新版本已推送，感謝使用！
"""
    
    success_count = 0
    for user_id, dm_channel in list(user_dms.items()):
        try:
            await dm_channel.send(update_message)
            success_count += 1
            await asyncio.sleep(0.5)
        except:
            pass
    
    logger.info(f"更新通知已發送: 成功 {success_count}")

# ==================== 啟動 ====================
def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("未找到 DISCORD_TOKEN")
        print("❌ 錯誤: 未找到 DISCORD_TOKEN")
        return
    
    logger.info("PRISM Bot v2.0 正在啟動...")
    print(f"""
╔════════════════════════════════════════╗
║        🌈 PRISM Bot v{BOT_VERSION} 啟動中 🌈     ║
║                                        ║
║    包含 28 個強大功能的完整實現        ║
║                                        ║
╚════════════════════════════════════════╝
""")
    
    try:
        client.run(token)
    except KeyboardInterrupt:
        logger.info("Bot 被用戶中斷")
    except Exception as e:
        logger.error(f"Bot 運行錯誤: {e}")
        raise

if __name__ == "__main__":
    main()
