# Discord AI Bot 完整使用手册

## 📚 目录
1. [新增功能](#新增功能)
2. [快速开始](#快速开始)
3. [后台功能](#后台功能)
4. [管理员命令](#管理员命令)
5. [使用指南](#使用指南)
6. [故障排除](#故障排除)

---

## ✨ 新增功能

### 🔄 完整的后台系统
- ✅ **日志记录** - 所有操作记录到 logs/ 文件夹
- ✅ **数据持久化** - 用户数据自动保存到 JSON
- ✅ **管理员面板** - 管理员可以管理 Bot 和用户数据
- ✅ **自动重连** - 异常时自动重启
- ✅ **后台运行脚本** - Windows/Linux 后台启动

---

## 🚀 快速开始

### Windows 用户（推荐）
1. **双击运行**: `start.bat`
2. **自动检查**：Ollama、依赖等
3. **后台运行**：Bot 在后台持续运行
4. **查看日志**：打开 `logs/` 文件夹

### 所有平台
```bash
# 方法 1: 直接运行
python bot.py

# 方法 2: 使用后台脚本
python run.py

# Linux 后台运行（使用 nohup）
nohup python bot.py > bot.log 2>&1 &

# Linux 后台运行（使用 screen）
screen -S discord_bot python bot.py
```

---

## 🔙 后台功能详解

### 📝 日志系统
- **位置**: `logs/bot_YYYYMMDD.log`
- **内容**: 
  - Bot 连接/断开事件
  - 用户命令执行
  - AI 请求和回应
  - 错误信息
  - 管理员操作

**查看日志**:
```bash
# Windows
type logs\bot_20260502.log

# Linux/Mac
cat logs/bot_20260502.log
tail -f logs/bot_*.log
```

### 💾 数据持久化
- **文件**: `user_data.json`
- **内容**:
  - 每个用户的角色设置
  - 最后保存时间
  
**数据自动保存**:
- 用户切换角色时
- 管理员备份时
- Bot 关闭时

**数据结构**:
```json
{
  "personalities": {
    "123456789": "程式",
    "987654321": "數理"
  },
  "last_save": "2026-05-02T12:34:56.789012"
}
```

### 🔌 自动重连
- **异常处理**: Bot 遇到错误会记录并继续运行
- **连接稳定**: 自动重新连接到 Discord
- **日志记录**: 所有错误都记录到日志

---

## 🛡️ 管理员命令

### 如何成为管理员？
编辑 `設定.env`，添加你的 Discord ID:
```env
ADMIN_IDS=123456789,987654321
```

**如何获取你的 ID？**:
1. 启用 Discord 开发者模式 (Settings → Advanced → Developer Mode)
2. 右键点击你的名字，选择 "Copy User ID"

### 管理员命令列表

#### `!admin stats`
查看 Bot 统计信息
```
!admin stats
→ 📊 Bot 統計
  總用戶: 5
  在線: 2 個伺服器
```

#### `!admin clear_user [user_id]`
清除指定用户的所有数据
```
!admin clear_user 123456789
→ ✅ 已清除用戶 123456789 的數據
```

#### `!admin backup`
手动备份所有用户数据
```
!admin backup
→ ✅ 已備份數據
```

#### `!admin restart`
重启 Bot（仅断开连接）
```
!admin restart
→ 🔄 Bot 即將重啟...
```

#### `!admin`
显示所有管理员命令
```
!admin
→ 管理員命令:
  !admin stats - 查看統計
  !admin clear_user [user_id] - 清除用戶數據
  !admin backup - 備份數據
  !admin restart - 重啟 Bot
```

---

## 📖 使用指南

### 用户命令（私信）
| 命令 | 说明 | 例子 |
|------|------|------|
| `!mode [角色]` | 切换 AI 角色 | `!mode 程式` |
| `!ask [问题]` | 提问 | `!ask Python 怎样写迴圈？` |
| `!clear` | 清除对话 | `!clear` |
| `!guide` | 显示使用指南 | `!guide` |
| `!help` | 显示帮助 | `!help` |

### 5 种 AI 角色
1. **✅ 閒談** - 友善、幽默的聊天夥伴
2. **🔢 數理** - 数学和科学专家
3. **📚 語文** - 语言和文学专家
4. **💻 程式** - 编程和技术专家
5. **🏠 家務** - 生活和家务建议

### 使用流程

```
1️⃣ 点击 Bot → 发送私信
   ↓
2️⃣ 自动收到 Guide
   ↓
3️⃣ !mode [角色名]  切换角色
   ↓
4️⃣ !ask [问题]  开始聊天
   ↓
5️⃣ 继续提问，享受连续对话！
```

---

## 🔧 配置说明

### 設定.env 文件

```env
# Discord Bot Token (必需)
DISCORD_TOKEN=你的_Token

# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=Qwen2.5-1.5B-Instruct

# 频道 ID (可选，用于测试)
TEST_CHANNEL_ID=1500045129614885079

# 管理员 ID (可选)
ADMIN_IDS=123456789,987654321
```

### 可用的 Ollama 模型
- `Qwen2.5-1.5B-Instruct` - **推荐** ✅ 对话优化
- `gemma2:2b` - 轻量级，速度快
- `mistral` - 通用模型
- `llama2` - 需自行下载

### 修改模型
编辑 `設定.env`:
```env
OLLAMA_MODEL=gemma2:2b
```

---

## 🐛 故障排除

### ❌ "未找到 DISCORD_TOKEN"
**原因**: Token 配置错误
```bash
# 解决方案:
# 1. 检查 設定.env 是否存在
# 2. 检查 DISCORD_TOKEN 是否正确
# 3. 检查是否有多余空格
```

### ❌ "Ollama API 404 错误"
**原因**: Ollama 未运行或模型不存在
```bash
# 解决方案:
ollama serve
ollama pull Qwen2.5-1.5B-Instruct
```

### ❌ 日志文件太大
**原因**: 长期运行产生大量日志
```bash
# 解决方案:
# 删除旧的日志文件 (logs/bot_*.log)
# 或定期清理
```

### ❌ 数据丢失
**原因**: user_data.json 被删除
```bash
# 解决方案:
# 备份重要数据到其他地方
# 定期执行 !admin backup
```

---

## 📊 文件结构

```
dcard_bot/
├── bot.py                    # 主程序（完整版）
├── bot_backup.py             # 备份
├── start.bat                 # Windows 启动脚本
├── run.py                    # Python 启动脚本
├── requirements.txt          # 依赖列表
├── 設定.env                   # 配置文件
├── README.md                 # 本文件
├── test.py                   # 测试脚本
├── user_data.json            # 用户数据（自动生成）
└── logs/                     # 日志目录（自动生成）
    ├── bot_20260502.log
    └── bot_20260503.log
```

---

## 🎯 最佳实践

### 安全性
- 🔐 **不要分享 Token** - 小心保管 設定.env
- 🔒 **限制管理员** - 只添加信任的用户为管理员
- 📝 **定期备份** - 每周手动备份数据

### 性能
- ⚡ **使用轻量模型** - gemma2:2b 更快
- 💾 **限制历史** - MAX_HISTORY 不宜过大
- 🔄 **定期重启** - 每周重启 Bot 一次

### 运维
- 📊 **监控日志** - 定期检查错误
- 🔔 **自动提醒** - 设置日志告警
- 🛡️ **自动备份** - 设置定时备份脚本

---

## 📞 问题反馈

如有问题，请查看：
1. 日志文件 (logs/)
2. 本 README
3. 执行 `!help` 命令

---

**最后更新**: 2026-05-02  
**版本**: 2.0 (完整后台版本)  
**许可**: MIT
