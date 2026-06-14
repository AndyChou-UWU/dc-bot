import os
import asyncio
import discord
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "設定.env")
load_dotenv(dotenv_path)

# Get environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", "0"))  # Add TEST_CHANNEL_ID to your .env

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✓ Bot 已連接！登入為: {client.user}")
    
    if TEST_CHANNEL_ID > 0:
        try:
            channel = client.get_channel(TEST_CHANNEL_ID)
            if channel:
                await channel.send("🧪 測試訊息 - Bot 發送訊息成功！")
                print(f"✓ 成功發送測試訊息到頻道 {channel.name}")
            else:
                print(f"✗ 找不到頻道 ID: {TEST_CHANNEL_ID}")
        except Exception as e:
            print(f"✗ 發送訊息失敗: {e}")
    else:
        print("⚠ 未設定 TEST_CHANNEL_ID，請在 設定.env 中添加 TEST_CHANNEL_ID=<你的頻道ID>")
    
    await client.close()

@client.event
async def on_error(event, *args, **kwargs):
    print(f"✗ 發生錯誤: {event}")

print("🚀 正在啟動 Discord Bot 測試...")
print(f"Token 是否已加載: {'✓' if DISCORD_TOKEN else '✗'}")

try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    print(f"✗ Bot 啟動失敗: {e}")
