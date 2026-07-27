"""
Cognitive Schema — Brain Echo 用户认知模型数据结构定义。

结构：
  identity   用户是谁（背景、领域、长期目标）
  state      用户现在在哪（当前项目、时间、精力）
  patterns   用户习惯怎么做（学习方式、决策偏好）
  policies   Agent 应该怎么做（触发条件 + 行动指令）
  evidence   为什么这么判断（原始依据和置信度）

详见 docs/cognitive-model.md
"""

SCHEMA = {

    # ══════════════════════════════════════════════════
    # 身份层 — 影响长期交互策略
    # ══════════════════════════════════════════════════
    "identity": {
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
    },

    # ══════════════════════════════════════════════════
    # 状态层 — 改变任务规模和节奏
    # ══════════════════════════════════════════════════
    "state": {
        "active_context": {
            "type": "str",
            "description": "当前重要项目或方向",
            "importance": "high",
        },
        "time_energy": {
            "type": "str",
            "description": "当前可投入时间和精力（暑假/学期/考试周等）",
            "importance": "high",
        },
    },

    # ══════════════════════════════════════════════════
    # 模式层 — 从行为中抽象出的稳定倾向
    # 每个 pattern 对应一个 derives_policy
    # ══════════════════════════════════════════════════
    "patterns": {
        "learning_goal": {
            "type": "list",
            "description": "学习场景下的目标偏好",
            "importance": "medium",
            "derives_policy": "teaching_approach",
        },
        "learning_style": {
            "type": "list",
            "description": "学习方式偏好（principle_first / direct_answer / compare_options / hands_on）",
            "importance": "high",
            "derives_policy": "teaching_approach",
        },
        "collaboration_style": {
            "type": "list",
            "description": "用户期望的 AI 协作方式",
            "importance": "high",
            "derives_policy": "interaction_style",
        },
    },

    # ══════════════════════════════════════════════════
    # 策略层 — 由 Patterns 推导的 Agent 指令
    # 不直接从初始化收集，由 Memory Engine 生成
    # ══════════════════════════════════════════════════
    "policies": {
        "teaching_approach": {
            "type": "str",
            "description": "教学/解释类场景的 Agent 策略",
            "importance": "high",
            "trigger": "用户提出技术问题或要求学习新知识",
        },
        "interaction_style": {
            "type": "str",
            "description": "日常交互的 Agent 策略",
            "importance": "high",
            "trigger": "用户提出方案、请求帮助或表达观点",
        },
    },

    # ══════════════════════════════════════════════════
    # 证据层 — 推导依据和置信度
    # 由 Memory Engine 写入，初始化阶段为空
    # ══════════════════════════════════════════════════
    "evidence": {
        "learning_style_sources": {
            "type": "list",
            "description": "推导学习风格偏好的原始依据",
            "importance": "low",
        },
        "collaboration_sources": {
            "type": "list",
            "description": "推导协作偏好的原始依据",
            "importance": "low",
        },
    },
}


# ── 辅助函数 ──────────────────────────────────────────────────

# 旧名称映射（V0.3 → V0.4 兼容）
_OLD_TO_NEW = {
    "stable": "identity",
    "dynamic": "state",
}


def field_keys(category: str | None = None) -> list[str]:
    """返回 schema 中所有 field key 列表。

    Args:
        category: "identity" / "state" / "patterns" / "policies" / "evidence"
                  也兼容旧的 "stable" / "dynamic"
    """
    cat = _OLD_TO_NEW.get(category, category)
    if cat:
        return list(SCHEMA.get(cat, {}).keys())
    keys = []
    for c in SCHEMA:
        keys.extend(SCHEMA[c].keys())
    return keys


def category_of(field_id: str) -> str | None:
    """返回指定 field 属于哪个分类。"""
    for cat in SCHEMA:
        if field_id in SCHEMA[cat]:
            return cat
    return None


def derives_policy(field_id: str) -> str | None:
    """返回指定 pattern field 推导出的 policy 名称。"""
    for cat in ("patterns",):
        field = SCHEMA.get(cat, {}).get(field_id)
        if field:
            return field.get("derives_policy")
    return None
