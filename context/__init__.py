"""
Context Builder — 从用户画像生成注入 Claude 的上下文。

职责：
  读取 profile/user.md → 格式化为 system prompt 片段
  → 通过 --append-system-prompt 注入 Claude。

使用：
  context = build_context()
  # → 返回字符串，空表示无 profile 文件
"""

import os

# profile 文件默认路径（相对项目根目录）
PROFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_PROFILE = os.path.join(PROFILE_DIR, "profile", "profile.md")


def build_context(profile_path: str | None = None) -> str:
    """读取用户画像，构建注入上下文字符串。

    Args:
        profile_path: profile 文件路径，默认 profile/profile.md

    Returns:
        注入上下文字符串（空字符串 = 无 profile 可加载）
    """
    path = profile_path or DEFAULT_PROFILE

    if not os.path.isfile(path):
        return ""

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except (OSError, UnicodeDecodeError) as e:
        print(f"[Brain Echo] 警告：读取 profile 失败 ({e})", file=__import__("sys").stderr)
        return ""

    if not content:
        return ""

    return _format_context(content)


def _format_context(raw: str) -> str:
    """将 markdown profile 格式化为简洁的注入上下文。"""
    # 去头尾空行，保留 markdown 结构但压缩连续空行
    lines = [line.rstrip() for line in raw.splitlines()]

    # 去除前导/尾随空行
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()

    # 压缩连续空行为单空行
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
    context = (
        "# User Context (from Brain Echo)\n"
        f"The following is known about the user you are assisting:\n\n"
        f"{formatted}\n\n"
        "Use this information to tailor your responses to the user's "
        "background, preferences, and goals."
    )

    return context


def profile_exists() -> bool:
    """检查是否存在可用的 profile 文件。"""
    return os.path.isfile(DEFAULT_PROFILE)
