# 🤖 Discord AI 聊天助手機器人

> 支援 5 種 AI 角色、多語言回答、連續對話、實時版本更新

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blueviolet)

## 📋 快速目錄

| 章節 | 內容 |
|------|------|
| [⚡ 功能特色](#⚡-功能特色) | Bot 的所有功能 |
| [📦 環境要求](#📦-環境要求) | 安裝前需要準備什麼 |
| [🚀 快速開始](#🚀-快速開始) | 5 分鐘安裝指南 |
| [⚙️ 詳細配置](#️-詳細配置) | 各種設定選項 |
| [💬 完整命令](#💬-完整命令) | 所有可用命令 |
| [🎭 AI 角色詳解](#🎭-ai-角色詳解) | 5 種角色的差異 |
| [📖 實戰教學](#📖-實戰教學) | 使用範例和技巧 |
| [🌍 多語言支援](#🌍-多語言支援) | 語言切換方法 |
| [👨‍💼 管理員功能](#👨‍💼-管理員功能) | 版本管理、統計等 |
| [❓ 常見問題](#❓-常見問題) | 問題解答 |
| [🔧 故障排除](#🔧-故障排除) | 遇到問題？看這裡 |

---

## ⚡ 功能特色

### 🎭 5 種 AI 角色
- **✅ 閒談** - 友善、幽默的日常聊天
- **🔢 數理** - 數學、科學、邏輯問題專家
- **📚 語文** - 語言、文學、寫作指導
- **💻 程式** - 編程、技術問題解決
- **🏠 家務** - 生活、烹飪、清潔建議

### ✨ 核心功能
| 功能 | 說明 |
|------|------|
| 🔄 **連續對話** | AI 記得對話歷史，支援多輪交互 |
| 🌍 **多語言** | 支援繁體中文、英文、日文、韓文、西班牙文 |
| 📝 **數據保存** | 自動保存用戶偏好和對話記錄 |
| 🔔 **版本更新** | 實時推送更新通知給所有用戶 |
| ⚡ **本地 AI** | 使用 Ollama，無需付費 API，隱私有保障 |
| 💾 **對話記憶** | 默認保留最近 10 輪對話 |

---

## 📦 環境要求

### 必需軟件
| 軟件 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 程式運行 |
| **Ollama** | 最新版 | 本地 AI 模型 |
| **Discord Token** | - | Bot 認證 |

### 必需 Python 套件
```
discord.py>=2.0.0
python-dotenv
aiohttp
httpx
```

### 系統資源建議
- **CPU**: 雙核心以上
- **RAM**: 8GB+ (推薦 16GB)
- **磁盤**: 15GB+ (用於 Ollama 模型)

---

## 🚀 快速開始

### ⏱️ 預計時間：5-10 分鐘

### 步驟 1️⃣ 安裝 Ollama
```bash
# 1. 下載 Ollama (Windows/Mac/Linux 都支援)
# https://ollama.ai

# 2. 安裝後，在終端拉取模型
ollama pull gpt-oss:120b-cloud

# 3. 測試 Ollama 是否運行
curl http://localhost:11434/api/tags
```

### 步驟 2️⃣ 安裝 Python 套件
```powershell
# 在項目資料夾中執行
pip install -r requirements.txt
```

### 步驟 3️⃣ 獲取 Discord Bot Token
1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 **「New Application」**
3. 給你的應用取個名字 (例: `AI Chat Bot`)
4. 左側選 **「Bot」** → 點擊 **「Add Bot」**
5. 在 **「TOKEN」** 下方點擊 **「Copy」**

### 步驟 4️⃣ 配置 `.env` 文件
在項目根目錄創建或編輯 `設定.env`：
```env
# 必需 - Discord Token
DISCORD_TOKEN=你複製的Token_粘貼這裡

# 可選 - 如無需修改可保留默認值
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:120b-cloud
ADMIN_IDS=你的Discord_ID,另一個管理員_ID
```

**如何獲取你的 Discord ID?**
- 在 Discord 啟用開發者模式: 用戶設置 → 進階 → 開發者模式 ✓
- 右鍵點擊你的用戶名 → 複製用戶 ID

### 步驟 5️⃣ 邀請 Bot 到伺服器
1. 在 Developer Portal 選 **「OAuth2」** → **「URL Generator」**
2. **Scopes** 選擇：`bot`
3. **Permissions** 勾選：
   - ✓ Send Messages
   - ✓ Read Messages/View Channels
   - ✓ Read Message History
4. 複製下方生成的 URL，在瀏覽器打開邀請 Bot

### 步驟 6️⃣ 啟動 Bot
```powershell
# 方法 1: 直接運行
python bot.py

# 方法 2: 使用自定義入口 (如果有 run.py)
python run.py
```

✅ 完成！Bot 現在應該已連接到 Discord

---

## ⚙️ 詳細配置

### 環境變數詳解

| 變數 | 必需 | 默認值 | 說明 |
|------|------|--------|------|
| `DISCORD_TOKEN` | ✅ | - | Discord Bot Token |
| `OLLAMA_BASE_URL` | ❌ | `http://localhost:11434` | Ollama API 地址 |
| `OLLAMA_MODEL` | ❌ | `gpt-oss:120b-cloud` | 使用的 AI 模型 |
| `ADMIN_IDS` | ❌ | 空 | 管理員 Discord ID (逗號分隔) |

### 推薦 Ollama 模型

| 模型 | 大小 | 速度 | 質量 | 推薦指數 |
|------|------|------|------|---------|
| **gpt-oss:120b-cloud** | 120B 雲端 | 高品質 | 優秀 | ⭐⭐⭐⭐⭐ |
| `gpt-oss:120b-cloud` | 120B 雲端 | 高品質 | 優秀 | ⭐⭐⭐⭐⭐ |
| `gemma2:2b` | 1.6GB | 最快 | 良好 | ⭐⭐⭐⭐ |
| `llama2` | 3.8GB | 中等 | 優秀 | ⭐⭐⭐⭐ |
| `mistral` | 4.1GB | 中等 | 優秀 | ⭐⭐⭐⭐ |

```bash
# 拉取模型的命令
ollama pull gpt-oss:120b-cloud
ollama pull gemma2:2b
ollama pull llama2
ollama pull mistral
```

### 高級配置

#### 修改對話歷史長度
編輯 `bot.py`，找到第 100 多行的 `MAX_HISTORY`：
```python
MAX_HISTORY = 10  # 改為你想要的值，例: 20
```

#### 添加自定義 AI 角色
編輯 `bot.py` 中的 `PERSONALITIES` 字典 (約第 80 行)：
```python
PERSONALITIES = {
    "你的角色": {
        "prefix": "custom",
        "system": "我是一個...的角色。" # 詳細的系統提示
    },
    # 其他角色...
}
```

---

## 💬 完整命令

### 用戶命令

#### 基本命令
| 命令 | 說明 | 示例 | 優先級 |
|------|------|------|--------|
| `!ask 問題` | 詢問 AI 問題（支持連續對話）| `!ask 2+2等於多少？` | ⭐⭐⭐⭐⭐ |
| `!mode [角色]` | 查看/切換 AI 角色 | `!mode 程式` | ⭐⭐⭐⭐⭐ |
| `!lan [語言]` | 查看/切換回答語言 | `!lan english` | ⭐⭐⭐⭐ |
| `!clear` | 清除對話歷史 | `!clear` | ⭐⭐⭐ |
| `!deleteall` | **完全刪除**所有數據和消息 | `!deleteall` | ⭐⭐ |
| `!guide` | 顯示快速入門指南 | `!guide` | ⭐⭐⭐ |
| `!help` | 顯示完整命令幫助 | `!help` | ⭐⭐⭐⭐ |

#### 工作流範例
```
1. !mode 程式           # 切換到程式角色
2. !lan english         # 設定英文回答
3. !ask How to loop?    # 提問
4. !ask Can you show example?  # 連續提問（AI 記得上文）
5. !clear               # 清除對話
```

### 管理員命令 👨‍💼

> ⚠️ 只有 `ADMIN_IDS` 中的用戶可以使用

| 命令 | 說明 | 示例 |
|------|------|------|
| `!admin` | 顯示管理員命令幫助 | `!admin` |
| `!admin stats` | 查看統計數據 | `!admin stats` |
| `!admin backup` | 手動備份所有數據 | `!admin backup` |
| `!admin update [版本號]` | **發送版本更新通知**給所有用戶 | `!admin update 1.0.1` |
| `!admin clear_user [用戶ID]` | 清除特定用戶數據 | `!admin clear_user 123456` |
| `!admin restart` | 重啟 Bot | `!admin restart` |

#### 版本更新流程
```powershell
# 1. 管理員執行更新命令
!admin update 1.0.1

# 2. 所有在線用戶收到通知：
# 🎉 **系統更新通知** 🎉
# ✅ 已更新成 **1.0.1**

# 3. 版本信息自動保存到 user_data.json
```

---

## 🎭 AI 角色詳解

### 1️⃣ 閒談 (デフォルト)
**性格**: 友善、幽默、親切、隨和
**最佳用途**: 日常聊天、娛樂、減壓
**回答風格**: 自然對話、表情豐富

```markdown
!mode 閒談
!ask 今天天氣怎樣呢？

【閒談】 嘿！天氣真是...
```

### 2️⃣ 數理 (專業)
**性格**: 邏輯清晰、嚴謹、循序漸進
**最佳用途**: 數學、物理、化學、邏輯題
**回答風格**: 步驟詳細、公式推導

```markdown
!mode 數理
!ask 求解方程: 2x + 5 = 13

【數理】
步驟 1: 2x + 5 = 13
步驟 2: 2x = 13 - 5 = 8
步驟 3: x = 8 ÷ 2 = 4
```

### 3️⃣ 語文 (文學)
**性格**: 深思熟慮、文學感強、詳細
**最佳用途**: 語法、寫作、文學分析、詞彙
**回答風格**: 例子豐富、逐層遞進

```markdown
!mode 語文
!ask 「然而」和「但是」有什麼區別？

【語文】
1. 「但是」：口語化、直接對比...
2. 「然而」：書面語、轉折更深層...
```

### 4️⃣ 程式 (技術)
**性格**: 實用、技術導向、問題解決者
**最佳用途**: 編程、除錯、技術問題、算法
**回答風格**: 代碼示例、最佳實踐

```markdown
!mode 程式
!ask 如何在 Python 中迴圈列表？

【程式】
方法 1:
```python
for item in my_list:
    print(item)
```

### 5️⃣ 家務 (生活)
**性格**: 貼心、實用、友善、經驗豐富
**最佳用途**: 烹飪、清潔、整理、生活建議
**回答風格**: 步驟清晰、實用技巧

```markdown
!mode 家務
!ask 怎樣快速清潔廚房？

【家務】
快速清潔步驟 (10 分鐘):
1. 清除大件物品...
```

---

## 🌍 多語言支援

Bot 支援 5 種語言！

### 支援的語言

| 代碼 | 語言 | 命令 |
|------|------|------|
| `chinese` | 繁體中文 | `!lan chinese` |
| `english` | English | `!lan english` |
| `japanese` | 日本語 | `!lan japanese` |
| `korean` | 한국어 | `!lan korean` |
| `spanish` | Español | `!lan spanish` |

### 使用方式
```markdown
# 查看當前語言
!lan

# 切換語言
!lan english

# 然後提問（AI 將用英文回答）
!ask How are you?
```

### 示例：多語言同一問題
```
!mode 程式
!lan english
!ask What is Python?

→ 【程式】 Python is a high-level programming language...

!lan japanese
!ask What is Python?

→ 【程式】 Pythonは、高級プログラミング言語です...
```

---

## 👨‍💼 管理員功能

### 設定管理員

編輯 `設定.env`：
```env
# 多個管理員用逗號分隔
ADMIN_IDS=123456789,987654321
```

**如何獲取你的 Discord ID?**
1. 右鍵點擊你的用戶名
2. 選 「複製用戶 ID」
3. 貼到 `ADMIN_IDS` 中

### 版本管理系統 🔔

#### 更新流程
```
1. 管理員執行: !admin update 1.0.1
2. Bot 自動發送通知給所有用戶
3. 每個用戶在 DM 中收到："✅ 已更新成 1.0.1"
4. 版本信息保存在 user_data.json
```

#### 更新通知內容
```
🎉 **系統更新通知** 🎉

✅ 已更新成 **1.0.1**

新版本已推送，感謝使用！
```

### 監控與統計

```markdown
# 查看 Bot 統計
!admin stats

→ 📊 **Bot 統計**
  總用戶: 42
  在線: 5 個伺服器
```

### 數據管理

#### 自動備份
- 每次執行 `!admin backup` 自動保存
- 用戶數據實時保存到 `user_data.json`
- 對話歷史保存在內存中

#### 清除用戶數據
```markdown
!admin clear_user 123456789

→ ✅ 已清除用戶 123456789 的數據
```

---

## 📖 實戰教學

### 場景 1️⃣: 學習 Python

```markdown
1️⃣ 切換角色和語言
!mode 程式
!lan chinese

2️⃣ 開始提問
!ask 什麼是函數？

3️⃣ 進一步討論（連續對話）
!ask 能給我一個例子嗎？

4️⃣ 嘗試另一種解釋
!ask 用簡單的詞彙再解釋一遍

5️⃣ 清除並開始新話題
!clear
!ask 什麼是類 (class)？
```

### 場景 2️⃣: 烹飪建議

```markdown
1️⃣ 選擇家務角色
!mode 家務

2️⃣ 詢問
!ask 如何煮蛋最快？

3️⃣ 追問細節
!ask 如果我要同時煮 10 個呢？

4️⃣ 切換語言重新詢問
!lan english
!ask Can you give me tips for batch cooking?
```

### 場景 3️⃣: 多角色對比

```markdown
# 同一個問題，不同角色的回答

!mode 閒談
!ask 什麼是 AI？
→【閒談】 嗯，AI 就是讓機器聰明起來...

!mode 數理
!ask 什麼是 AI？
→【數理】 AI 使用數學算法...

!mode 程式
!ask 什麼是 AI？
→【程式】 AI 涉及機器學習、神經網絡...
```

---

## ❓ 常見問題

### Q1: Bot 不回應怎麼辦？
**A**: 檢查清單：
- [ ] Ollama 是否在運行？ (在終端輸入 `ollama list`)
- [ ] Discord Token 是否正確？
- [ ] Bot 是否有 "Send Messages" 權限？
- [ ] 你是否在 DM 中發送消息？

### Q2: 為什麼回答很慢？
**A**: 正常現象。本地 Ollama 比雲 API 慢。
- 使用推薦模型: `gpt-oss:120b-cloud`
- 升級 CPU/RAM
- 減少對話歷史長度

### Q3: 如何更換 AI 模型？
**A**: 編輯 `設定.env`：
```env
OLLAMA_MODEL=gpt-oss:120b-cloud
```
然後重啟 Bot

### Q4: 可以自定義 AI 角色嗎？
**A**: 可以！編輯 `bot.py` 的 `PERSONALITIES` 字典並重啟

### Q5: 用戶數據會被保存嗎？
**A**: 是的：
- 用戶偏好 (角色、語言) → `user_data.json`
- 對話歷史 → 內存 (最多 10 輪)
- 重啟 Bot 後內存數據會清空

### Q6: 如何刪除我的所有數據？
**A**: 在 DM 中執行：
```
!deleteall
```
此命令會：
- ❌ 刪除你的所有 Bot 消息
- ❌ 清除你的對話歷史
- ❌ 移除你的用戶偏好設定

### Q7: 支援群組聊天嗎？
**A**: 目前只支援 DM。群組消息會提示："請在私信中使用命令！"

### Q8: Bot 的隱私怎樣？
**A**: 隱私有保障：
- 所有處理在本地完成
- 不連接任何外部服務（除了 Discord）
- 用戶數據只保存在本機

---

## 🔧 故障排除

### ❌ 模型 404 錯誤
**症狀**:
```
❌ 發生錯誤: Ollama API returned status 404
```

**解決方案**:
```powershell
# 1. 確認 Ollama 正在運行
Get-Process ollama

# 2. 檢查已安裝的模型
ollama list

# 3. 如果模型不見，重新拉取
ollama pull gpt-oss:120b-cloud

# 4. 測試 API 是否正常
curl http://localhost:11434/api/tags

# 5. 如果還是不行，嘗試輕量級模型
# 編輯設定.env:
# OLLAMA_MODEL=gemma2:2b
```

### ❌ Socket 綁定錯誤
**症狀**:
```
ERROR: bind: Only one usage of each socket address (Addr:(0,0,0,0,11434))
```

**原因**: Ollama 已在後台運行

**解決方案**:
```powershell
# Ollama 已在背景執行，直接運行 Bot
python bot.py

# 或者殺死現有進程重啟
# Windows:
Get-Process ollama | Stop-Process
ollama serve

# Mac/Linux:
killall ollama
ollama serve
```

### ❌ 缺少模組
**症狀**:
```
ModuleNotFoundError: No module named 'discord'
```

**解決方案**:
```powershell
# 確保在項目目錄中
pip install -r requirements.txt

# 或手動安裝
pip install discord.py python-dotenv aiohttp httpx
```

### ❌ Bot 沒有連接到 Discord
**症狀**: 啟動 Bot 後，Discord 中看不到 Bot 上線

**檢查清單**:
```powershell
# 1. 驗證 Token
# 編輯 設定.env，確保 DISCORD_TOKEN 正確

# 2. 檢查權限
# - Bot 是否邀請到伺服器？
# - Bot 是否有 "Send Messages" 權限？

# 3. 查看終端錯誤訊息
# 如有紅色錯誤，複製錯誤訊息搜索解決方案

# 4. 查看 Discord 開發者日誌
# 在 Discord 終端用: Ctrl+Shift+I 打開開發者工具
```

### ❌ 超時錯誤
**症狀**:
```
❌ 發生錯誤: Request timeout...
```

**可能原因**:
1. Ollama 伺服器超載
2. 模型太大或 RAM 不足
3. 網絡連接問題

**解決方案**:
```powershell
# 1. 等待一會再試

# 2. 檢查 RAM 使用
Get-Process ollama | Select-Object WorkingSet

# 3. 改用更輕量的模型
# 編輯設定.env:
# OLLAMA_MODEL=gemma2:2b

# 4. 減少對話歷史
# 編輯 bot.py: MAX_HISTORY = 5
```

### ❌ AI 回答重複或無意義
**症狀**: AI 重複同樣的句子或回答不相關的內容

**解決方案**:
```markdown
# 1. 清除對話歷史
!clear

# 2. 嘗試詢問更具體的問題
# ✗ 錯誤: !ask 什麼？
# ✓ 正確: !ask Python 中如何創建列表？

# 3. 改用不同的 AI 角色
!mode 程式
```

### ❌ Windows 編碼問題
**症狀**: 日誌或輸出中出現亂碼

**解決方案**: 此問題已在 `bot.py` 第 15 行修復，無需額外操作

### ❌ 數據文件損毀
**症狀**: 
```
JSONDecodeError: Expecting value...
```

**解決方案**:
```powershell
# 1. 備份現有文件
Copy-Item user_data.json user_data.json.bak

# 2. 刪除損毀文件
Remove-Item user_data.json

# 3. 重啟 Bot（會重建文件）
python bot.py
```

---

## 📁 項目結構

```
dcard_bot/
├── bot.py                 # 主程式
├── run.py                 # 啟動入口
├── requirements.txt       # Python 依賴
├── 設定.env               # 環境變數設定
├── user_data.json         # 用戶數據 (自動生成)
├── README.md              # 說明文檔
├── logs/                  # 日誌文件夾
│   └── bot_20240509.log   # 今日日誌
└── Dockerfile            # Docker 容器化
```

---

## 🐳 Docker 部署

```bash
# 構建容器
docker build -t discord-bot .

# 運行容器
docker run -d --name discord-bot \
  -e DISCORD_TOKEN=你的_token \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  discord-bot
```

---

## 📞 獲取幫助

遇到問題？

1. **查看日誌**: `logs/bot_*.log`
2. **閱讀本文檔的故障排除部分**
3. **在 Discord 中嘗試**: `!help` 或 `!guide`
4. **聯絡開發者** (如適用)

---

## 📄 許可證

此項目採用 MIT 許可證。詳見項目根目錄的 LICENSE 文件。

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 🎉 更新日誌

### v1.0.0 (2024-05-09) 🎊
- ✅ 基礎功能完成
- ✅ 5 種 AI 角色
- ✅ 多語言支援
- ✅ 版本管理系統
- ✅ 管理員命令
- ✅ 用戶數據持久化

---

**祝你使用愉快！如有任何建議，歡迎反饋！** 🚀
    },
    # ... 其他角色
}
```

---

## 📞 支援與回報

如遇到問題：
1. 查看 [故障排除](#故障排除) 部分
2. 檢查終端錯誤訊息
3. 確認所有設定無誤

---

**最後更新**: 2026-05-02  
**版本**: 1.0  
**許可**: MIT
