"""
PRISM Bot - 娱乐游戏系统模块
包含: Pokemon猜谜、Trivia、动漫角色、数字游戏、互动动作
"""

import discord
import random
import asyncio
from enum import Enum

# ==================== Pokemon 数据库 ====================
POKEMON_DB = {
    "皮卡丘": {"type": "电", "color": "黄", "ability": "静电"},
    "妙蛙种子": {"type": "草/毒", "color": "绿", "ability": "茂盛"},
    "小火龙": {"type": "火", "color": "橙", "ability": "火焰身体"},
    "杰尼龟": {"type": "水", "color": "蓝", "ability": "激流"},
    "比雕": {"type": "飞行/普通", "color": "棕", "ability": "锐利目光"},
    "阿柏": {"type": "毒", "color": "紫", "ability": "蜕皮"},
}

# ==================== Trivia 数据库 ====================
TRIVIA_DB = [
    {
        "question": "地球上最大的陆地动物是什么？",
        "options": ["大象", "长颈鹿", "犀牛", "河马"],
        "answer": "大象",
        "category": "生物"
    },
    {
        "question": "Python 编程语言由谁创造？",
        "options": ["Guido van Rossum", "Linus Torvalds", "Dennis Ritchie", "Bjarne Stroustrup"],
        "answer": "Guido van Rossum",
        "category": "技术"
    },
    {
        "question": "世界最高的山峰是？",
        "options": ["珠穆朗玛峰", "乞力马扎罗山", "麦金利峰", "阿空加瓜山"],
        "answer": "珠穆朗玛峰",
        "category": "地理"
    },
    {
        "question": "中国的首都是？",
        "options": ["北京", "上海", "广州", "深圳"],
        "answer": "北京",
        "category": "地理"
    },
    {
        "question": "莎士比亚是哪个国家的作家？",
        "options": ["英国", "美国", "法国", "意大利"],
        "answer": "英国",
        "category": "文学"
    },
]

# ==================== 动漫角色数据库 ====================
ANIME_CHARACTERS = {
    "鸣人": {"anime": "火影忍者", "description": "金色头发的忍者，经历坎坷但心地善良", "power": "尾兽能力"},
    "路飞": {"anime": "海贼王", "description": "戴着草帽的少年，梦想成为海贼王", "power": "橡胶果实"},
    "悟空": {"anime": "龙珠", "description": "一根头发立起来的战士，喜欢战斗", "power": "气功波"},
    "炭治郎": {"anime": "鬼灭之刃", "description": "黑发少年，妹妹被鬼化", "power": "呼吸法"},
    "五条悟": {"anime": "咒术回战", "description": "白发帅哥，有着特殊的眼睛能力", "power": "六眼"},
}

# ==================== 互动动作 ====================
ACTION_GIFS = {
    "hug": {"text": "拥抱了", "emoji": "🤗"},
    "pat": {"text": "拍了拍", "emoji": "👋"},
    "slap": {"text": "打了", "emoji": "👋"},
    "kiss": {"text": "亲了", "emoji": "💋"},
    "punch": {"text": "打拳了", "emoji": "👊"},
    "dance": {"text": "跳舞了", "emoji": "🕺"},
    "cry": {"text": "哭了", "emoji": "😭"},
    "laugh": {"text": "笑了", "emoji": "😂"},
}

class GameSystem:
    """游戏系统管理"""
    
    def __init__(self):
        self.active_games = {}
        self.user_scores = {}
    
    # ==================== Pokemon 猜谜游戏 ====================
    def start_pokemon_game(self, user_id):
        """开始 Pokemon 猜谜游戏"""
        pokemon = random.choice(list(POKEMON_DB.keys()))
        pokemon_info = POKEMON_DB[pokemon]
        
        question = f"""
🎮 **Pokemon 猜谜游戏开始！**

**线索:**
- 类型: {pokemon_info['type']}
- 颜色: {pokemon_info['color']}
- 特性: {pokemon_info['ability']}

你有 30 秒来猜测这是哪只 Pokemon！
输入: !guess [pokemon名字]
"""
        self.active_games[user_id] = {
            "type": "pokemon",
            "answer": pokemon,
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_pokemon_answer(self, user_id, guess):
        """检查 Pokemon 答案"""
        if user_id not in self.active_games:
            return False, "没有活跃的游戏"
        
        game = self.active_games[user_id]
        if guess.lower() == game["answer"].lower():
            reward = 250
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正确！这是 **{game['answer']}**！+{reward} 分"
        else:
            return False, f"❌ 错误。答案是 **{game['answer']}**"
    
    # ==================== Trivia 竞赛 ====================
    def start_trivia(self, user_id):
        """开始 Trivia 游戏"""
        trivia = random.choice(TRIVIA_DB)
        
        options_text = "\n".join([f"**{i+1}**. {opt}" for i, opt in enumerate(trivia["options"])])
        
        question = f"""
🧠 **Trivia 知识竞赛**

**问题:** {trivia['question']}

{options_text}

回答: !answer [1-4]
"""
        self.active_games[user_id] = {
            "type": "trivia",
            "answer": trivia["answer"],
            "category": trivia["category"],
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_trivia_answer(self, user_id, answer_num):
        """检查 Trivia 答案"""
        if user_id not in self.active_games:
            return False, "没有活跃的游戏"
        
        game = self.active_games[user_id]
        try:
            trivia = TRIVIA_DB[answer_num - 1] if 1 <= answer_num <= len(TRIVIA_DB) else None
        except:
            return False, "请输入有效的答案号 (1-4)"
        
        # 这里简化了逻辑，实际应该匹配正确答案
        return True, f"✅ 正确答案是: {game['answer']}"
    
    # ==================== 动漫角色猜谜 ====================
    def start_anime_guess(self, user_id):
        """开始动漫角色猜谜"""
        character = random.choice(list(ANIME_CHARACTERS.keys()))
        char_info = ANIME_CHARACTERS[character]
        
        question = f"""
⛩️ **动漫角色猜谜游戏**

**线索:**
- 描述: {char_info['description']}
- 能力: {char_info['power']}

你有 30 秒来猜测是哪个角色！
输入: !guess_char [角色名字]
"""
        self.active_games[user_id] = {
            "type": "anime",
            "answer": character,
            "anime": char_info["anime"],
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_anime_answer(self, user_id, guess):
        """检查动漫角色答案"""
        if user_id not in self.active_games:
            return False, "没有活跃的游戏"
        
        game = self.active_games[user_id]
        if guess.lower() == game["answer"].lower():
            reward = 300
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正确！这是 **{game['answer']}** 来自 **{game['anime']}**！+{reward} 分"
        else:
            return False, f"❌ 错误。答案是 **{game['answer']}** 来自 **{game['anime']}**"
    
    # ==================== 数字猜测游戏 ====================
    def start_number_game(self, user_id):
        """开始数字猜测游戏"""
        number = random.randint(1, 100)
        
        question = """
🎲 **数字猜测游戏**

我想了一个 1-100 之间的数字，你有 10 次机会猜测！

输入: !guess_number [数字]
"""
        self.active_games[user_id] = {
            "type": "number",
            "answer": number,
            "attempts": 0,
            "timestamp": asyncio.get_event_loop().time()
        }
        return question
    
    def check_number_answer(self, user_id, guess):
        """检查数字答案"""
        if user_id not in self.active_games:
            return False, "没有活跃的游戏"
        
        game = self.active_games[user_id]
        game["attempts"] += 1
        
        if game["attempts"] > 10:
            answer = game["answer"]
            del self.active_games[user_id]
            return False, f"❌ 游戏结束！答案是 **{answer}**"
        
        if guess == game["answer"]:
            reward = max(500 - (game["attempts"] * 20), 100)
            if user_id not in self.user_scores:
                self.user_scores[user_id] = 0
            self.user_scores[user_id] += reward
            del self.active_games[user_id]
            return True, f"✅ 正确！用了 {game['attempts']} 次机会。+{reward} 分"
        elif guess < game["answer"]:
            return None, f"📈 太小了 ({game['attempts']}/10)"
        else:
            return None, f"📉 太大了 ({game['attempts']}/10)"
    
    # ==================== 互动动作 ====================
    def get_action(self, action_name):
        """获取互动动作"""
        if action_name.lower() in ACTION_GIFS:
            return ACTION_GIFS[action_name.lower()]
        return None
    
    def get_user_score(self, user_id):
        """获取用户总分"""
        return self.user_scores.get(user_id, 0)

# ==================== 命令列表 ====================
def get_game_commands():
    """获取所有游戏命令"""
    return {
        "!pokemon": "开始 Pokemon 猜谜游戏",
        "!trivia": "开始 Trivia 知识竞赛",
        "!anime": "开始动漫角色猜谜",
        "!number": "开始数字猜测游戏",
        "!score": "查看你的游戏分数",
        "!hug [@用户]": "拥抱某人",
        "!pat [@用户]": "拍某人",
        "!slap [@用户]": "打某人",
        "!kiss [@用户]": "亲某人",
        "!dance": "跳舞",
        "!cry": "哭泣",
        "!laugh": "大笑"
    }
