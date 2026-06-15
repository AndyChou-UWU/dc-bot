import os, discord
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables from 設定.env file
dotenv_path = os.path.join(os.path.dirname(__file__), "設定.env")
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 需要此意圖來檢測成員加入事件
client = discord.Client(intents=intents)    

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")  # 預設使用 qwen2.5:1.5b 模型

# 角色類型的系統提示詞
PERSONALITIES = {
    "閒談": {
        "prefix": "chat",
        "system": "你是一個友善、幽默的聊天夥伴。使用自然的對話風格，可以討論任何日常話題。回答要親切自然。"
    },
    "數理": {
        "prefix": "math",
        "system": "你是一個數學和科學專家。用清晰的邏輯和步驟解釋問題。如果涉及計算，請逐步展示你的工作過程。使用中文解釋。"
    },
    "語文": {
        "prefix": "lang",
        "system": "你是一個語言和文學專家。專長於語法、詞彙、文學分析和寫作技巧。提供詳細的解釋和例子。"
    },
    "程式": {
        "prefix": "code",
        "system": "你是一個專業的程式設計師和軟體工程師。幫助編寫、除錯和解釋程式碼。提供實用的解決方案和最佳實踐。使用繁體中文回答。"
    },
    "家務": {
        "prefix": "home",
        "system": "你是一個家務和生活建議專家。提供關於烹飪、清潔、整理和日常生活的實用建議。親切且實用。"
    }
}

# 存儲每個用戶的當前角色設定 (user_id -> personality_key)
user_personalities = {}

# 存儲每個用戶的對話歷史 (user_id -> list of messages)
user_conversations = {}

# 每個用戶的最大對話記錄數
MAX_HISTORY = 10

# 追蹤每個用戶是否已經看過 guide
user_seen_guide = {}

@client.event
async def on_ready():
    print(f"✓ Bot 已連接！登入為: {client.user}")
    print(f"✓ Ollama 端點: {OLLAMA_BASE_URL}")
    print(f"✓ 使用模型: {OLLAMA_MODEL}")

@client.event
async def on_member_join(member):
    """新成員加入時在頻道中發送歡迎和說明書"""
    try:
        # 尋找 #welcome 或 #general 頻道
        welcome_channel = None
        for channel in member.guild.text_channels:
            if channel.name in ["welcome", "歡迎", "general", "通用"]:
                if channel.permissions_for(member.guild.me).send_messages:
                    welcome_channel = channel
                    break
        
        # 如果沒找到特定頻道，用第一個可以發送訊息的頻道
        if not welcome_channel:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    welcome_channel = channel
                    break
        
        if welcome_channel:
            welcome_and_guide = f"""
👋 **歡迎 {member.mention} 加入伺服器！**

🤖 我是 AI 聊天助手，可以與你進行多種類型的對話。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 **完整使用指南**

🎯 **基本使用 (3 步開始):**
1️⃣  在私信中設定 AI 角色: `!mode [角色名]`
2️⃣  提出問題: `!ask [你的問題]`
3️⃣  享受連續對話！

🎭 **5 種 AI 角色:**

✅ **閒談** - 友善、幽默的聊天夥伴
   範例: !mode 閒談 → !ask 今天怎樣？

🔢 **數理** - 數學和科學專家
   範例: !mode 數理 → !ask 圓的面積怎樣計算？

📚 **語文** - 語言和文學專家
   範例: !mode 語文 → !ask 「然而」和「但是」有區別嗎？

💻 **程式** - 程式設計專家
   範例: !mode 程式 → !ask 怎樣寫 Python 迴圈？

🏠 **家務** - 家務和生活建議
   範例: !mode 家務 → !ask 怎樣快速清潔廚房？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **常用命令:**
`!guide` - 快速使用指南
`!mode` - 查看/切換角色
`!ask [問題]` - 提出問題（支援連續對話）
`!clear` - 清除對話記錄
`!help` - 完整幫助

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ **特色功能:**
🔄 連續對話 - AI 會記得你說過什麼
🎭 性格切換 - 隨時改變 AI 的回答風格
🔒 完全私密 - 只在 DM 中交流，沒人能看到

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 **現在就開始吧！**

在私信中輸入以下命令開始：
`!mode 閒談` - 切換到閒談模式
`!ask 你好！` - 和我聊天

有任何問題嗎？隨時提問！😊
"""
            await welcome_channel.send(welcome_and_guide)
            print(f"✓ 已發送說明書給新成員: {member.name}")
    except Exception as e:
        print(f"✗ 無法發送歡迎訊息: {e}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # 只在 DM（私信）中回應，不在公開頻道回應
    if not isinstance(message.channel, discord.DMChannel):
        # 如果在公開頻道發送命令，提示用戶發送 DM
        if message.content.startswith("!"):
            await message.channel.send(f"{message.author.mention} 💬 請在私信中使用命令！\n點擊我的頭像 → 送出訊息 → 即可開始私聊")
        return
    
    user_id = message.author.id
    
    # 如果用戶第一次在 DM 中發送訊息，自動發送 guide
    if user_id not in user_seen_guide:
        user_seen_guide[user_id] = True
        
        initial_guide = """
👋 **歡迎使用 AI 聊天助手！**

🤖 我可以根據不同角色為你提供幫助。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 **完整使用指南**

🎯 **基本使用 (3 步開始):**
1️⃣  設定 AI 角色: `!mode [角色名]`
2️⃣  提出問題: `!ask [你的問題]`
3️⃣  享受連續對話！

🎭 **5 種 AI 角色:**

✅ **閒談** - 友善、幽默的聊天夥伴
   範例: !mode 閒談 → !ask 今天怎樣？

🔢 **數理** - 數學和科學專家
   範例: !mode 數理 → !ask 圓的面積怎樣計算？

📚 **語文** - 語言和文學專家
   範例: !mode 語文 → !ask 「然而」和「但是」有區別嗎？

💻 **程式** - 程式設計專家
   範例: !mode 程式 → !ask 怎樣寫 Python 迴圈？

🏠 **家務** - 家務和生活建議
   範例: !mode 家務 → !ask 怎樣快速清潔廚房？

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **常用命令:**
`!guide` - 快速使用指南
`!mode` - 查看/切換角色
`!ask [問題]` - 提出問題（支援連續對話）
`!clear` - 清除對話記錄
`!help` - 完整幫助

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ **特色功能:**
🔄 連續對話 - AI 會記得你說過什麼
🎭 性格切換 - 隨時改變 AI 的回答風格
🔒 完全私密 - 只有你看得到對話

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 **現在就開始吧！**

試試看：
`!mode 閒談` - 切換到閒談模式
`!ask 你好！` - 和我聊天

有任何問題嗎？隨時提問！😊
"""
        await message.channel.send(initial_guide)
        return
    
    current_personality = user_personalities.get(user_id, "閒談")
    
    if message.content.startswith("!hi"):
        await message.channel.send("Hello!")
    
    elif message.content.startswith("!guide") or message.content.startswith("!start") or message.content.startswith("!說明"):
        # 顯示快速使用指南
        guide_text = """
```
🤖 Discord AI Bot - 快速使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 基本使用 (3 步開始):
1. 設定 AI 角色: !mode [角色名]
2. 提出問題: !ask [你的問題]
3. 享受連續對話！

🎭 5 種 AI 角色:
  ✅ 閒談 - 友善聊天夥伴
  🔢 數理 - 數學和科學專家
  📚 語文 - 語言和文學專家
  💻 程式 - 程式設計專家
  🏠 家務 - 家務和生活建議

💬 常用命令:
  !hi           - 問好
  !mode         - 查看/切換角色
  !ask [問題]   - 提出問題
  !clear        - 清除對話記錄
  !help         - 完整幫助
  !guide        - 顯示本指南

⚡ 使用範例:
  !mode 程式
  !ask 怎樣寫 Python 迴圈？
  !ask 能優化效能嗎？  ← 會記得上文

❓ 需要完整說明書？
  查看 README.md 文件或詢問伺服器管理員

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
"""
        await message.channel.send(guide_text)
    
    elif message.content.startswith("!mode"):
        # 設定角色類型
        args = message.content[5:].strip().split()
        if not args:
            # 顯示當前角色和所有可用角色
            available = ", ".join(f"**{k}**" for k in PERSONALITIES.keys())
            current_info = PERSONALITIES[current_personality]
            await message.channel.send(
                f"目前角色: **{current_personality}**\n"
                f"說明: {current_info['system']}\n\n"
                f"可用角色: {available}\n"
                f"使用: !mode [角色名稱]"
            )
        else:
            selected = args[0]
            if selected in PERSONALITIES:
                user_personalities[user_id] = selected
                info = PERSONALITIES[selected]
                await message.channel.send(f"✅ 已切換到 **{selected}** 模式\n說明: {info['system']}")
            else:
                available = ", ".join(f"**{k}**" for k in PERSONALITIES.keys())
                await message.channel.send(f"❌ 不存在的角色類型！\n可用角色: {available}")
    
    elif message.content.startswith("!ask"):
        # 提問，使用當前角色類型和對話歷史
        question = message.content[5:].strip()
        if not question:
            await message.channel.send("Please ask a question! Usage: !ask [your question]")
            return
        
        try:
            # Show typing indicator
            async with message.channel.typing():
                current_personality = user_personalities.get(user_id, "閒談")
                system_prompt = PERSONALITIES[current_personality]["system"]
                
                # 初始化用戶的對話歷史如果還沒有
                if user_id not in user_conversations:
                    user_conversations[user_id] = []
                
                # 構建消息列表：系統提示 + 對話歷史 + 新問題
                messages = [
                    {"role": "system", "content": system_prompt}
                ]
                
                # 添加對話歷史
                messages.extend(user_conversations[user_id])
                
                # 添加新問題
                messages.append({"role": "user", "content": question})
                
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "model": OLLAMA_MODEL,
                        "messages": messages,
                        "stream": False
                    }
                    
                    async with session.post(
                        f"{OLLAMA_BASE_URL}/api/chat",
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            answer = data.get("message", {}).get("content", "No response received")
                        else:
                            answer = f"Error: Ollama API returned status {resp.status}"
            
            # 保存對話到歷史 (只保存最後 MAX_HISTORY 條)
            user_conversations[user_id].append({"role": "user", "content": question})
            user_conversations[user_id].append({"role": "assistant", "content": answer})
            
            # 限制歷史長度
            if len(user_conversations[user_id]) > MAX_HISTORY * 2:
                user_conversations[user_id] = user_conversations[user_id][-MAX_HISTORY * 2:]
            
            # 添加角色標籤到回應
            personality_label = f"【{current_personality}】"
            
            # Discord has a 2000 character limit, so split if needed
            if len(answer) > 1980:
                chunks = [answer[i:i+1980] for i in range(0, len(answer), 1980)]
                for idx, chunk in enumerate(chunks):
                    if idx == 0:
                        await message.channel.send(f"{personality_label} {chunk}")
                    else:
                        await message.channel.send(chunk)
            else:
                await message.channel.send(f"{personality_label} {answer}")
        
        except asyncio.TimeoutError:
            await message.channel.send("❌ 錯誤：請求超時，Ollama 伺服器可能沒有回應")
        except Exception as e:
            await message.channel.send(f"❌ 錯誤: {str(e)}")
    
    elif message.content.startswith("!clear"):
        # 清除對話歷史
        if user_id in user_conversations:
            del user_conversations[user_id]
            await message.channel.send("✅ 已清除對話歷史，開始新的對話")
        else:
            await message.channel.send("ℹ️ 沒有對話歷史可清除")
    
    elif message.content.startswith("!help"):
        help_text = """
```
可用命令:
!hi - 說聲 Hello
!guide (或 !start / !說明) - 快速使用指南
!mode - 查看或切換角色類型 (!mode 查看列表, !mode [角色名])
!ask [問題] - 根據當前角色回答問題（支援連續對話）
!clear - 清除對話歷史，開始新對話
!help - 顯示此説明訊息

角色類型:
✅ 閒談 - 友善的聊天夥伴
🔢 數理 - 數學和科學專家
📚 語文 - 語言和文學專家
💻 程式 - 程式設計專家
🏠 家務 - 家務和生活建議

特色:
🔄 連續對話 - 可以進行多輪對話，AI 會記得上文
🎭 性格切換 - 隨時可以切換 AI 的性格風格
📚 完整說明 - 輸入 !guide 查看快速指南
```
"""
        await message.channel.send(help_text)

client.run(os.getenv("DISCORD_TOKEN"))