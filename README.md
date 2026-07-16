# Brain Echo

Agent 上层个人智能层入口。

## 目标

在 AI Agent（Claude / DeepSeek 等）之上增加一层"用户长期理解层"：

```
用户
 ↓
Brain Echo（入口层）
 ↓
Claude Agent / 其他Agent
 ↓
大模型
 ↓
执行任务
```

## V0.1

创建一个 `brain` 命令，启动 Claude CLI 并承载未来扩展。

### 验收标准

```bash
brain
```

输出：

```
Brain Echo starting...

Loading config...

Starting Claude...

>
```

然后进入正常 Claude CLI 交互，`/resume`、`/exit` 等命令全部保留。

## 项目结构

```
BrainEcho/
├── main.py        ← 入口
├── config/        ← 配置模块
├── memory/        ← 记忆模块
└── README.md
```

## 安装

```bash
# 1. 创建软链接
sudo ln -sf ~/Projects/BrainEcho/main.py /usr/local/bin/brain

# 2. 验证
brain
```

## 路线图

- **V0.1** — Brain Echo 入口层，启动 Claude CLI（当前）
- **V0.2** — 配置加载器
- **V0.3** — 用户记忆管理层
- **V0.4** — 上下文构建器
- **V0.5** — 多 Agent 路由层

## 原则

1. 不重复造 Claude Code 的轮子
2. 不先做 UI
3. 不先做复杂 Memory
4. 先证明入口层是否可行
