"""
Memory Schema — Brain Echo 用户画像数据结构定义。

定义"Brain Echo 认为一个人应该被如何描述"。

结构：
  stable    不常变化的身份属性（目的、兴趣、风格等）
  dynamic   随时间和上下文变化的状态（当前项目、精力等）

扩展方式：
  在对应分类下追加 field 定义即可。引擎无需修改。
"""

SCHEMA = {

    # ══════════════════════════════════════════════════
    # 稳定身份 — 影响长期交互策略
    # ══════════════════════════════════════════════════
    "stable": {
        "purpose": {
            "type": "list",
            "description": "用户使用 AI 的主要目的",
            "importance": "high",
        },
        "long_term_goal": {
            "type": "list",
            "description": "长期职业或人生目标",
            "importance": "high",
        },
        "skill_level": {
            "type": "str",
            "description": "当前能力水平",
            "importance": "high",
        },
        "learning_goal": {
            "type": "list",
            "description": "学习场景下的目标偏好",
            "importance": "medium",
        },
        "learning_style": {
            "type": "list",
            "description": "学习方式偏好",
            "importance": "medium",
        },
        "dev_fields": {
            "type": "list",
            "description": "关注的开发领域",
            "importance": "medium",
        },
        "dev_systems": {
            "type": "list",
            "description": "系统开发方向细化",
            "importance": "low",
        },
        "collaboration_style": {
            "type": "list",
            "description": "用户期望的 AI 协作方式",
            "importance": "high",
        },
    },

    # ══════════════════════════════════════════════════
    # 实时状态 — 由 Memory Layer 更新（V0.4+）
    # ══════════════════════════════════════════════════
    "dynamic": {
        "active_context": {
            "type": "str",
            "description": "当前重要项目或方向",
            "importance": "high",
        },
    },
}


# ── 辅助函数 ──────────────────────────────────────────────────


def field_keys(category: str | None = None) -> list[str]:
    """返回 schema 中所有 field key 列表。

    Args:
        category: "stable" / "dynamic"，为 None 返回全部。
    """
    if category:
        return list(SCHEMA.get(category, {}).keys())
    keys = []
    for cat in SCHEMA:
        keys.extend(SCHEMA[cat].keys())
    return keys


def category_of(field_id: str) -> str | None:
    """返回指定 field 属于 stable 还是 dynamic。"""
    for cat in SCHEMA:
        if field_id in SCHEMA[cat]:
            return cat
    return None
