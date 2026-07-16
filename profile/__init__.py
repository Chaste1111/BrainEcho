"""
Profile — 用户画像生命周期管理。

结构：
  changes.json       变化记录（V0.4+ 使用）
  profile.json       结构化用户画像（JSON，程序处理用）
  profile.md         人类+LLM 可读的用户画像（注入 Claude 用）

  onboarding/        初始化引擎模块
    __init__.py      门面（暴露给 main.py）
    engine.py        树遍历引擎
    questions.py     问题树数据（纯配置）
    schema.py        Memory Schema 定义
    generator.py     答案生成器（answers → profile.md + profile.json）
"""
