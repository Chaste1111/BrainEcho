"""
Question Tree — Brain Echo Onboarding Tree v0.2（认知模型版）

设计哲学：
  不收集"用户标签"，而收集"场景偏好"。
  每个问题描述一个具体场景，用户的倾向直接对应 Pattern → 推导 Policy。

格式说明：
  id        — 唯一标识，用作答案 key
  question  — 向用户展示的题目（描述场景）
  type      — single_choice / multi_choice / text
  collect   — [schema_field_id, ...] 标识该问题写入哪些 schema 字段
  options   — [{"id": "...", "label": "..."}]（选择题用）
  depends   — {"parent_id": "required_option_id"}，父选项未选中时隐藏
  placeholder — 自由文本题的提示（仅 type=text）
  optional  — true 表示允许跳过（仅 type=text）

添加新问题：
  1. 在 QUESTIONS 列表末尾追加 dict
  2. 指定 collect 映射到 schema field
  3. 指定 depends（可选）控制可见性
  4. 无需修改引擎或生成器代码
"""

QUESTIONS = [

    # ══════════════════════════════════════════════
    # Root：所有人都回答
    # ══════════════════════════════════════════════
    {
        "id": "purpose",
        "question": "你主要希望 AI 帮助你做什么？（可多选，输入字母如 ABD）",
        "type": "multi_choice",
        "collect": ["purpose"],
        "options": [
            {"id": "learning",    "label": "学习成长"},
            {"id": "development", "label": "软件/工程开发"},
            {"id": "work",        "label": "工作效率"},
            {"id": "creation",    "label": "创作表达"},
        ],
    },

    # ══════════════════════════════════════════════
    # 学习场景（取代原来的 learning_goal + learning_style 两个问题）
    # 直接问场景偏好 → 推导 teaching_approach policy
    # ══════════════════════════════════════════════

    {
        "id": "learning_style",
        "question": "当你学习一个新知识时，你希望 AI 怎么帮你？（可多选）",
        "type": "multi_choice",
        "collect": ["learning_style", "learning_goal"],
        "depends": {"purpose": "learning"},
        "options": [
            {"id": "principle_first", "label": "先解释背景和原理，再深入细节"},
            {"id": "project_driven",  "label": "结合一个实际项目边做边学"},
            {"id": "direct_answer",   "label": "直接给答案，快速上手"},
            {"id": "compare_options", "label": "给多个方案对比，我自己选"},
        ],
    },

    # ══════════════════════════════════════════════
    # 开发场景
    # ══════════════════════════════════════════════

    {
        "id": "dev_fields",
        "question": "你主要关注哪些开发领域？（可多选）",
        "type": "multi_choice",
        "collect": ["dev_fields"],
        "depends": {"purpose": "development"},
        "options": [
            {"id": "frontend",       "label": "前端"},
            {"id": "backend",        "label": "后端"},
            {"id": "systems",        "label": "系统/底层开发"},
            {"id": "ai_engineering", "label": "AI 工程"},
            {"id": "data",           "label": "数据/算法"},
        ],
    },

    {
        "id": "skill_level",
        "question": "目前你的开发能力更接近？",
        "type": "single_choice",
        "collect": ["skill_level"],
        "depends": {"purpose": "development"},
        "options": [
            {"id": "beginner",     "label": "学习语法和基础"},
            {"id": "intermediate", "label": "能完成小项目"},
            {"id": "advanced",     "label": "能独立开发完整项目"},
            {"id": "expert",       "label": "能设计复杂系统"},
        ],
    },

    # ══════════════════════════════════════════════
    # 协作场景（所有人）
    # ══════════════════════════════════════════════

    {
        "id": "collaboration_style",
        "question": "遇到一个你不熟悉的问题时，你希望 AI 怎么和你合作？（可多选）",
        "type": "multi_choice",
        "collect": ["collaboration_style"],
        "options": [
            {"id": "quick_fix",         "label": "直接给我方案，快速解决"},
            {"id": "teach_method",      "label": "教会我方法和思路"},
            {"id": "discuss_tradeoffs", "label": "一起分析，讨论方案优劣"},
            {"id": "challenge",         "label": "挑战我的想法，指出盲点"},
        ],
    },

    # ══════════════════════════════════════════════
    # 长期目标（所有人）
    # ══════════════════════════════════════════════

    {
        "id": "long_term_goal",
        "question": "未来 2-5 年，你希望？（可多选）",
        "type": "multi_choice",
        "collect": ["long_term_goal"],
        "options": [
            {"id": "engineer", "label": "成为专业工程师"},
            {"id": "research", "label": "进入研究方向"},
            {"id": "builder",  "label": "创业/创造产品"},
            {"id": "explorer", "label": "暂时探索"},
        ],
    },

    # ══════════════════════════════════════════════
    # 时间精力（所有人）- 影响任务规模策略
    # ══════════════════════════════════════════════

    {
        "id": "time_energy",
        "question": "你目前能投入的时间大概是？",
        "type": "single_choice",
        "collect": ["time_energy"],
        "options": [
            {"id": "little",    "label": "每天 1 小时以内"},
            {"id": "moderate",  "label": "每天 1-3 小时"},
            {"id": "plenty",    "label": "每天 3 小时以上"},
            {"id": "variable",  "label": "不固定，看情况"},
        ],
    },

    # ══════════════════════════════════════════════
    # 当前上下文（所有人，可选）
    # ══════════════════════════════════════════════

    {
        "id": "active_context",
        "question": "目前有没有重要项目或方向，希望 AI 了解？",
        "type": "text",
        "collect": ["active_context"],
        "placeholder": "例如：当前项目、学习计划、研究方向（逗号分隔）",
        "optional": True,
    },
]
