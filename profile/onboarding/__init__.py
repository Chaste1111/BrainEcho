"""
Onboarding — 首次用户画像初始化流程（门面包）

外部入口（main.py import 路径不变）：
  from profile.onboarding import needs_onboarding, run_onboarding, confirm_overwrite

内部引擎：
  engine.py      树遍历引擎（渲染、收集、导航）
  questions.py   问题树数据（纯配置）
  schema.py      Memory Schema 定义
  generator.py   答案 → profile.md + profile.json
"""

from .engine import walk
from .generator import generate
from .questions import QUESTIONS

import os

# profile 文件路径（相对于项目根）
_PROFILE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE_PATH = os.path.join(_PROFILE_DIR, "profile.md")


def needs_onboarding() -> bool:
    """检查是否需要执行初始化流程。"""
    if not os.path.isfile(PROFILE_PATH):
        return True
    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except (OSError, UnicodeDecodeError):
        return True
    return not content


def run_onboarding():
    """执行交互式初始化流程。"""
    answers = walk(QUESTIONS)
    generate(answers, QUESTIONS)


def confirm_overwrite() -> bool:
    """覆盖前向用户确认。"""
    print()
    print("确认重新初始化？当前画像将被覆盖。")
    try:
        raw = input("  [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return raw in ("y", "yes")
