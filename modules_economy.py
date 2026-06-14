"""
PRISM Bot - 经济系统模块
包含: 挖矿、钓鱼、狩猎、赌博、宠物、市场交易
"""

import discord
import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from prism_config import CURRENCY_NAME, MINING_REWARDS, FISHING_CATCHES, PETS, STARTING_BALANCE

ECONOMY_DATA_FILE = "data/economy.json"

class EconomySystem:
    """经济系统管理"""
    
    def __init__(self):
        self.user_wallets = {}
        self.user_pets = {}
        self.user_cooldowns = {}
        self.load_economy_data()
    
    def load_economy_data(self):
        """加载经济数据"""
        os.makedirs("data", exist_ok=True)
        if os.path.exists(ECONOMY_DATA_FILE):
            try:
                with open(ECONOMY_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_wallets = {int(k): v for k, v in data.get("wallets", {}).items()}
                    self.user_pets = {int(k): v for k, v in data.get("pets", {}).items()}
            except:
                pass
    
    def save_economy_data(self):
        """保存经济数据"""
        data = {
            "wallets": {str(k): v for k, v in self.user_wallets.items()},
            "pets": {str(k): v for k, v in self.user_pets.items()}
        }
        with open(ECONOMY_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_balance(self, user_id):
        """获取用户余额"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        return self.user_wallets[user_id]["balance"]
    
    def add_balance(self, user_id, amount):
        """增加余额"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        self.user_wallets[user_id]["balance"] += amount
        self.save_economy_data()
        return self.user_wallets[user_id]["balance"]
    
    def subtract_balance(self, user_id, amount):
        """减少余额"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        
        if self.user_wallets[user_id]["balance"] >= amount:
            self.user_wallets[user_id]["balance"] -= amount
            self.save_economy_data()
            return True
        return False
    
    def transfer_balance(self, from_id, to_id, amount):
        """转账"""
        if self.subtract_balance(from_id, amount):
            self.add_balance(to_id, amount)
            return True
        return False
    
    # ==================== 挖矿系统 ====================
    def can_mine(self, user_id):
        """检查是否可以挖矿"""
        return self.check_cooldown(user_id, "mine", 60)
    
    def mine(self, user_id):
        """挖矿"""
        ore_type = random.choice(list(MINING_REWARDS.keys()))
        reward_info = MINING_REWARDS[ore_type]
        amount = reward_info["amount"]
        
        self.add_balance(user_id, amount)
        return ore_type, amount, reward_info["emoji"]
    
    # ==================== 钓鱼系统 ====================
    def can_fish(self, user_id):
        """检查是否可以钓鱼"""
        return self.check_cooldown(user_id, "fish", 60)
    
    def fish(self, user_id):
        """钓鱼"""
        catch = random.choice(list(FISHING_CATCHES.keys()))
        catch_info = FISHING_CATCHES[catch]
        amount = catch_info["amount"]
        
        self.add_balance(user_id, amount)
        return catch, amount, catch_info["emoji"]
    
    # ==================== 狩猎系统 ====================
    def can_hunt(self, user_id):
        """检查是否可以狩猎"""
        return self.check_cooldown(user_id, "hunt", 120)
    
    def hunt(self, user_id):
        """狩猎"""
        animals = {
            "兔子": {"amount": 80, "emoji": "🐰"},
            "鹿": {"amount": 200, "emoji": "🦌"},
            "熊": {"amount": 500, "emoji": "🐻"}
        }
        animal = random.choice(list(animals.keys()))
        animal_info = animals[animal]
        amount = animal_info["amount"]
        
        self.add_balance(user_id, amount)
        return animal, amount, animal_info["emoji"]
    
    # ==================== 赌博系统 ====================
    def gamble(self, user_id, amount):
        """赌博"""
        if not self.subtract_balance(user_id, amount):
            return False, 0, "余额不足"
        
        if random.random() < 0.5:  # 50% 赢的概率
            winnings = amount * 2
            self.add_balance(user_id, winnings)
            return True, winnings, "赢了！"
        else:
            return False, 0, "输了..."
    
    def slots(self, user_id, amount):
        """老虎机"""
        if not self.subtract_balance(user_id, amount):
            return False, 0, []
        
        symbols = ["🍒", "🍊", "🍋", "🍌", "🍉"]
        result = [random.choice(symbols) for _ in range(3)]
        
        if result[0] == result[1] == result[2]:
            winnings = amount * 5
            self.add_balance(user_id, winnings)
            return True, winnings, result
        else:
            return False, 0, result
    
    # ==================== 宠物系统 ====================
    def adopt_pet(self, user_id, pet_name):
        """领养宠物"""
        if user_id in self.user_pets:
            return False, "你已经有一只宠物了"
        
        if pet_name not in PETS:
            return False, f"不存在的宠物: {pet_name}"
        
        pet_info = PETS[pet_name]
        self.user_pets[user_id] = {
            "name": pet_name,
            "adopted_at": datetime.now().isoformat(),
            "mood": 100,
            "emoji": pet_info["emoji"]
        }
        self.save_economy_data()
        return True, f"成功领养了 {pet_info['emoji']} {pet_name}！"
    
    def get_pet(self, user_id):
        """获取宠物信息"""
        if user_id not in self.user_pets:
            return None
        return self.user_pets[user_id]
    
    def feed_pet(self, user_id, amount):
        """喂养宠物"""
        pet = self.get_pet(user_id)
        if not pet:
            return False, "你没有宠物"
        
        if not self.subtract_balance(user_id, amount):
            return False, "余额不足"
        
        pet["mood"] = min(100, pet["mood"] + 20)
        self.save_economy_data()
        return True, f"你的宠物开心了！心情: {pet['mood']}/100"
    
    # ==================== 市场系统 ====================
    def list_market_prices(self):
        """列出市场价格"""
        prices = {
            "挖矿收入": {
                "铁": MINING_REWARDS["iron"]["amount"],
                "金": MINING_REWARDS["gold"]["amount"],
                "钻": MINING_REWARDS["diamond"]["amount"]
            },
            "钓鱼收入": FISHING_CATCHES
        }
        return prices
    
    # ==================== 冷却时间 ====================
    def check_cooldown(self, user_id, action, cooldown_seconds):
        """检查冷却时间"""
        if user_id not in self.user_cooldowns:
            self.user_cooldowns[user_id] = {}
        
        key = f"{user_id}_{action}"
        now = datetime.now()
        
        if key in self.user_cooldowns[user_id]:
            last_used = self.user_cooldowns[user_id][key]
            if (now - last_used).total_seconds() < cooldown_seconds:
                remaining = cooldown_seconds - int((now - last_used).total_seconds())
                return False, remaining
        
        self.user_cooldowns[user_id][key] = now
        return True, 0

# ==================== 命令处理函数 ====================
def get_economy_commands():
    """获取所有经济系统命令"""
    return {
        "!balance": "查看余额",
        "!mine": "挖矿 (冷却 60秒)",
        "!fish": "钓鱼 (冷却 60秒)",
        "!hunt": "狩猎 (冷却 120秒)",
        "!gamble [金额]": "赌博 (50% 概率翻倍)",
        "!slots [金额]": "老虎机 (3个相同符号赢得5倍)",
        "!pet list": "查看可领养的宠物",
        "!pet adopt [宠物名]": "领养宠物",
        "!pet info": "查看宠物信息",
        "!pet feed [金额]": "喂养宠物",
        "!market": "查看市场价格",
        "!transfer [@用户] [金额]": "转账给其他用户"
    }
