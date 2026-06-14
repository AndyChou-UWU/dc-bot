# 🚀 Discord AI Bot 运行步骤

## 📋 前置检查

```powershell
# 1️⃣ 检查 Python 版本（必须 3.8+）
python --version

# 2️⃣ 检查 Ollama 是否运行（应显示进程）
Get-Process ollama

# 3️⃣ 检查 Ollama 模型是否存在
ollama list
```

---

## ⚙️ 安装依赖

```powershell
# 进入项目目录
cd "C:\Users\User\Downloads\python 學習檔案\dcard_bot"

# 安装所需套件
pip install -r requirements.txt
```

✅ 应该会安装：
- discord.py
- python-dotenv
- aiohttp

---

## 📝 配置 設定.env

打开 `設定.env` 文件，检查以下内容：

```env
# 必填项（没有会报错）
DISCORD_TOKEN=你的_Token_（必须填）

# 推荐配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=Qwen2.5-1.5B-Instruct

# 可选（管理员功能）
ADMIN_IDS=你的Discord_ID
```

**如何获取 Token？**
1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 选择你的 Bot Application
3. 左侧选择 "Bot"
4. 点击 "Copy" 复制 Token
5. 粘贴到 `設定.env` 的 `DISCORD_TOKEN=` 后面

---

## 🎯 运行方式

### 方式 1️⃣: 直接运行（推荐新手）
```powershell
cd "C:\Users\User\Downloads\python 學習檔案\dcard_bot"
python bot.py
```

✅ **优点**：
- 简单直接
- 可以实时看到日志
- 问题时立即显示

❌ **缺点**：
- 关闭终端 Bot 就停止了

---

### 方式 2️⃣: 后台运行（推荐长期运行）

**Windows 用户 - 双击运行：**
```
直接双击 start.bat
```

或手动运行：
```powershell
.\start.bat
```

✅ **优点**：
- 后台运行
- 自动检查依赖和 Ollama
- 关闭终端 Bot 继续运行

✅ 会自动显示：
```
✅ 所有检查完成，正在启动 Bot...
✅ Bot 已在后台启动！
🔍 查看日志: logs\ 文件夹
```

---

### 方式 3️⃣: Python 脚本运行

```powershell
python run.py
```

✅ 跨平台方式

---

## ✅ 验证 Bot 是否启动成功

### 查看终端输出

```
✓ Bot 已連接！登入為: python project#9934
✓ Ollama 端點: http://localhost:11434
✓ 使用模型: Qwen2.5-1.5B-Instruct
```

### 检查日志文件

```powershell
# Windows
dir logs\

# 查看最新日志
type logs\bot_20260502.log
```

---

## 🧪 测试 Bot

### 1️⃣ 在 Discord 中测试

1. 打开 Discord
2. 找到你的 Bot
3. **点击 Bot 头像 → "送出訊息" 或 "Send Message"**
4. 在私信中输入任何文字

### 2️⃣ Bot 应该回复

首次发送时：
```
👋 歡迎使用 AI 聊天助手！

🎭 5 種角色:
✅ 閒談 | 🔢 數理 | 📚 語文 | 💻 程式 | 🏠 家務

📖 使用方法:
`!mode 角色名` - 切換角色 (例: !mode 程式)
`!ask 你的問題` - 提問
...
```

### 3️⃣ 开始使用

在私信中输入：
```
!mode 閒談
```

然后：
```
!ask 你好！
```

Bot 应该回复类似：
```
【閒談】你好！很高興認識你...
```

---

## 📊 常见命令

| 命令 | 说明 | 例子 |
|------|------|------|
| `!mode [角色]` | 切换角色 | `!mode 程式` |
| `!ask [问题]` | 提问 | `!ask Python怎么写循环？` |
| `!clear` | 清除对话 | `!clear` |
| `!guide` | 显示指南 | `!guide` |
| `!help` | 显示帮助 | `!help` |

---

## ❌ 常见问题

### ❌ "未找到 DISCORD_TOKEN"
```
解决: 编辑 設定.env，添加 DISCORD_TOKEN=你的Token
```

### ❌ "Ollama 404 错误"
```
解决:
1. 检查 Ollama 是否运行: Get-Process ollama
2. 检查模型: ollama list
3. 拉取模型: ollama pull Qwen2.5-1.5B-Instruct
```

### ❌ 编码错误/乱码
```
✅ 已修复！重新运行 python bot.py 即可
```

### ❌ Bot 连接不上
```
解决:
1. 检查 Token 是否正确
2. 检查 Bot 是否已邀请到伺服器
3. 检查网络连接
```

---

## 🎯 完整运行流程

```
1️⃣ 打开 PowerShell
   ↓
2️⃣ 进入项目目录
   cd "C:\Users\User\Downloads\python 學習檔案\dcard_bot"
   ↓
3️⃣ 检查配置
   cat 設定.env  # 确认 DISCORD_TOKEN 已填
   ↓
4️⃣ 启动 Bot（三选一）
   
   方式 A - 直接运行:
   python bot.py
   
   方式 B - 后台运行:
   .\start.bat
   
   方式 C - Python 脚本:
   python run.py
   ↓
5️⃣ 等待显示：
   ✓ Bot 已連接！
   ↓
6️⃣ 在 Discord 私信测试
   发送任何消息 → Bot 回复 guide
   ↓
7️⃣ 开始使用
   !mode 角色名
   !ask 你的问题
```

---

## 💡 小贴士

✅ **保存日志** - 日志自动保存到 `logs/` 文件夹
✅ **数据持久化** - 用户数据自动保存到 `user_data.json`
✅ **后台监控** - 可以在后台运行 Bot，继续使用电脑
✅ **定期备份** - 运行 `!admin backup` 备份数据

---

## 🆘 需要帮助？

1. 检查 `logs/` 中的错误日志
2. 阅读 `README_BACKEND.md` 完整文档
3. 运行 `!help` 查看命令

祝你使用愉快！🎉
