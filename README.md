# Brain Echo

Agent 上层个人智能层入口。

在 Agent（Claude 等）之上增加一层"用户长期理解层"：

```
用户
 ↓
brain
 ↓
用户画像注入
 ↓
Claude
```

## 快速安装

```bash
curl -fsSL https://raw.githubusercontent.com/Chaste1111/BrainEcho/main/install.sh | bash
```

首次运行 `brain` 将进入初始化流程，回答几个问题后即可开始使用。

## 命令

| 命令 | 作用 |
|------|------|
| `brain` | 启动交互式 Claude（自动初始化和注入）|
| `brain --version / -v` | 显示版本号 |
| `brain --help / -h` | 显示帮助 |
| `brain --onboarding` | 强制重新初始化 |

其余参数原样透传 Claude CLI。

## 项目结构

```
BrainEcho/
├── main.py                   ← 入口分发
├── adapter/                  ← Claude CLI 启动封装
├── context/                  ← 上下文构建（profile → 注入 Claude）
├── profile/
│   ├── onboarding/           ← 初始化引擎
│   │   ├── engine.py         ← 树遍历引擎
│   │   ├── questions.py      ← 问题树数据
│   │   ├── schema.py         ← 用户模型定义
│   │   └── generator.py      ← 答案 → profile 文件
│   ├── profile.md            ← 用户画像（给 LLM 读）
│   ├── profile.json          ← 用户画像（程序处理用）
│   └── changes.json          ← 变化记录（V0.4+）
├── install.sh                ← 一键安装脚本
└── README.md
```

## 路线图

- **V0.1** — CLI 入口层（brain → Claude）
- **V0.2** — Context 层（用户画像注入 Claude）
- **V0.3** — Onboarding Engine（首次初始化流程 + Memory Schema）
- **V0.4** — 动态记忆层（计划中）

## 原则

1. 不重复造 Claude Code 的轮子
2. 不先做 UI
3. 不先做复杂 Memory
4. 先证明入口层是否可行
