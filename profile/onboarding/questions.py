"""
Question Tree — Brain Echo Onboarding Tree v0.1

问题树是纯配置数据，不含执行逻辑。
引擎（engine.py）负责遍历、渲染、收集。

格式说明：
  id        — 唯一标识，用作答案 key
  question  — 向用户展示的题目
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
        "question": "你主要希望 AI 帮助你什么？（可多选，输入字母如 ABD）",
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
    # 学习分支
    # ══════════════════════════════════════════════

    {
        "id": "learning_goal",
        "question": "你使用 AI 学习主要为了？（可多选）",
        "type": "multi_choice",
        "collect": ["learning_goal"],
        "depends": {"purpose": "learning"},
        "options": [
            {"id": "quick_grasp",       "label": "快速掌握知识完成任务"},
            {"id": "deep_understanding", "label": "建立系统理解"},
            {"id": "project_driven",    "label": "解决实际项目问题"},
            {"id": "exploration",       "label": "探索未来方向"},
        ],
    },

    {
        "id": "learning_style",
        "question": "你更喜欢 AI 如何帮你学习？（可多选）",
        "type": "multi_choice",
        "collect": ["learning_style"],
        "depends": {"purpose": "learning"},
        "options": [
            {"id": "direct_answer",   "label": "直接给答案"},
            {"id": "principle_first", "label": "解释原理后给方案"},
            {"id": "guide_think",     "label": "通过提问引导我思考"},
            {"id": "compare_options", "label": "给多个方案比较"},
        ],
    },

    # ══════════════════════════════════════════════
    # 开发分支
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
        "id": "dev_systems",
        "question": "你在系统开发方面对哪些方向感兴趣？（可多选）",
        "type": "multi_choice",
        "collect": ["dev_systems"],
        "depends": {"dev_fields": "systems"},
        "options": [
            {"id": "linux",        "label": "Linux"},
            {"id": "networking",   "label": "网络"},
            {"id": "os",           "label": "操作系统"},
            {"id": "performance",  "label": "高性能计算"},
            {"id": "database",     "label": "数据库"},
            {"id": "compiler",     "label": "编译器"},
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
    # 协作方式（所有人）
    # ══════════════════════════════════════════════

    {
        "id": "collaboration_style",
        "question": "遇到问题时，你希望 AI 如何与你协作？（可多选）",
        "type": "multi_choice",
        "collect": ["collaboration_style"],
        "options": [
            {"id": "quick_fix",       "label": "快速解决"},
            {"id": "teach_method",    "label": "教会我方法"},
            {"id": "discuss_tradeoffs", "label": "和我一起分析决策"},
            {"id": "challenge",       "label": "挑战我的想法"},
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
