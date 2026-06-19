# subaso-俗北ㄙㄡˊ

> 一個以 Discord 私訊為介面的本地 AI 聊天機器人。支援 5 種角色、連續對話、語言切換與管理員指令。

## 這個專案現在只保留一個啟動入口
- 主啟動檔：`entrypoint.sh`
- 唯一說明文件：`README.md`

## 1. 功能簡介
- 5 種 AI 角色：閒談、數理、語文、程式、家務
- 本地 Ollama 模型推論，隱私與成本較可控
- Discord 私訊互動、角色切換、語言切換、對話記憶
- 管理員指令、資料備份、版本更新通知與遊戲互動整合

## 2. 安裝需求
- Python 3.8+
- Ollama（推薦安裝後拉取 `qwen2.5:7b-instruct`）
- Discord Bot Token

## 3. 快速開始

### Step 1：安裝依賴
```powershell
cd "C:\Users\User\Downloads\python 學習檔案\dcard_bot"
pip install -r requirements.txt
```

### Step 2：設定環境變數
編輯 `設定.env`：
```env
DISCORD_TOKEN=你的_Token
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct
ADMIN_IDS=你的Discord_ID
```

### Step 3：啟動專案
在 Git Bash / WSL / Linux / macOS：
```bash
sh entrypoint.sh
```

在 Windows PowerShell：
```powershell
bash entrypoint.sh
```

> 這個啟動檔會自動完成：安裝套件、檢查 Ollama、拉取模型、啟動 Bot。

## 4. 測試方式
在 Discord 私訊中輸入：
```text
!help
!mode 閒談
!ask 你好
```

## 5. 常用指令
| 指令 | 說明 |
|------|------|
| `!mode [角色]` | 切換角色 |
| `!ask [問題]` | 提問 |
| `!lan [語言]` | 切換語言 |
| `!pokemon` / `!trivia` / `!anime` / `!number` | 啟動遊戲 |
| `!guess [名字]` / `!guess_char [名字]` / `!guess_number [數字]` | 回答遊戲 |
| `!score` | 查詢遊戲分數 |
| `!admin stats` / `!admin logs [數量]` / `!admin welcome [訊息]` / `!admin leave [訊息]` | 管理員功能 |
| `!admin custom add [命令] [回覆]` / `!admin custom list` / `!admin custom delete [命令]` | 自訂回覆與管理紀錄 |
| `!admin backup` / `!admin update [版本]` / `!admin clear_user [user_id]` | 資料備份與管理操作 |
| `!clear` | 清除對話 |
| `!guide` | 顯示指南 |
| `!help` | 顯示幫助 |

## 6. 常見問題
### Bot 沒有回應
1. 檢查 `DISCORD_TOKEN` 是否填對
2. 確認 Ollama 已啟動：`ollama list`
3. 確認 Bot 有 Discord 私訊權限

### Ollama 404 / 模型不存在
```powershell
ollama pull qwen2.5:7b-instruct
```

### Python 套件缺少
```powershell
pip install -r requirements.txt
```

## 7. 專案結構
```text
.
├── entrypoint.sh      # 唯一主啟動入口
├── bot.py             # 核心 Bot 程式
├── 設定.env            # Discord / Ollama 設定
├── user_data.json     # 使用者資料
└── logs/              # 執行紀錄
```

## 8. 版本資訊
- 版本：1.0
- 名稱：subaso-俗北ㄙㄡˊ

祝你使用愉快！
