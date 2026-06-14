"""
生成专业的 Discord AI Bot 项目 PPT
使用 python-pptx 库
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from datetime import datetime

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 定义颜色方案
COLOR_DARK = RGBColor(25, 25, 112)  # 午夜蓝
COLOR_ACCENT = RGBColor(65, 105, 225)  # 皇家蓝
COLOR_HIGHLIGHT = RGBColor(255, 69, 0)  # 橙红
COLOR_TEXT = RGBColor(50, 50, 50)
COLOR_LIGHT_BG = RGBColor(240, 248, 255)

def add_title_slide(prs, title, subtitle=""):
    """添加标题页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_DARK
    
    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.word_wrap = True
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(54)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(255, 255, 255)
    
    # 副标题
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4), Inches(9), Inches(1))
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.text = subtitle
        subtitle_p = subtitle_frame.paragraphs[0]
        subtitle_p.font.size = Pt(28)
        subtitle_p.font.color.rgb = COLOR_HIGHLIGHT
    
    return slide

def add_content_slide(prs, title, content_items):
    """添加内容页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # 标题栏
    title_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(1))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = COLOR_ACCENT
    title_shape.line.color.rgb = COLOR_ACCENT
    
    # 标题文字
    title_frame = title_shape.text_frame
    title_frame.text = title
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(40)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(255, 255, 255)
    title_p.alignment = PP_ALIGN.CENTER
    
    # 内容
    left = Inches(0.8)
    top = Inches(1.5)
    for idx, item in enumerate(content_items):
        text_box = slide.shapes.add_textbox(left, top + idx * Inches(0.9), Inches(8.4), Inches(0.8))
        text_frame = text_box.text_frame
        text_frame.word_wrap = True
        
        if isinstance(item, tuple):
            title_text, desc = item
            text_frame.text = f"{title_text}"
            p = text_frame.paragraphs[0]
            p.font.size = Pt(20)
            p.font.bold = True
            p.font.color.rgb = COLOR_DARK
            
            # 描述
            p2 = text_frame.add_paragraph()
            p2.text = desc
            p2.font.size = Pt(16)
            p2.font.color.rgb = COLOR_TEXT
            p2.level = 0
        else:
            text_frame.text = f"• {item}"
            p = text_frame.paragraphs[0]
            p.font.size = Pt(18)
            p.font.color.rgb = COLOR_TEXT
            p.space_before = Pt(6)
    
    return slide

def add_two_column_slide(prs, title, left_items, right_items):
    """添加两列内容页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # 标题
    title_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(10), Inches(0.8))
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = COLOR_ACCENT
    title_shape.line.color.rgb = COLOR_ACCENT
    
    title_frame = title_shape.text_frame
    title_frame.text = title
    title_p = title_frame.paragraphs[0]
    title_p.font.size = Pt(36)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(255, 255, 255)
    title_p.alignment = PP_ALIGN.CENTER
    
    # 左列
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(4.5), Inches(5.8))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    
    for idx, item in enumerate(left_items):
        if idx == 0:
            p = left_frame.paragraphs[0]
        else:
            p = left_frame.add_paragraph()
        p.text = f"• {item}" if idx > 0 else item
        p.font.size = Pt(16)
        p.font.color.rgb = COLOR_TEXT
        p.space_before = Pt(6)
    
    # 右列
    right_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.2), Inches(4.5), Inches(5.8))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    
    for idx, item in enumerate(right_items):
        if idx == 0:
            p = right_frame.paragraphs[0]
        else:
            p = right_frame.add_paragraph()
        p.text = f"• {item}" if idx > 0 else item
        p.font.size = Pt(16)
        p.font.color.rgb = COLOR_TEXT
        p.space_before = Pt(6)
    
    return slide

# ===================== 开始创建 PPT =====================

# 第1页：标题页
add_title_slide(prs, "🤖 Discord AI 聊天机器人", 
                "Python 大作业 | 多功能 AI 助手系统")

# 第2页：项目概述
add_content_slide(prs, "📌 项目概述", [
    ("项目名称", "subaso-俗北ㄙㄡˊ Discord AI Bot"),
    ("主要目标", "为 Discord 用户提供智能化的 AI 聊天和娱乐功能"),
    ("核心技术", "Python 3.8+ | discord.py | Ollama 本地 AI | 异步编程"),
    ("版本", "v2.0.0"),
])

# 第3页：核心功能
add_content_slide(prs, "⚡ 核心功能特色", [
    "🎭 5 种 AI 角色 - 闲谈、数理、语文、程式、家务",
    "💬 连续对话 - 记住对话历史，支持多轮交互",
    "🌍 多语言支持 - 繁体中文、英文、日文、韩文、西班牙文",
    "📝 数据持久化 - 自动保存用户偏好和对话记录",
    "⚡ 本地 AI 引擎 - 基于 Ollama，无需付费 API，隐私有保障",
    "🔔 版本管理 - 实时推送更新通知给所有用户",
])

# 第4页：功能模块
add_content_slide(prs, "🎯 功能模块架构", [
    ("🤖 AI 对话系统", "多角色、多语言、连续对话、版本管理、数据保存"),
    ("💰 经济系统", "挖矿、钓鱼、狩猎、赌博、宠物系统、市场交易"),
    ("🎮 娱乐游戏", "Pokemon 猜谜、Trivia 问答、动漫角色、数字游戏"),
    ("⚙️ 管理工具", "日志管理、消息清理、欢迎消息、自定义命令"),
])

# 第5页：AI 角色详解
add_two_column_slide(prs, "🎭 5 大 AI 角色详解",
    ["✅ 闲谈 - 友善幽默的日常聊天伙伴",
     "🔢 数理 - 数学和科学问题专家",
     "📚 语文 - 语言文学和写作指导"],
    ["💻 程式 - 编程技术问题解决",
     "🏠 家务 - 生活烹饪清洁建议"])

# 第6页：技术架构
add_content_slide(prs, "🔧 技术栈与架构", [
    ("编程语言", "Python 3.8+ | 异步编程 (asyncio)"),
    ("主要库", "discord.py 2.0+ | aiohttp | httpx | python-dotenv"),
    ("AI 引擎", "Ollama (本地轻量级 LLM) | Qwen2.5-1.5B 模型"),
    ("数据存储", "JSON 文件存储 | user_data.json 用户数据"),
    ("日志系统", "结构化日志 | 文件和控制台输出 | UTF-8 编码支持"),
])

# 第7页：系统架构图（文字描述）
add_two_column_slide(prs, "📐 系统架构",
    ["Discord API",
     "↓",
     "bot.py (主程序)",
     "↓",
     "prism_config.py",
     "↓",
     "Ollama AI"],
    ["用户交互",
     "↓",
     "命令处理",
     "↓",
     "AI 角色切换",
     "↓",
     "本地智能回复"])

# 第8页：工作流程
add_content_slide(prs, "🔄 工作流程", [
    "1️⃣ 用户在 Discord 发送消息或命令",
    "2️⃣ Bot 接收事件，解析命令和参数",
    "3️⃣ 根据选定的 AI 角色，构建 system prompt",
    "4️⃣ 调用 Ollama API，发送消息和对话历史",
    "5️⃣ Ollama 本地推理，返回 AI 回复",
    "6️⃣ Bot 格式化回复，发送到 Discord",
    "7️⃣ 保存对话记录和用户数据到本地文件",
])

# 第9页：使用示例
add_content_slide(prs, "💡 使用示例", [
    ("数学问题", "/ai 数理 如何求解二次方程？"),
    ("日常闲聊", "/ai 闲谈 今天天气真好！"),
    ("编程帮助", "/ai 程式 Python 中如何定义类？"),
    ("语文指导", "/ai 语文 怎样写出好的开头？"),
    ("生活建议", "/ai 家务 如何快速清洁厨房？"),
])

# 第10页：技术亮点
add_content_slide(prs, "✨ 技术亮点", [
    "🔐 异步编程 - 高效处理多个并发用户请求",
    "🎯 面向对象设计 - 清晰的模块划分和可扩展性",
    "🔄 状态管理 - 完整的用户数据和对话历史管理",
    "🌐 API 集成 - 与 Discord 和 Ollama 的无缝对接",
    "📊 日志系统 - 结构化日志便于调试和监控",
    "🔧 配置管理 - 集中配置，易于自定义和维护",
])

# 第11页：环境要求
add_two_column_slide(prs, "📋 环境与依赖",
    ["硬件要求:",
     "• Python 3.8+",
     "• 8GB+ 内存",
     "• 15GB+ 磁盘空间",
     "• 网络连接"],
    ["软件依赖:",
     "• discord.py >= 2.0.0",
     "• python-dotenv",
     "• aiohttp",
     "• Ollama (本地 AI)",
     "• Discord Token"])

# 第12页：部署方式
add_content_slide(prs, "🚀 部署与运行", [
    "1️⃣ 安装依赖：pip install -r requirements.txt",
    "2️⃣ 安装 Ollama：https://ollama.ai",
    "3️⃣ 拉取模型：ollama pull Qwen2.5-1.5B-Instruct",
    "4️⃣ 配置 Token：在 設定.env 中设置 DISCORD_TOKEN",
    "5️⃣ 启动 Bot：python bot.py",
    "6️⃣ Docker 部署：docker build -t dcard-bot . && docker run ...",
])

# 第13页：改进与展望
add_content_slide(prs, "🎯 改进与展望", [
    "🔮 未来计划",
    "• 支持更多 AI 模型（GPT、Claude 等付费 API）",
    "• 添加语音交互功能",
    "• 实现用户权限管理系统",
    "• 开发 Web 控制面板",
    "• 支持数据库存储（MongoDB、PostgreSQL）",
    "• 多服务器部署和负载均衡",
])

# 第14页：项目成果
add_content_slide(prs, "🏆 项目成果与创新", [
    ("完整性", "完全自主开发，功能模块齐全，代码规范清晰"),
    ("创新性", "结合本地 AI 和 Discord Bot，提供隐私保护的智能助手"),
    ("可用性", "开箱即用，配置简单，文档详细"),
    ("可扩展性", "模块化设计，易于添加新功能和新角色"),
    ("学习价值", "综合运用 Python 异步编程、API 开发、数据管理等技能"),
])

# 第15页：结论
slide = prs.slides.add_slide(prs.slide_layouts[6])
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = COLOR_DARK

conclusion_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3.5))
conclusion_frame = conclusion_box.text_frame
conclusion_frame.word_wrap = True

p1 = conclusion_frame.paragraphs[0]
p1.text = "感谢评审！"
p1.font.size = Pt(48)
p1.font.bold = True
p1.font.color.rgb = COLOR_HIGHLIGHT
p1.alignment = PP_ALIGN.CENTER

p2 = conclusion_frame.add_paragraph()
p2.text = "\n本项目展示了现代 Python 开发的最佳实践\n以及 AI 应用的实际部署能力"
p2.font.size = Pt(24)
p2.font.color.rgb = RGBColor(255, 255, 255)
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(20)

p3 = conclusion_frame.add_paragraph()
p3.text = "\n源代码已上传 GitHub"
p3.font.size = Pt(18)
p3.font.color.rgb = RGBColor(200, 200, 200)
p3.alignment = PP_ALIGN.CENTER
p3.space_before = Pt(40)

# 保存 PPT
output_path = "Discord_AI_Bot_大作业_演示.pptx"
prs.save(output_path)
print(f"✅ PPT 已生成：{output_path}")
print(f"📊 共 {len(prs.slides)} 页幻灯片")
print(f"⏰ 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
