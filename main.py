#!/usr/bin/env python3
"""
Brain Echo — Agent 上层个人智能层入口

架构:
  main.py        → 入口分发：Brain Echo 命令 / 初始化 / Claude 启动
  adapter/       → Claude CLI 启动封装（路径探测、参数构建、subprocess）
  context/       → 用户上下文构建（读取 profile → 注入 Claude）
  profile/       → 用户画像 + 初始化流程（onboarding）

添加新命令：
  1. 在 main() 的 Brain Echo 命令拦截区加 if 分支
  2. 在 HELP_TEXT 中登记
  3. 不认识的参数自动透传 Claude，无需处理

V0.3 初始化层：brain → 首次问答建画像 → 注入 Claude
"""

import os
import sys

from adapter import (
    resolve_claude,
    build_args,
    launch_claude,
    is_interactive,
)
from context import build_context
from profile.onboarding import needs_onboarding, run_onboarding, confirm_overwrite

# ── 版本信息 ──────────────────────────────────────────────────
VERSION = "0.3.0"
HELP_TEXT = f"""Brain Echo {VERSION} — Agent 上层个人智能层入口

用法:
  brain                          启动交互式 Claude 会话（自动初始化和注入）
  brain "你的输入"               同上，带初始 prompt
  brain --version / -v           显示版本号
  brain --help / -h              显示此帮助
  brain --onboarding             强制重新初始化用户画像

除上述命令外，其余所有参数原样透传给 Claude CLI（如 --model、--print 等）。
详细参数列表请查看: claude --help

项目位置: ~/Projects/BrainEcho/"""

# ── 递归执行保护 ──────────────────────────────────────────────
_BRAIN_ECHO_SENTINEL = "BRAIN_ECHO_ALREADY_LAUNCHED"


def _guard_recursive_launch():
    """防止 brain 在 Claude 内部再次调用 brain 形成无限循环。"""
    if os.environ.get(_BRAIN_ECHO_SENTINEL):
        print("[Brain Echo] 检测到递归调用，跳过入口层直接启动 Claude。", file=sys.stderr)
        return False
    os.environ[_BRAIN_ECHO_SENTINEL] = "1"
    return True


# ── 入口 ─────────────────────────────────────────────────────
def main():
    # ── Brain Echo 自身命令拦截 ──────────────────────────
    if any(arg in {"--version", "-v"} for arg in sys.argv[1:]):
        print(f"Brain Echo {VERSION}")
        return
    if any(arg in {"--help", "-h"} for arg in sys.argv[1:]):
        print(HELP_TEXT, end="")
        return

    # ── 递归保护 ─────────────────────────────────────────
    if not _guard_recursive_launch():
        os.execvp("claude", ["claude"] + sys.argv[1:])

    interactive = is_interactive(sys.argv[1:])

    # ── 探测 Claude ──────────────────────────────────────
    claude_path = resolve_claude()
    if claude_path is None:
        print(
            "错误：未找到 Claude CLI。请确认已安装 Claude Code。\n"
            "  npm install -g @anthropic-ai/claude-code\n"
            "  或参考 https://docs.anthropic.com/en/docs/claude-code/setup",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 强制重新初始化（--onboarding） ────────────────────
    if any(arg == "--onboarding" for arg in sys.argv[1:]):
        if not interactive:
            print("错误：--onboarding 需要交互式终端。", file=sys.stderr)
            sys.exit(1)
        # 过滤掉 --onboarding，不让它传给 Claude
        filtered_args = [a for a in sys.argv[1:] if a != "--onboarding"]
        sys.argv[1:] = filtered_args

        if not confirm_overwrite():
            print("已取消。")
            sys.exit(0)
        run_onboarding()
        # 继续往下走，加载新的 profile 并启动 Claude

    # ── 首次检查：是否需要初始化 ──────────────────────────
    elif needs_onboarding():
        if not interactive:
            print(
                "Brain Echo: profile missing.\n"
                "Run `brain --onboarding` first.",
                file=sys.stderr,
            )
            sys.exit(1)
        run_onboarding()

    # ── 构建用户上下文 ────────────────────────────────────
    context = build_context()

    # ── 构建 Claude 参数（注入 context） ──────────────────
    claude_args = build_args(sys.argv[1:], context=context)

    # ── 启动头（仅交互模式） ────────────────────────────
    if interactive:
        print(f"Brain Echo {VERSION}", flush=True)
        print(flush=True)
        print("Loading user context...", flush=True)
        if context:
            print("✓ user profile loaded", flush=True)
        else:
            print("  (no profile)", flush=True)
        print(flush=True)
        print("Starting Claude...", flush=True)
        print(flush=True)

    # ── 启动 Claude ──────────────────────────────────────
    return_code = launch_claude(claude_path, claude_args)

    # ── 退出清理 ─────────────────────────────────────────
    from adapter import _reset_terminal
    _reset_terminal(clear_screen=interactive)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
