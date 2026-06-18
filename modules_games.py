"""
subaso - 娛樂遊戲系統模塊
包含: Pokemon猜謎、Trivia、動漫角色、數字遊戲、互動動作
"""

import discord
import random
import asyncio
from enum import Enum

# ==================== Pokemon 數據庫 ====================
POKEMON_DB = {
    "皮卡丘": {"type": "電", "color": "黃", "ability": "靜電"},
    "妙蛙種子": {"type": "草/毒", "color": "綠", "ability": "茂盛"},
    "小火龍": {"type": "火", "color": "橙", "ability": "火焰身體"},
    "傑尼龜": {"type": "水", "color": "藍", "ability": "激流"},
    "比雕": {"type": "飛行/普通", "color": "棕", "ability": "銳利目光"},
    "阿柏": {"type": "毒", "color": "紫", "ability": "蛻皮"},
}

# ==================== Trivia 數據庫 ====================
TRIVIA_DB = [
    {
        "question": "地球上最大的陸地動物是什麼？",
        "options": ["大象", "長頸鹿", "犀牛", "河馬"],
        "answer": "大象",
        "category": "生物"
    },
    {
        "question": "Python 編程語言由誰創造？",
        "options": ["Guido van Rossum", "Linus Torvalds", "Dennis Ritchie", "Bjarne Stroustrup"],
        "answer": "Guido van Rossum",
        "category": "技術"
    },
    {
        "question": "世界最高的山峯是？",
        "options": ["珠穆朗瑪峯", "乞力馬扎羅山", "麥金利峯", "阿空加瓜山"],
        "answer": "珠穆朗瑪峯",
        "category": "地理"
    },
    {
        "question": "中國的首都是？",
        "options": ["北京", "上海", "廣州", "深圳"],
        "answer": "北京",
        "category": "地理"
    },
    {
        "question": "莎士比亞是哪個國家的作家？",
        "options": ["英國", "美國", "法國", "意大利"],
        "answer": "英國",
        "category": "文學"
    },
]

# ==================== 動漫角色數據庫 ====================
ANIME_CHARACTERS = {
    "鳴人": {"anime": "火影忍者", "description": "金色頭髮的忍者，經歷坎坷但心地善良", "power": "尾獸能力"},
    "路飛": {"anime": "海賊王", "description": "戴着草帽的少年，夢想成爲海賊王", "power": "橡膠果實"},
    "悟空": {"anime": "龍珠", "description": "一根頭髮立起來的戰士，喜歡戰鬥", "power": "氣功波"},
    "炭治郎": {"anime": "鬼滅之刃", "description": "黑髮少年，妹妹被鬼化", "power": "呼吸法"},
    "五條悟": {"anime": "咒術回戰", "description": "白髮帥哥，有着特殊的眼睛能力", "power": "六眼"},
}

# ==================== 互動動作 ====================
ACTION_GIFS = {
    "hug": {"text": "擁抱了", "emoji": "🤗"},
    "pat": {"text": "拍了拍", "emoji": "👋"},
    "slap": {"text": "打了", "emoji": "👋"},
    "kiss": {"text": "親了", "emoji": "💋"},
    "punch": {"text": "打拳了", "emoji": "👊"},
    "dance": {"text": "跳舞了", "emoji": "🕺"},
    "cry": {"text": "哭了", "emoji": "😭"},
    "laugh": {"text": "笑了", "emoji": "😂"},
}

# ==================== 辯論話題 ====================
DEBATE_TOPICS = [
    {
        "topic": "披薩應該放鳳梨嗎？",
        "side_a": "鳳梨派 🍍",
        "side_b": "純粹派 ❌"
    },
    {
        "topic": "咖啡應該加糖嗎？",
        "side_a": "甜咖派 🍬",
        "side_b": "黑咖派 🖤"
    },
    {
        "topic": "夜貓子和早鳥哪個更優？",
        "side_a": "夜貓子 🦉",
        "side_b": "早鳥 🐓"
    },
    {
        "topic": "手機遊戲和電腦遊戲哪個更好？",
        "side_a": "手機遊戲 📱",
        "side_b": "電腦遊戲 💻"
    },
    {
        "topic": "吃陽春麵還是牛肉麵更划算？",
        "side_a": "陽春麵派 🍜",
        "side_b": "牛肉麵派 🐂"
    }
]

class GameSystem:
    """遊戲系統管理"""
    
    def __init__(self):
        self.active_games = {}
        self.user_scores = {}
    
    # ==================== Pokemon 猜謎遊戲 ====================
    def start_pokemon_game(self, user_id):
        """開始 Pokemon 猜謎遊戲"""
        pokemon = random.choice(list(POKEMON_DB.keys()))
        pokemon_info = POKEMON_DB[pokemon]
        
        question = f"""
🎮 **Pokemon 猜謎遊戲開始！**

**線索:**
- 類型: {pokemon_info['type']}
- 顏色: {pokemon_info['color']}
- 特性: {pokemon_info['ability']}

你有 30 秒來猜測這是哪隻 Pokemon！
輸入: !guess [pokemon名字]
"""
        self.active_games[user_id] = {
            "type": "pokemon",
            "answer": pokemon,
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_pokemon_answer(self, user_id, guess):
        """檢查 Pokemon 答案"""
        if user_id not in self.active_games:
            return False, "沒有活躍的遊戲"
        
        game = self.active_games[user_id]
        if game.get("type") != "pokemon":
            return False, "目前沒有 Pokemon 猜謎遊戲，請先輸入 !pokemon 開始遊戲。"
        
        answer = str(game.get("answer", ""))
        guess_text = str(guess).strip()
        if guess_text.lower() == answer.lower():
            reward = 250
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正確！這是 **{game['answer']}**！+{reward} 分"
        else:
            return False, f"❌ 錯誤。答案是 **{game['answer']}**"
    
    # ==================== Trivia 競賽 ====================
    def start_trivia(self, user_id):
        """開始 Trivia 遊戲"""
        trivia = random.choice(TRIVIA_DB)
        
        options_text = "\n".join([f"**{i+1}**. {opt}" for i, opt in enumerate(trivia["options"])])
        
        question = f"""
🧠 **Trivia 知識競賽**

**問題:** {trivia['question']}

{options_text}

回答: !answer [1-4]
"""
        self.active_games[user_id] = {
            "type": "trivia",
            "answer": trivia["answer"],
            "options": trivia["options"],
            "category": trivia["category"],
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_trivia_answer(self, user_id, answer_num):
        """檢查 Trivia 答案"""
        if user_id not in self.active_games:
            return False, "沒有活躍的遊戲"
        
        game = self.active_games[user_id]
        if game.get("type") != "trivia":
            return False, "目前沒有 Trivia 遊戲，請先輸入 !trivia 開始遊戲。"
        
        if not isinstance(answer_num, int) or answer_num < 1 or answer_num > len(game.get("options", [])):
            return False, "請輸入有效的答案號 (1-4)"
        
        selected_option = game["options"][answer_num - 1]
        if selected_option.lower() == str(game["answer"]).lower():
            reward = 200
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 恭喜你答對了！正確答案是 **{game['answer']}**。+{reward} 分"
        else:
            return False, f"❌ 錯誤。正確答案是 **{game['answer']}**。"
    
    # ==================== 動漫角色猜謎 ====================
    def start_anime_guess(self, user_id):
        """開始動漫角色猜謎"""
        character = random.choice(list(ANIME_CHARACTERS.keys()))
        char_info = ANIME_CHARACTERS[character]
        
        question = f"""
⛩️ **動漫角色猜謎遊戲**

**線索:**
- 描述: {char_info['description']}
- 能力: {char_info['power']}

你有 30 秒來猜測是哪個角色！
輸入: !guess_char [角色名字]
"""
        self.active_games[user_id] = {
            "type": "anime",
            "answer": character,
            "anime": char_info["anime"],
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_anime_answer(self, user_id, guess):
        """檢查動漫角色答案"""
        if user_id not in self.active_games:
            return False, "沒有活躍的遊戲"
        
        game = self.active_games[user_id]
        if game.get("type") != "anime":
            return False, "目前沒有動漫角色猜謎遊戲，請先輸入 !anime 開始遊戲。"
        
        answer = str(game.get("answer", "")).lower()
        anime_title = str(game.get("anime", "未知作品"))
        guess_text = str(guess).strip()
        if guess_text.lower() == answer:
            reward = 300
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正確！這是 **{game['answer']}** 來自 **{anime_title}**！+{reward} 分"
        else:
            return False, f"❌ 錯誤。答案是 **{game['answer']}** 來自 **{anime_title}**"
    
    # ==================== 數字猜測遊戲 ====================
    def start_number_game(self, user_id):
        """開始數字猜測遊戲"""
        number = random.randint(1, 100)
        
        question = """
🎲 **數字猜測遊戲**

我想了一個 1-100 之間的數字，你有 10 次機會猜測！

輸入: !guess_number [數字]
"""
        self.active_games[user_id] = {
            "type": "number",
            "answer": number,
            "attempts": 0,
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_number_answer(self, user_id, guess):
        """檢查數字答案"""
        if user_id not in self.active_games:
            return False, "沒有活躍的遊戲"
        
        game = self.active_games[user_id]
        if game.get("type") != "number":
            return False, "目前沒有數字猜測遊戲，請先輸入 !number 開始遊戲。"
        
        if not isinstance(guess, int):
            return False, "請輸入有效數字，例如: !guess_number 42"
        
        game["attempts"] += 1
        
        if game["attempts"] > 10:
            answer = game["answer"]
            del self.active_games[user_id]
            return False, f"❌ 遊戲結束！答案是 **{answer}**"
        
        if guess == game["answer"]:
            reward = max(500 - (game["attempts"] * 20), 100)
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正確！用了 {game['attempts']} 次機會。+{reward} 分"
        elif guess < game["answer"]:
            return None, f"📈 太小了 ({game['attempts']}/10)"
        else:
            return None, f"📉 太大了 ({game['attempts']}/10)"
    
    # ==================== 互動動作 ====================
    def get_action(self, action_name):
        """獲取互動動作"""
        if action_name.lower() in ACTION_GIFS:
            return ACTION_GIFS[action_name.lower()]
        return None
    
    def get_user_score(self, user_id):
        """獲取用戶總分"""
        return self.user_scores.get(user_id, 0)
    
    # ==================== 辯論系統 ====================
    def start_debate(self):
        """開始辯論遊戲"""
        debate = random.choice(DEBATE_TOPICS)

        message = f"""
🎤 **辯論時間開始！** 🎤

**議題**: {debate['topic']}

你要跟 AI 對戰，先選你的立場：
- `!debate a` 支持 {debate['side_a']}
- `!debate b` 支持 {debate['side_b']}

選邊後，AI 會直接給出對方論點，接著你可以用 `!debate arg [你的論點]` 反駁。
輸入 `!debate end` 可結束辯論，AI 充當評審判勝負。
"""
        debate_data = {
            'topic': debate['topic'],
            'side_a': debate['side_a'],
            'side_b': debate['side_b'],
            'user_choice': None,
            'chat_history': []
        }

        return message, debate_data
    
    def get_debate_result(self, debate, choice):
        """獲取辯論結果（搞笑的判決）"""
        choice = choice.lower()
        if choice not in ['a', 'b']:
            return None
        
        topics = debate['topic']
        side_a = debate['side_a']
        side_b = debate['side_b']
        
        results = {
            'a': [
                f"🏆 {side_a} 大獲全勝！評審們被說服了！",
                f"⚖️ 經過激烈討論，{side_a} 最終勝出！",
                f"🎯 {side_a} 用無敵的邏輯擊敗了對手！",
                f"💪 {side_a} 的論點無法反駁，完全碾壓！",
                f"🥊 {side_a} 一拳KO，對手躺平！"
            ],
            'b': [
                f"🏆 {side_b} 反敗為勝！翻盤了！",
                f"⚖️ 最終法官判定 {side_b} 獲勝！",
                f"🎯 {side_b} 用犀利的回應擊敗對手！",
                f"💪 {side_b} 的論據無懈可擊，對手認輸！",
                f"🥊 {side_b} 完勝，對方詞窮！"
            ]
        }
        
        result_text = random.choice(results[choice])
        bonus_points = random.randint(50, 150)
        
        return {
            "result": result_text,
            "points": bonus_points,
            "message": f"{result_text}\n\n🎁 你獲得了 **{bonus_points}** 積分！"
        }

# ==================== 命令列表 ====================
def get_game_commands():
    """獲取所有遊戲命令"""
    return {
        "!pokemon": "開始 Pokemon 猜謎遊戲",
        "!trivia": "開始 Trivia 知識競賽",
        "!anime": "開始動漫角色猜謎",
        "!number": "開始數字猜測遊戲",
        "!debate": "開始搞笑辯論對談",
        "!score": "查看你的遊戲分數",
        "!hug [@用戶]": "擁抱某人",
        "!pat [@用戶]": "拍某人",
        "!slap [@用戶]": "打某人",
        "!kiss [@用戶]": "親某人",
        "!dance": "跳舞",
        "!cry": "哭泣",
        "!laugh": "大笑"
    }
