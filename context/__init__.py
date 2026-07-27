"""
Context Builder — 从用户画像生成注入 Claude 的上下文。

职责：
  读取 profile/profile.md → 格式化为 system prompt 片段
  → 通过 --append-system-prompt 注入 Claude。

未来扩展：
  build_context(target="claude")    → 拼成 CLI 参数格式（当前）
  build_context(target="deepseek")  → 拼成 API system message 格式

  build_context(from_dict={...})    → 从内存 dict 注入，不读文件
  （V0.4 Memory Layer 使用）
"""

import os

# profile 文件默认路径（相对项目根目录）
PROFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_PROFILE = os.path.join(PROFILE_DIR, "profile", "profile.md")


def build_context(
    profile_path: str | None = None,
    *,
    from_dict: dict | None = None,
    target: str = "claude",
) -> str:
    """读取用户画像，构建注入上下文字符串。

    Args:
        profile_path: profile 文件路径，默认 profile/profile.md
        from_dict: 从内存 dict 直接构建（V0.4+），优先级高于 profile_path
        target: 输出目标格式，当前仅支持 "claude"

    Returns:
        注入上下文字符串（空字符串 = 无 profile 可加载）
    """
    if from_dict:
        content = _format_from_dict(from_dict)
    else:
        content = _read_profile_file(profile_path or DEFAULT_PROFILE)

    if not content:
        return ""

    return _format_context(content, target=target)


def _read_profile_file(path: str) -> str:
    """从文件读取 raw markdown 内容。"""
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except (OSError, UnicodeDecodeError) as e:
        print(f"[Brain Echo] 警告：读取 profile 失败 ({e})", file=__import__("sys").stderr)
        return ""


def _format_from_dict(data: dict) -> str:
    """将 profile.json 的 stable/dynamic 结构格式化为可读文本。

    Args:
        data: profile.json 内容（含 stable 和 dynamic）

    Returns:
        纯文本上下文（不含包装头，_format_context 会加）
    """
    lines = []

    for category in ("stable", "dynamic"):
        section = data.get(category, {})
        if not section:
            continue
        cat_label = "Stable Identity" if category == "stable" else "Current State"
        lines.append(f"## {cat_label}")
        lines.append("")
        for key, value in section.items():
            if isinstance(value, list):
                lines.append(f"- {key}: {', '.join(value)}")
            else:
                lines.append(f"- {key}: {value}")
        lines.append("")

    return "\n".join(lines).strip()


def _format_context(raw: str, target: str = "claude") -> str:
    """将 raw 内容包装为注入上下文。"""
    # 去头尾空行，保留 markdown 结构但压缩连续空行
    lines = [line.rstrip() for line in raw.splitlines()]

    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()

    result = []
    prev_blank = False
    for line in lines:
        is_blank = not line
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank

    formatted = "\n".join(result).strip()

    # 包装为 Claude 可读的注入上下文
    if target == "claude":
        context = (
            "# User Context (from Brain Echo)\n"
            f"The following is known about the user you are assisting:\n\n"
            f"{formatted}\n\n"
            "Use this information to tailor your responses to the user's "
            "background, preferences, and goals."
        )
    else:
        # 未来扩展其他 target（deepseek 等）
        context = formatted

    return context


def profile_exists() -> bool:
    """检查是否存在可用的 profile 文件。"""
    return os.path.isfile(DEFAULT_PROFILE)
