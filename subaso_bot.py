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
from datetime import datetime, timedelta
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
user_debates = {}  # 存儲用戶當前的辯論
last_notified_version = BOT_VERSION

# 星期三自動更新相關
last_auto_update_date = None
AUTO_UPDATE_HOUR = 0  # 每天 00:00 檢查

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
    global user_personalities, user_languages, user_conversations, user_seen_guide, user_debates, last_notified_version
    data = load_user_data()
    if "personalities" in data:
        user_personalities = {int(k): v for k, v in data["personalities"].items()}
    if "languages" in data:
        user_languages = {int(k): v for k, v in data["languages"].items()}
    if "conversations" in data:
        user_conversations = data["conversations"]
    if "seen_guide" in data:
        user_seen_guide = data["seen_guide"]
    if "debates" in data:
        user_debates = data["debates"]
    if "last_notified_version" in data:
        last_notified_version = data["last_notified_version"]
    logger.info(f"加載了 {len(user_personalities)} 個用戶的數據")

def save_all_user_data():
    global user_personalities, user_languages, user_conversations, user_seen_guide, user_debates, BOT_VERSION, last_notified_version
    data = {
        "personalities": {str(k): v for k, v in user_personalities.items()},
        "languages": {str(k): v for k, v in user_languages.items()},
        "conversations": user_conversations,
        "seen_guide": user_seen_guide,
        "debates": user_debates,
        "last_save": datetime.now().isoformat(),
        "bot_version": BOT_VERSION,
        "last_notified_version": last_notified_version
    }
    save_user_data(data)

async def weekly_auto_update_task():
    """後台任務：每週三 00:00 自動觸發版本更新檢查"""
    global last_auto_update_date
    
    while True:
        try:
            now = datetime.now()
            # 檢查是否是星期三 (weekday() 返回 0-6，其中 2 是星期三)
            if now.weekday() == 2 and now.hour == AUTO_UPDATE_HOUR:
                # 檢查今天是否已執行過
                today = now.date()
                if last_auto_update_date != today:
                    last_auto_update_date = today
                    logger.info(f"⏰ 星期三自動更新檢查觸發! 版本: {BOT_VERSION}")
                    
                    # 觸發更新通知
                    if len(user_dms) > 0:
                        await broadcast_update_notification(BOT_VERSION)
                    else:
                        logger.info("暫無用戶連接，跳過更新通知")
            
            # 每分鐘檢查一次
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"自動更新任務出錯: {e}")
            await asyncio.sleep(60)

# 事件處理等內容與原本版本類似，為簡潔此處使用原檔案內容（已移除舊名稱）

@client.event
async def on_ready():
    logger.info(f"✓ {BOT_NAME} v{BOT_VERSION} 已連接！登入為: {client.user}")
    logger.info(f"✓ Ollama 端點: {OLLAMA_BASE_URL}")
    logger.info(f"✓ 使用模型: {OLLAMA_MODEL}")
    load_all_user_data()
    
    # 啟動星期三自動更新後台任務
    asyncio.create_task(weekly_auto_update_task())
    logger.info("✓ 星期三自動更新任務已啟動")
    
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
    
    try:
        # 只在 DM 中回應
        if not isinstance(message.channel, discord.DMChannel):
            if message.content.startswith("!"):
                await message.channel.send(f"{message.author.mention} 💬 請在私信中使用命令！")
            return
        
        user_id = message.author.id
        
        # 保存用戶 DM 頻道
        if user_id not in user_dms:
            user_dms[user_id] = message.channel
        
        # 如果使用者還沒儲存預設個人設定，補上並持久化
        if user_id not in user_personalities:
            user_personalities[user_id] = "閒談"
        if user_id not in user_languages:
            user_languages[user_id] = "chinese"
        save_all_user_data()
        
        # 首次發送時顯示指南
        if user_id not in user_seen_guide:
            user_seen_guide[user_id] = True
            guide = f"""
👋 **歡迎使用 {BOT_NAME}**

🎊 已集成 **28 個強大功能**

🤖 **AI 對話** (5個) - 多角色、多語言、連續對話
💰 **經濟系統** (6個) - 挖礦、釣魚、賭博、寵物、市場
🎮 **娛樂遊戲** (6個) - Pokemon、Trivia、動漫、數字遊戲
⚙️ **管理工具** (5個) - 日誌、清理、歡迎、配置

📖 **快速開始:**
`!help` - 查看完整命令
`!mode` - 切換 AI 角色
`!ask` - 提問

輸入 !help 獲取全部指令。
"""
            await message.channel.send(guide)
            return
    
        # 處理管理員命令
        if message.content.startswith("!admin") and user_id in ADMIN_IDS:
            await handle_admin_command(message)
            return
    
        current_personality = user_personalities.get(user_id, "閒談")
    
        # AI 命令
        if message.content.startswith("!mode"):
            args = message.content[5:].strip().split()
            if not args:
                available = ", ".join(f"**{k}** {v['emoji']}" for k, v in PERSONALITIES.items())
                await message.channel.send(f"目前角色: **{current_personality}**\n可用角色: {available}")
                return

            raw_input = args[0].strip()
            normalized = raw_input

            if normalized not in PERSONALITIES:
                alias_map = {
                    "chat": "閒談",
                    "math": "數理",
                    "science": "數理",
                    "language": "語文",
                    "lang": "語文",
                    "code": "程式",
                    "programming": "程式",
                    "home": "家務",
                    "house": "家務",
                }
                lowered = raw_input.lower()
                if lowered in alias_map:
                    normalized = alias_map[lowered]
                else:
                    matches = [k for k in PERSONALITIES.keys() if k.lower() == lowered]
                    if matches:
                        normalized = matches[0]
                    else:
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
                    await message.channel.send(f"❌ 不支援的語言。可選: {available}")

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

        elif message.content.startswith("!debate"):
            raw = message.content[8:].strip()
            if not raw:
                debate_msg, debate_data = games.start_debate()
                user_debates[user_id] = debate_data
                await message.channel.send(debate_msg)
                return

            args = raw.split(maxsplit=1)
            command = args[0].lower()
            debate = user_debates.get(user_id)

            if command in ['a', 'b'] and len(args) == 1:
                if not debate:
                    await message.channel.send("⚠️ 請先用 `!debate` 開始一場辯論")
                    return
                if debate.get('user_choice'):
                    await message.channel.send("⚠️ 你已經選過立場了，請使用 `!debate arg [你的論點]` 或 `!debate end`。")
                    return

                debate['user_choice'] = command
                user_side = debate['side_a'] if command == 'a' else debate['side_b']
                ai_side = debate['side_b'] if command == 'a' else debate['side_a']
                topic = debate['topic']
                prompt = (
                    f"議題: {topic}\n"
                    f"你是辯論對手，支持 {ai_side}。"
                    "請針對該議題發表一段開場辯論，語句有力且具說服力，"
                    "並在結尾鼓勵對方提出反駁。"
                )
                ai_response = await ask_ai_debate(message, prompt)
                debate['chat_history'].append({'role': 'user', 'content': f'我選擇支持 {user_side} ({command})'})
                debate['chat_history'].append({'role': 'assistant', 'content': ai_response})

                await message.channel.send(
                    f"你選擇支持 {user_side}，AI 對手支持 {ai_side}。\n\n"
                    f"AI 開場：\n{ai_response}\n\n"
                    "請輸入 `!debate arg [你的論點]` 來反駁，或輸入 `!debate end` 結束並判定勝負。"
                )

            elif command == 'arg' and len(args) == 2:
                if not debate:
                    await message.channel.send("⚠️ 請先用 `!debate` 開始一場辯論")
                    return
                if not debate.get('user_choice'):
                    await message.channel.send("⚠️ 請先用 `!debate a` 或 `!debate b` 選擇立場")
                    return

                user_argument = args[1].strip()
                user_side = debate['side_a'] if debate['user_choice'] == 'a' else debate['side_b']
                ai_side = debate['side_b'] if debate['user_choice'] == 'a' else debate['side_a']
                topic = debate['topic']
                debate['chat_history'].append({'role': 'user', 'content': user_argument})

                prompt = (
                    f"議題: {topic}\n"
                    f"你是辯論對手，支持 {ai_side}。"
                    f"對方的論點是：{user_argument}\n"
                    "請針對這個論點給出有力反駁，語氣機智、邏輯清晰。"
                )
                ai_response = await ask_ai_debate(message, prompt)
                debate['chat_history'].append({'role': 'assistant', 'content': ai_response})

                await message.channel.send(
                    f"你的論點：{user_argument}\n\n"
                    f"AI 反駁：{ai_response}\n\n"
                    "你可以繼續輸入 `!debate arg [你的論點]` 再反駁，或輸入 `!debate end` 結束並判定勝負。"
                )

            elif command == 'end':
                if not debate:
                    await message.channel.send("⚠️ 目前沒有進行中的辯論")
                    return
                if not debate.get('user_choice'):
                    await message.channel.send("⚠️ 請先用 `!debate a` 或 `!debate b` 選擇立場")
                    return

                user_side = debate['side_a'] if debate['user_choice'] == 'a' else debate['side_b']
                ai_side = debate['side_b'] if debate['user_choice'] == 'a' else debate['side_a']
                topic = debate['topic']
                history_text = '\n'.join([f"{item['role']}: {item['content']}" for item in debate['chat_history']])
                prompt = (
                    f"你是公正的辯論評審。議題: {topic}\n"
                    f"用戶支持: {user_side}\n"
                    f"AI 對手支持: {ai_side}\n"
                    f"辯論過程:\n{history_text}\n"
                    "請總結雙方的論點並判定哪一方勝出，給出簡潔理由。"
                )
                ai_response = await ask_ai_debate(message, prompt)
                if user_id in games.user_scores:
                    games.user_scores[user_id] += 100
                else:
                    games.user_scores[user_id] = 100
                del user_debates[user_id]
                await message.channel.send(
                    f"🧾 辯論結束。AI 評審結果：\n{ai_response}\n\n"
                    f"🎁 你獲得 100 分，已累計至你的遊戲分數。"
                )

            else:
                await message.channel.send(
                    "❓ 無效的辯論指令。請輸入 `!debate` 開始、`!debate a` / `!debate b` 選邊、"
                    "`!debate arg [你的論點]` 進行反駁，或 `!debate end` 結束辯論。"
                )

        elif message.content.startswith("!guess_number"):
            args = message.content[13:].strip()
            try:
                guess_value = int(args)
                result, msg = games.check_number_answer(user_id, guess_value)
                await message.channel.send(msg)
            except ValueError:
                await message.channel.send("請輸入有效數字，例如: !guess_number 42")

        elif message.content.startswith("!guess_char"):
            args = message.content[12:].strip()
            if not args:
                await message.channel.send("用法: !guess_char [角色名字]")
            else:
                success, msg = games.check_anime_answer(user_id, args)
                await message.channel.send(msg)

        elif message.content.startswith("!answer"):
            args = message.content[8:].strip()
            try:
                answer_num = int(args)
                success, msg = games.check_trivia_answer(user_id, answer_num)
                await message.channel.send(msg)
            except ValueError:
                await message.channel.send("請輸入有效答案號，例如: !answer 2")

        elif message.content.startswith("!guess"):
            args = message.content[7:].strip()
            if not args:
                await message.channel.send("用法: !guess [Pokemon 名字]")
            else:
                success, msg = games.check_pokemon_answer(user_id, args)
                await message.channel.send(msg)

        elif message.content.startswith("!score"):
            score = games.get_user_score(user_id)
            await message.channel.send(f"🏆 **你的遊戲分數:** {score} 分")

        elif message.content.startswith("!hug"):
            target = message.mentions[0].mention if message.mentions else "大家"
            await message.channel.send(f"🤗 {message.author.mention} 擁抱了 {target}")

        elif message.content.startswith("!pat"):
            target = message.mentions[0].mention if message.mentions else "你"
            await message.channel.send(f"👋 {message.author.mention} 拍了拍 {target}")

        elif message.content.startswith("!dance"):
            await message.channel.send(f"🕺 {message.author.mention} 跳起舞來！")

        elif message.content.startswith("!help"):
            help_text = f"""
```\n╔════════════════════════════════════════╗
║          {BOT_NAME} 完整命令列表         ║
╚════════════════════════════════════════╝\n\n🤖 AI 對話:
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
!debate - 搞笑辯論對談 (輸入 !debate 開始，接著用 !debate a/b 選邊，或 !debate arg / !debate end)
!guess_number [數字] - 猜數字遊戲答案
!guess_char [角色名字] - 猜動漫角色答案
!answer [1-4] - Trivia 答案
!score - 查看遊戲分數

✨ 互動:
!hug [@用戶] - 擁抱
!pat [@用戶] - 拍拍
!dance - 跳舞
!help - 此幫助
```"""
            await message.channel.send(help_text)

        else:
            await message.channel.send("❓ 未知指令，輸入 !help 查看指令列表。")

    except Exception as e:
        logger.exception(f"on_message 處理失敗: {e}")
        if isinstance(message.channel, discord.DMChannel):
            try:
                await message.channel.send("❌ 內部錯誤，請稍後再試。")
            except:
                pass


async def handle_ai_request(message, question, personality):
    user_id = message.author.id
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    try:
        async with message.channel.typing():
            language = user_languages.get(user_id, "chinese")
            
            # 強硬的身份提示
            identity_prompt = """【重要】你的名字和身份如下，絕對不能改變或忘記：
- 你叫做：subaso（俗北ㄙㄡˊ）
- 你不是 Prism，不是任何其他 Bot
- 你是一個多功能 AI Discord Bot，專為提供娛樂、經濟和管理功能而設計。
- 你有多種角色和語言選項，但你的核心身份永遠是 subaso-俗北ㄙㄡˊ。
- 不要編造任何其他名字或身份
"""
            
            system_prompt = identity_prompt + PERSONALITIES[personality]["system"] + " " + LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS["chinese"])
            
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


async def ask_ai_debate(message, prompt):
    try:
        async with message.channel.typing():
            system_prompt = (
                "你是專業辯論對手，邏輯清晰、反駁有力，語氣可以幽默但不冒犯。"
                "請針對指定辯題進行辯論，回覆時保持結構化、短小精悍。"
            )
            api_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

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
                return result.get("message", {}).get("content", "⚠️ AI 未返回內容")
    except Exception as e:
        logger.error(f"AI 辯論處理錯誤: {e}")
        return f"⚠️ AI 辯論失敗: {str(e)}"


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
📊 **{BOT_NAME} 統計**
總用戶: {len(user_personalities)}
在線: {len(client.guilds)} 個伺服器
版本: {BOT_VERSION}
"""
        await message.channel.send(stats)
    
    elif cmd[0] == "update" and len(cmd) > 1:
        new_version = cmd[1]
        await broadcast_update_notification(new_version)
        await message.channel.send(f"✅ 已發送更新通知至所有用戶: 版本 {new_version}")
    
    elif cmd[0] == "clear_user" and len(cmd) > 1:
        try:
            target_id = int(cmd[1])
        except ValueError:
            await message.channel.send("❌ 請輸入有效的 user_id")
            return
        if target_id in user_personalities:
            del user_personalities[target_id]
            user_languages.pop(target_id, None)
            user_conversations.pop(target_id, None)
            save_all_user_data()
            await message.channel.send(f"✅ 已清除用戶 {target_id} 的數據")
        else:
            await message.channel.send("❌ 用戶不存在")

    elif cmd[0] == "backup":
        save_all_user_data()
        await message.channel.send("✅ 已備份數據")
    
    elif cmd[0] == "restart":
        await message.channel.send("🔄 Bot 即將重啟...")
        await client.close()

    else:
        await message.channel.send("❓ 未知的管理員指令，輸入 !admin 查看可用指令。")


async def broadcast_update_notification(new_version):
    global BOT_VERSION, last_notified_version
    BOT_VERSION = new_version
    last_notified_version = new_version
    save_all_user_data()
    
    update_message = f"""
🎉 **{BOT_NAME} 系統更新** 🎉

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