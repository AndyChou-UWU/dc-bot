"""
PRISM Bot - 管理工具模块
包含: 日志、清理、欢迎消息、配置、自定义命令
"""

import discord
import json
import os
from datetime import datetime

ADMIN_DATA_FILE = "data/admin.json"
CUSTOM_COMMANDS_FILE = "data/custom_commands.json"

class AdminSystem:
    """管理系统"""
    
    def __init__(self):
        self.mod_logs = {}
        self.custom_commands = {}
        self.welcome_messages = {}
        self.load_admin_data()
    
    def load_admin_data(self):
        """加载管理数据"""
        os.makedirs("data", exist_ok=True)
        
        # 加载自定义命令
        if os.path.exists(CUSTOM_COMMANDS_FILE):
            try:
                with open(CUSTOM_COMMANDS_FILE, 'r', encoding='utf-8') as f:
                    self.custom_commands = json.load(f)
            except:
                pass
        
        # 加载日志数据
        if os.path.exists(ADMIN_DATA_FILE):
            try:
                with open(ADMIN_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.mod_logs = data.get("logs", {})
                    self.welcome_messages = data.get("welcome_messages", {})
            except:
                pass
    
    def save_admin_data(self):
        """保存管理数据"""
        data = {
            "logs": self.mod_logs,
            "welcome_messages": self.welcome_messages
        }
        with open(ADMIN_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        with open(CUSTOM_COMMANDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.custom_commands, f, ensure_ascii=False, indent=2)
    
    # ==================== 日志系统 ====================
    def log_action(self, guild_id, action, user, reason="无"):
        """记录管理员操作"""
        if str(guild_id) not in self.mod_logs:
            self.mod_logs[str(guild_id)] = []
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user": str(user),
            "reason": reason
        }
        self.mod_logs[str(guild_id)].append(log_entry)
        self.save_admin_data()
    
    def get_logs(self, guild_id, limit=10):
        """获取日志"""
        logs = self.mod_logs.get(str(guild_id), [])
        return logs[-limit:]
    
    # ==================== 欢迎消息 ====================
    def set_welcome_message(self, guild_id, message):
        """设置欢迎消息"""
        self.welcome_messages[str(guild_id)] = message
        self.save_admin_data()
        return True
    
    def get_welcome_message(self, guild_id):
        """获取欢迎消息"""
        return self.welcome_messages.get(str(guild_id), "欢迎来到我们的服务器！")
    
    def set_leave_message(self, guild_id, message):
        """设置离开消息"""
        key = f"{guild_id}_leave"
        self.welcome_messages[key] = message
        self.save_admin_data()
        return True
    
    def get_leave_message(self, guild_id):
        """获取离开消息"""
        key = f"{guild_id}_leave"
        return self.welcome_messages.get(key, "成员已离开")
    
    # ==================== 自定义命令 ====================
    def create_custom_command(self, command_name, response):
        """创建自定义命令"""
        if command_name in self.custom_commands:
            return False, "命令已存在"
        
        self.custom_commands[command_name] = {
            "response": response,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        self.save_admin_data()
        return True, f"✅ 已创建命令 `!{command_name}`"
    
    def get_custom_command(self, command_name):
        """获取自定义命令"""
        if command_name in self.custom_commands:
            cmd = self.custom_commands[command_name]
            cmd["usage_count"] += 1
            self.save_admin_data()
            return cmd["response"]
        return None
    
    def delete_custom_command(self, command_name):
        """删除自定义命令"""
        if command_name in self.custom_commands:
            del self.custom_commands[command_name]
            self.save_admin_data()
            return True, f"✅ 已删除命令 `!{command_name}`"
        return False, "命令不存在"
    
    def list_custom_commands(self):
        """列出所有自定义命令"""
        if not self.custom_commands:
            return "没有自定义命令"
        
        commands_list = "\n".join([
            f"**!{name}** - {data['response'][:50]}... (使用 {data['usage_count']} 次)"
            for name, data in self.custom_commands.items()
        ])
        return f"📋 **自定义命令列表:**\n{commands_list}"
    
    # ==================== 清理功能 ====================
    def create_cleanup_request(self, channel_id, count):
        """创建清理请求"""
        if count < 1 or count > 1000:
            return False, "必须清理 1-1000 条消息"
        return True, count
    
    # ==================== 配置系统 ====================
    def get_server_config(self, guild_id):
        """获取服务器配置"""
        config = {
            "mod_log_enabled": True,
            "welcome_message": self.get_welcome_message(guild_id),
            "leave_message": self.get_leave_message(guild_id),
            "custom_commands": len(self.custom_commands),
            "prefix": "!",
            "auto_role_enabled": False,
            "filter_enabled": False
        }
        return config
    
    def update_server_config(self, guild_id, key, value):
        """更新服务器配置"""
        if key == "welcome_message":
            return self.set_welcome_message(guild_id, value)
        elif key == "leave_message":
            return self.set_leave_message(guild_id, value)
        return False

# ==================== 命令列表 ====================
def get_admin_commands():
    """获取所有管理员命令"""
    return {
        "!prune [数量]": "删除指定数量的消息",
        "!logs [数量]": "查看操作日志",
        "!welcome [消息]": "设置欢迎消息",
        "!leave [消息]": "设置离开消息",
        "!custom add [命令] [回复]": "创建自定义命令",
        "!custom list": "列出所有自定义命令",
        "!custom delete [命令]": "删除自定义命令",
        "!kick [@用户] [原因]": "踢出成员",
        "!ban [@用户] [原因]": "封禁成员",
        "!softban [@用户] [原因]": "软封禁成员",
        "!mute [@用户]": "禁言成员",
        "!unmute [@用户]": "取消禁言",
        "!config": "查看服务器配置",
        "!config set [选项] [值]": "修改配置"
    }
