#!/usr/bin/env bash
# Brain Echo — 一键安装脚本
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/Chaste1111/BrainEcho/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/Projects/BrainEcho"
CLAUDE_PATH="$HOME/.local/bin/brain"
REPO_URL="https://github.com/Chaste1111/BrainEcho.git"

echo "🧠 Brain Echo 安装中..."
echo ""

# 1. 检查 claude 是否已安装
if ! command -v claude &>/dev/null; then
    echo "→ 未检测到 Claude CLI，正在安装..."
    npm install -g @anthropic-ai/claude-code
fi

# 2. 检查 Python 3
if ! command -v python3 &>/dev/null; then
    echo "错误：需要 Python 3，请先安装。"
    exit 1
fi

# 3. 下载 Brain Echo 代码
if [ -d "$INSTALL_DIR" ]; then
    echo "→ BrainEcho 已存在，更新中..."
    cd "$INSTALL_DIR" && git pull
else
    echo "→ 下载 BrainEcho..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 4. 创建 brain 命令软链接
echo "→ 创建 brain 命令..."
ln -sf "$INSTALL_DIR/main.py" "$CLAUDE_PATH"
chmod +x "$INSTALL_DIR/main.py"

# 5. 确保 ~/.local/bin 在 PATH 中
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    echo "→ 已将 ~/.local/bin 加入 PATH（请重新打开终端或执行 source ~/.bashrc）"
fi

echo ""
echo "✅ Brain Echo 安装完成！"
echo ""
echo "首次使用请运行: brain"
echo "将进入初始化流程，回答几个问题后即可使用。"
