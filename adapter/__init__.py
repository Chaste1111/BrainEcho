"""
Adapter — Claude CLI 启动封装。

职责：
  探测 claude 路径、构建参数列表、subprocess 启动。
  main.py 不直接接触 subprocess。
"""

import os
import sys
import subprocess

# ── Claude CLI 路径探测 ──────────────────────────────────────


def resolve_claude() -> str | None:
    """从 PATH 和常见安装位置寻找 claude 可执行文件。"""
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for d in path_dirs:
        candidate = os.path.join(d, "claude")
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    home = os.path.expanduser("~")
    fallbacks = [
        os.path.join(home, ".local", "bin", "claude"),
        os.path.join(home, "bin", "claude"),
        "/usr/local/bin/claude",
    ]
    for p in fallbacks:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p

    return None


# ── 参数构建 ──────────────────────────────────────────────────


def build_args(
    user_args: list[str],
    *,
    context: str = "",
) -> list[str]:
    """构建传给 Claude CLI 的完整参数列表。

    Args:
        user_args: 用户传入的原始参数（sys.argv[1:] 的过滤后版本）
        context: 要注入的用户上下文（空字符串不注入）

    Returns:
        完整的 Claude CLI 参数列表
    """
    args = list(user_args)

    # 如果有上下文，通过 --append-system-prompt 注入
    if context:
        args = ["--append-system-prompt", context] + args

    return args


# ── 启动 ─────────────────────────────────────────────────────


def launch_claude(claude_path: str, args: list[str]) -> int:
    """启动 Claude CLI 子进程，等待退出后返回退出码。"""
    try:
        proc = subprocess.run(
            [claude_path] + args,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except KeyboardInterrupt:
        _reset_terminal(clear_screen=True)
        sys.exit(130)
    except FileNotFoundError:
        print(
            f"错误：无法执行 {claude_path}。文件可能已被删除。",
            file=sys.stderr,
        )
        sys.exit(1)

    return proc.returncode


# ── 终端工具 ──────────────────────────────────────────────────


def is_interactive(user_args: list[str]) -> bool:
    """判断本次启动是否是交互式 Claude 会话。

    非交互模式（不启动 TUI）的标志只有 --print / -p。
    --version / -v 和 --help / -h 已在 main.py 中拦截，不会走到这里。
    prompt 参数（如 brain "写个排序"）仍然是交互式会话。
    """
    non_interactive = {"--print", "-p"}
    for arg in user_args:
        if arg in non_interactive:
            return False
    return True


def _reset_terminal(clear_screen: bool = False):
    """恢复终端到可用状态。"""
    subprocess.run(["stty", "sane"], stderr=subprocess.DEVNULL)
    if clear_screen and sys.stdout.isatty():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
