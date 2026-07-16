"""
Generator — 将 Onboarding 答案转换为 profile.md + profile.json

职责：
  接收 engine.walk() 返回的 answers dict
  → 按 schema 分组（stable / dynamic）
  → 生成程序可处理的 profile.json
  → 生成人类+LLM 可读的 profile.md
  → 写入 profile/ 目录
"""

import json
import os
from datetime import date

# profile 文件路径
_PROFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE_MD = os.path.join(_PROFILE_DIR, "profile.md")
PROFILE_JSON = os.path.join(_PROFILE_DIR, "profile.json")
CHANGES_JSON = os.path.join(_PROFILE_DIR, "changes.json")

# ── 章节展示名称映射 ──────────────────────────────────────
_SECTION_TITLES = {
    "purpose":             "Purpose",
    "learning_goal":       "Learning Goals",
    "learning_style":      "Learning Style",
    "dev_fields":          "Development Focus",
    "dev_systems":         "Systems Interest",
    "skill_level":         "Skill Level",
    "long_term_goal":      "Long-term Goals",
    "collaboration_style": "Collaboration Style",
    "active_context":      "Current Context",
}

# ── 章节排序（控制 profile.md 中的输出顺序） ──────────
_SECTION_ORDER = [
    "purpose",
    "long_term_goal",
    "skill_level",
    "learning_goal",
    "learning_style",
    "dev_fields",
    "dev_systems",
    "collaboration_style",
    "active_context",
]

# ── 公开接口 ──────────────────────────────────────────────────


def generate(answers: dict, questions: list[dict]) -> tuple[str, str]:
    """根据 answers + schema 分组生成 profile，写入文件。

    Returns:
        (md_path, json_path)
    """
    label_map = _build_label_map(questions)
    today = date.today().isoformat()

    # 1. 按 schema 分组（stable / dynamic）
    profile_data = _structure_by_schema(answers, label_map)

    # 2. 生成 JSON
    json_data = {
        "version": "0.3.0",
        "created": today,
        "updated": today,
        "stable": profile_data.get("stable", {}),
        "dynamic": profile_data.get("dynamic", {}),
        "raw_answers": answers,
    }

    # 3. 生成 markdown
    md_content = _to_markdown(profile_data, today)

    # 4. 写入文件
    os.makedirs(os.path.dirname(PROFILE_MD), exist_ok=True)
    with open(PROFILE_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    with open(PROFILE_JSON, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # 5. 确保 changes.json 存在（空占位）
    if not os.path.isfile(CHANGES_JSON):
        with open(CHANGES_JSON, "w", encoding="utf-8") as f:
            json.dump([], f)

    print("✓ 用户画像已保存")
    print()

    return PROFILE_MD, PROFILE_JSON


# ── label 映射构建 ──────────────────────────────────────────


def _build_label_map(questions: list[dict]) -> dict[str, str]:
    """从问题定义中提取 option id → label 映射。"""
    m = {}
    for q in questions:
        for opt in q.get("options", []):
            m[opt["id"]] = opt["label"]
    return m


# ── Schema 分组 ─────────────────────────────────────────────


def _structure_by_schema(answers: dict, label_map: dict) -> dict:
    """将答案按 schema 分组为 stable / dynamic。"""
    # 初始化结构
    result = {"stable": {}, "dynamic": {}}

    # 从 schema.py 获取字段归属
    from .schema import category_of

    for qid, answer in answers.items():
        if not answer:
            continue
        if isinstance(answer, list) and not answer:
            continue

        # 转换成可读 label
        if isinstance(answer, list):
            value = [label_map.get(oid, oid) for oid in answer]
        else:
            value = label_map.get(answer, answer)

        # 根据 schema 决定归属
        cat = category_of(qid)
        if cat:
            result[cat][qid] = value

    return result


# ── Markdown 生成 ───────────────────────────────────────────


def _to_markdown(profile_data: dict, today: str) -> str:
    lines = [
        "# User Profile",
        "",
        f"Created: {today}",
        f"Updated: {today}",
        "",
    ]

    for qid in _SECTION_ORDER:
        # 从 stable 或 dynamic 中找值
        value = profile_data.get("stable", {}).get(qid) or profile_data.get("dynamic", {}).get(qid)
        if not value:
            continue

        title = _SECTION_TITLES.get(qid, qid)
        lines.append(f"## {title}")
        lines.append("")

        if isinstance(value, list):
            for item in value:
                lines.append(f"- {item}")
        else:
            lines.append(f"{value}")

        lines.append("")

    # 去尾随空行
    while lines and not lines[-1]:
        lines.pop()

    return "\n".join(lines) + "\n"
