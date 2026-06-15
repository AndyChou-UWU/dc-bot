"""
PRISM Bot - 經濟系統模塊
包含: 挖礦、釣魚、狩獵、賭博、寵物、市場交易
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
    """經濟系統管理"""
    
    def __init__(self):
        self.user_wallets = {}
        self.user_pets = {}
        self.user_cooldowns = {}
        self.load_economy_data()
    
    def load_economy_data(self):
        """加載經濟數據"""
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
        """保存經濟數據"""
        data = {
            "wallets": {str(k): v for k, v in self.user_wallets.items()},
            "pets": {str(k): v for k, v in self.user_pets.items()}
        }
        with open(ECONOMY_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_balance(self, user_id):
        """獲取用戶餘額"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        return self.user_wallets[user_id]["balance"]
    
    def add_balance(self, user_id, amount):
        """增加餘額"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        self.user_wallets[user_id]["balance"] += amount
        self.save_economy_data()
        return self.user_wallets[user_id]["balance"]
    
    def subtract_balance(self, user_id, amount):
        """減少餘額"""
        if user_id not in self.user_wallets:
            self.user_wallets[user_id] = {"balance": STARTING_BALANCE, "created_at": datetime.now().isoformat()}
        
        if self.user_wallets[user_id]["balance"] >= amount:
            self.user_wallets[user_id]["balance"] -= amount
            self.save_economy_data()
            return True
        return False
    
    def transfer_balance(self, from_id, to_id, amount):
        """轉賬"""
        if self.subtract_balance(from_id, amount):
            self.add_balance(to_id, amount)
            return True
        return False
    
    # ==================== 挖礦系統 ====================
    def can_mine(self, user_id):
        """檢查是否可以挖礦"""
        return self.check_cooldown(user_id, "mine", 60)
    
    def mine(self, user_id):
        """挖礦"""
        ore_type = random.choice(list(MINING_REWARDS.keys()))
        reward_info = MINING_REWARDS[ore_type]
        amount = reward_info["amount"]
        
        self.add_balance(user_id, amount)
        return ore_type, amount, reward_info["emoji"]
    
    # ==================== 釣魚系統 ====================
    def can_fish(self, user_id):
        """檢查是否可以釣魚"""
        return self.check_cooldown(user_id, "fish", 60)
    
    def fish(self, user_id):
        """釣魚"""
        catch = random.choice(list(FISHING_CATCHES.keys()))
        catch_info = FISHING_CATCHES[catch]
        amount = catch_info["amount"]
        
        self.add_balance(user_id, amount)
        return catch, amount, catch_info["emoji"]
    
    # ==================== 狩獵系統 ====================
    def can_hunt(self, user_id):
        """檢查是否可以狩獵"""
        return self.check_cooldown(user_id, "hunt", 120)
    
    def hunt(self, user_id):
        """狩獵"""
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
    
    # ==================== 賭博系統 ====================
    def gamble(self, user_id, amount):
        """賭博"""
        if not self.subtract_balance(user_id, amount):
            return False, 0, "餘額不足"
        
        if random.random() < 0.5:  # 50% 贏的概率
            winnings = amount * 2
            self.add_balance(user_id, winnings)
            return True, winnings, "贏了！"
        else:
            return False, 0, "輸了..."
    
    def slots(self, user_id, amount):
        """老虎機"""
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
    
    # ==================== 寵物系統 ====================
    def adopt_pet(self, user_id, pet_name):
        """領養寵物"""
        if user_id in self.user_pets:
            return False, "你已經有一隻寵物了"
        
        if pet_name not in PETS:
            return False, f"不存在的寵物: {pet_name}"
        
        pet_info = PETS[pet_name]
        self.user_pets[user_id] = {
            "name": pet_name,
            "adopted_at": datetime.now().isoformat(),
            "mood": 100,
            "emoji": pet_info["emoji"]
        }
        self.save_economy_data()
        return True, f"成功領養了 {pet_info['emoji']} {pet_name}！"
    
    def get_pet(self, user_id):
        """獲取寵物信息"""
        if user_id not in self.user_pets:
            return None
        return self.user_pets[user_id]
    
    def feed_pet(self, user_id, amount):
        """餵養寵物"""
        pet = self.get_pet(user_id)
        if not pet:
            return False, "你沒有寵物"
        
        if not self.subtract_balance(user_id, amount):
            return False, "餘額不足"
        
        pet["mood"] = min(100, pet["mood"] + 20)
        self.save_economy_data()
        return True, f"你的寵物開心了！心情: {pet['mood']}/100"
    
    # ==================== 市場系統 ====================
    def list_market_prices(self):
        """列出市場價格"""
        prices = {
            "挖礦收入": {
                "鐵": MINING_REWARDS["iron"]["amount"],
                "金": MINING_REWARDS["gold"]["amount"],
                "鑽": MINING_REWARDS["diamond"]["amount"]
            },
            "釣魚收入": FISHING_CATCHES
        }
        return prices
    
    # ==================== 冷卻時間 ====================
    def check_cooldown(self, user_id, action, cooldown_seconds):
        """檢查冷卻時間"""
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

# ==================== 命令處理函數 ====================
def get_economy_commands():
    """獲取所有經濟系統命令"""
    return {
        "!balance": "查看餘額",
        "!mine": "挖礦 (冷卻 60秒)",
        "!fish": "釣魚 (冷卻 60秒)",
        "!hunt": "狩獵 (冷卻 120秒)",
        "!gamble [金額]": "賭博 (50% 概率翻倍)",
        "!slots [金額]": "老虎機 (3個相同符號贏得5倍)",
        "!pet list": "查看可領養的寵物",
        "!pet adopt [寵物名]": "領養寵物",
        "!pet info": "查看寵物信息",
        "!pet feed [金額]": "餵養寵物",
        "!market": "查看市場價格",
        "!transfer [@用戶] [金額]": "轉賬給其他用戶"
    }
