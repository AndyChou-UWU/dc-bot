"""
subaso - 全局配置文件 (副本，用於替代舊的配置文件)
包含所有常量、配置和系統設置（顯示名稱：subaso-俗北ㄙㄡˊ）
"""

# ==================== 版本信息 ====================
BOT_VERSION = "2.0.0"
BOT_NAME = "subaso-俗北ㄙㄡˊ"
BOT_DESCRIPTION = "subaso-俗北ㄙㄡˊ - 多功能 AI Discord Bot"

# ==================== 功能模塊配置 ====================
MODULES = {
    "ai": {
        "name": "🤖 AI 對話系統",
        "enabled": True,
        "features": ["多角色", "多語言", "連續對話", "版本管理", "數據保存"]
    },
    "economy": {
        "name": "💰 經濟系統",
        "enabled": True,
        "features": ["挖礦", "釣魚", "狩獵", "賭博", "寵物", "市場"]
    },
    "games": {
        "name": "🎮 娛樂遊戲",
        "enabled": True,
        "features": ["Pokemon猜謎", "Trivia", "動漫角色", "數字遊戲", "動漫查詢", "互動動作"]
    },
    "admin": {
        "name": "⚙️ 管理工具",
        "enabled": True,
        "features": ["日誌", "清理", "歡迎消息", "配置", "自定義命令"]
    },
    "music": {
        "name": "🎵 音樂系統",
        "enabled": False,  # 可選 - 需要 Lavalink
        "features": ["播放", "播放列表", "控制", "DJ模式", "直播", "搜索"]
    }
}

# ==================== 經濟系統常量 ====================
CURRENCY_NAME = "💎 晶幣"
STARTING_BALANCE = 1000

# 挖礦系統
MINING_REWARDS = {
    "iron": {"amount": 50, "emoji": "⛏️"},
    "gold": {"amount": 150, "emoji": "🏆"},
    "diamond": {"amount": 500, "emoji": "💎"}
}

# 釣魚系統
FISHING_CATCHES = {
    "鯉魚": {"amount": 40, "emoji": "🐟"},
    "金魚": {"amount": 120, "emoji": "✨"},
    "龍魚": {"amount": 400, "emoji": "🐉"}
}

# 寵物系統
PETS = {
    "貓": {"emoji": "🐱", "mood_boost": 1.1},
    "狗": {"emoji": "🐕", "mood_boost": 1.15},
    "龍": {"emoji": "🐉", "mood_boost": 1.5}
}

# ==================== 遊戲系統常量 ====================
TRIVIA_CATEGORIES = [
    "general", "science", "history", "sports", 
    "entertainment", "geography", "technology"
]

POKEMON_DIFFICULTY = {
    "easy": {"reward": 100, "timeout": 30},
    "medium": {"reward": 250, "timeout": 20},
    "hard": {"reward": 500, "timeout": 10}
}

# ==================== 管理系統常量 ====================
LOG_FILE_FORMAT = "logs/subaso_{date}.log"
MAX_MESSAGES_PRUNE = 1000

# ==================== AI 角色配置 ====================
PERSONALITIES = {
    "閒談": {
        "prefix": "chat",
        "emoji": "✅",
        "system": "我是一個友善、幽默的聊天夥伴。使用自然的對話風格，可以討論任何日常話題。回答要親切自然。別忘了不行文不對題"
    },
    "數理": {
        "prefix": "math",
        "emoji": "🔢",
        "system": "我是一個數學和科學專家。用清晰的邏輯和步驟解釋問題。如果涉及計算，請逐步展示你的工作過程。使用中文解釋。"
    },
    "語文": {
        "prefix": "lang",
        "emoji": "📚",
        "system": "我是一個語言和文學專家。專長於語法、詞彙、文學分析和寫作技巧。提供詳細的解釋和例子。"
    },
    "程式": {
        "prefix": "code",
        "emoji": "💻",
        "system": "我是一個專業的程式設計師和軟體工程師。幫助編寫、除錯和解釋程式碼。提供實用的解決方案和最佳實踐。使用繁體中文回答。"
    },
    "家務": {
        "prefix": "home",
        "emoji": "🏠",
        "system": "我是一個家務和生活建議專家。提供關於烹飪、清潔、整理和日常生活的實用建議。親切且實用。"
    }
}

# ==================== 多語言支援 ====================
LANGUAGE_OPTIONS = {
    "chinese": "🇹🇼 繁體中文",
    "english": "🇺🇸 English",
    "japanese": "🇯🇵 日本語",
    "korean": "🇰🇷 한국어",
    "spanish": "🇪🇸 Español"
}

LANGUAGE_PROMPTS = {
    "chinese": "請使用繁體中文回答。",
    "english": "Please answer in English.",
    "japanese": "日本語で回答してください。",
    "korean": "한국어로 대답해 주세요.",
    "spanish": "Por favor responde en Español."
}

# ==================== 命令前綴 ====================
DEFAULT_PREFIX = "!"
ADMIN_PREFIX = "!admin"

# ==================== 權限等級 ====================
PERMISSION_LEVELS = {
    0: "用戶",
    1: "版主",
    2: "管理員",
    3: "Bot 所有者"
}
