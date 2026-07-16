#!/usr/bin/env bash
# Brain Echo — 一键安装脚本
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/Chaste1111/BrainEcho/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/Projects/BrainEcho"
CLAUDE_LINK="$HOME/.local/bin/brain"
REPO_URL="https://github.com/Chaste1111/BrainEcho.git"

echo "🧠 Brain Echo 安装中..."
echo ""

# 1. 检查必要工具
for cmd in git python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "错误：需要 $cmd，请先安装。"
        exit 1
    fi
done

# 2. 检查 / 安装 Claude CLI
if ! command -v claude &>/dev/null; then
    if command -v npm &>/dev/null; then
        echo "→ 未检测到 Claude CLI，正在安装..."
        npm install -g @anthropic-ai/claude-code
    else
        echo "错误：需要 Claude CLI，请先安装 npm 或手动安装。"
        exit 1
    fi
fi

# 3. 下载 / 更新 Brain Echo 代码
if [ -d "$INSTALL_DIR" ]; then
    echo "→ BrainEcho 已存在，更新中..."
    cd "$INSTALL_DIR" && git pull
else
    echo "→ 下载 BrainEcho..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 4. 确保 ~/.local/bin 存在
mkdir -p "$HOME/.local/bin"

# 5. 创建 brain 命令软链接
echo "→ 创建 brain 命令..."
ln -sf "$INSTALL_DIR/main.py" "$CLAUDE_LINK"
chmod +x "$INSTALL_DIR/main.py"

# 6. 确保 ~/.local/bin 在 PATH 中
case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *)
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
        echo "→ 已将 ~/.local/bin 加入 PATH"
        echo "  请执行: source ~/.bashrc"
        ;;
esac

echo ""
echo "✅ Brain Echo 安装完成！"
echo ""
echo "首次使用请运行: brain"
echo "将进入初始化流程，回答几个问题后即可使用。"
