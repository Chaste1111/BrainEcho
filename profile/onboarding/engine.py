"""
Engine — 树形问题遍历引擎

职责：
  遍历问题树 → 按依赖过滤 → 渲染题目 → 收集答案 → 返回答案 dict

与问题数据完全解耦：questions.py 加新问题不需要修改引擎代码。

类型支持：
  single_choice  — 单选（输入一个字母）
  multi_choice   — 多选（输入字母组合，如 ABD）
  text           — 自由文本（输入文字）
"""

import sys

# ── 公开接口 ──────────────────────────────────────────────────


def walk(questions: list[dict]) -> dict:
    """交互式遍历问题树，返回答案 dict。

    返回值格式：
      {
        "question_id": str | list[str],
        ...
      }
      - single_choice → str（选项 id）
      - multi_choice  → list[str]（选项 id 列表）
      - text          → str（用户输入文本）
    """
    answers = {}

    print()
    print("=" * 56)
    print("  欢迎使用 Brain Echo — 让我们先了解你")
    print("=" * 56)
    print()
    print("需要回答几个简单问题，帮你获得更贴切的回答。")
    print()

    for question in questions:
        if not _is_visible(question, answers):
            continue
        answer = _ask(question)
        answers[question["id"]] = answer
        print()

    return answers


# ── 可见性判断 ──────────────────────────────────────────────


def _is_visible(question: dict, answers: dict) -> bool:
    """根据已收集的答案判断该问题是否应对用户可见。"""
    depends = question.get("depends")
    if not depends:
        return True

    for parent_id, required_opt in depends.items():
        if parent_id not in answers:
            return False
        parent_answer = answers[parent_id]

        # multi_choice 父问题：检查列表是否包含 required_opt
        if isinstance(parent_answer, list):
            if required_opt not in parent_answer:
                return False
        # single_choice / text 父问题：检查值是否匹配
        else:
            if parent_answer != required_opt:
                return False

    return True


# ── 题目渲染 ────────────────────────────────────────────────


def _ask(question: dict):
    """渲染一道题目，返回用户答案。"""
    qtype = question["type"]

    if qtype in ("single_choice", "multi_choice"):
        return _ask_choice(question, multi=(qtype == "multi_choice"))
    elif qtype == "text":
        return _ask_text(question)
    else:
        print(f"[Brain Echo] 未知题目类型: {qtype}", file=sys.stderr)
        return ""


def _ask_choice(question: dict, multi: bool) -> str | list[str]:
    """渲染选择题（单选/多选）。"""
    options = question["options"]
    label = question["question"]

    # 打印题目
    print(f"[{question['id']}] {label}")

    # 打印选项
    for i, opt in enumerate(options):
        letter = chr(ord("A") + i)
        print(f"  {letter}. {opt['label']}")

    # 选项字母 → id 映射
    letter_to_id = {chr(ord("A") + i): opt["id"] for i, opt in enumerate(options)}
    valid_letters = set(letter_to_id.keys())

    # 提示文字
    prompt = "  请输入选项字母："
    if multi:
        prompt = "  请输入选项字母（多选用空格分隔，如 A B C）："

    while True:
        try:
            raw = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(1)

        raw = raw.strip().upper()

        if multi:
            chosen = raw.split()
        else:
            chosen = [raw]

        # 验证每个输入是有效选项
        if not chosen or not all(c in valid_letters for c in chosen):
            valid_str = ", ".join(sorted(valid_letters))
            print(f"  请输入 {valid_str} 中的选项")
            continue

        # 去重（多选场景）
        seen = set()
        unique = []
        for c in chosen:
            if c not in seen:
                seen.add(c)
                unique.append(c)

        if multi:
            return [letter_to_id[c] for c in unique]
        else:
            return letter_to_id[unique[0]]


def _ask_text(question: dict) -> str:
    """渲染自由文本题。"""
    print(f"[{question['id']}] {question['question']}")

    placeholder = question.get("placeholder", "")
    if placeholder:
        print(f"  ({placeholder})")

    optional = question.get("optional", False)

    while True:
        try:
            raw = input("  > ")
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(1)

        raw = raw.strip()
        if raw:
            return raw
        if optional:
            return ""
