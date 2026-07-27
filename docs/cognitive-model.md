# Cognitive Model — Brain Echo 认知模型设计

> 版本：v0.4-draft
> 日期：2026-07-27
> 状态：设计文档，待实现

---

## 一、核心哲学

### 1.1 Brain Echo 不是什么

Brain Echo 不是：

- ❌ 聊天记录存储器
- ❌ 用户属性数据库
- ❌ 知识库 / RAG 系统
- ❌ 向量数据库
- ❌ 多 Agent 通信总线

### 1.2 Brain Echo 是什么

Brain Echo 是：

> **一个将用户行为转化为 Agent 协作策略的系统。**

关键转变：

```
传统 Memory：   "我记得你说过什么"
                    ↓
Brain Echo：    "我知道根据你的特点，我应该怎么做"
```

### 1.3 核心原则

**信息本身没有价值，能改变 Agent 行为的信息才有价值。**

一条用户信息是否值得保存，唯一标准是：

> 保存它之后，Agent 的决策会不会变得更好？

如果不会，就不存。

---

## 二、什么是 Memory？

### 2.1 Brain Echo 的定义

```
Memory = 可以改变 Agent 决策的信息
```

不是用户说过的话，而是从用户行为中抽象出的、能指导 Agent 协作策略的认知模型。

### 2.2 Memory 的三个特征

| 特征 | 说明 |
|------|------|
| **可决策** | 能直接影响 Agent 的某个行为选择 |
| **可验证** | 有足够的证据支持，不是单次猜测 |
| **可操作** | 能转化为具体的 Agent 指令（Policy） |

### 2.3 不是 Memory 的信息

| 信息类型 | 排除原因 |
|----------|---------|
| 具体代码片段 | 太临时，下次对话不再有用 |
| 今日情绪状态 | 变化太快，无法形成稳定策略 |
| 原始对话文本 | 没有提炼，无法直接指导 Agent 行为 |
| 一次性任务详情 | 不会重复出现，不值得记录 |
| 他人信息 | 与当前用户协作无关 |

---

## 三、认知模型的五层结构

```
┌───────────────────────────────────────────────┐
│              Identity（身份层）                │
│  用户是谁 —— 背景、领域、长期目标            │
│  价值：低，仅作参考                          │
│  来源：初始化问答                            │
│  更新频率：几乎不变                          │
├───────────────────────────────────────────────┤
│              State（状态层）                  │
│  用户在哪 —— 当前项目、时间、精力           │
│  价值：高，改变任务规模和节奏                │
│  来源：初始化 + 每次会话快速探测             │
│  更新频率：每次会话                          │
├───────────────────────────────────────────────┤
│              Patterns（模式层）               │
│  用户习惯怎么做 —— 学习方式、决策偏好、      │
│  沟通模式、工作节奏                          │
│  价值：高，决定交互方式                      │
│  来源：初始化 + 对话中持续抽取               │
│  更新频率：月度级别（稳定后几乎不变）        │
├───────────────────────────────────────────────┤
│              Policies（策略层）               │
│  Agent 应该怎么做 —— 触发条件 + 行动指令    │
│  价值：最高，直接改变 Agent 行为            │
│  来源：由 Patterns 推导而来                  │
│  更新频率：随 Patterns 更新                  │
├───────────────────────────────────────────────┤
│              Evidence（证据层）               │
│  为什么这么判断 —— 原始依据和置信度         │
│  价值：用于审计、回滚、用户确认             │
│  来源：对话记录                              │
│  更新频率：追加写入，不覆盖                 │
└───────────────────────────────────────────────┘
```

### 3.1 五层的关系

```
Identity + State
       │
       ▼
  用户当前场景
       │
       ▼
Patterns（从行为中观察到的稳定倾向）
       │
       ▼
Policies（转化为 Agent 的执行指令）
       │
       ▼
Agent 行为改变
       │
       ▼
Evidence（记录推导过程，支持回溯）
```

### 3.2 一个完整的例子

用户说："我不喜欢直接复制代码，我想知道为什么这么设计。"

```
提取 → Observation：
  "用户要求理解设计原因，而不是直接获取代码"

归纳 → Pattern：
  learning_style = principle_first
  confidence = 0.85
  evidence = ["2026-07-16: 要求解释设计原因"]

推导 → Policy：
  trigger: 用户询问技术问题
  action:
    1. 先解释该技术/方案存在的背景（为什么需要它）
    2. 再解释设计原理（为什么这么设计）
    3. 最后提供代码或方案

执行 → Agent 行为改变：
  "我们先看看为什么会出现 Reactor 模式..."
  而不是：
  "这是 Reactor 的代码：..."

记录 → Evidence：
  {
    "date": "2026-07-16",
    "source": "用户主动表达",
    "pattern": "learning_style",
    "value": "principle_first",
    "confidence": 0.85
  }
```

---

## 四、Patterns 的定义与管理

### 4.1 什么是 Pattern

Pattern 不是用户属性，而是**从多次行为中抽象出的稳定倾向**。

一条信息成为 Pattern 需要满足：

1. **观察到至少 2 次以上**（单次不构成模式）
2. **跨场景一致**（不同话题下表现相同）
3. **可推导出 Policy**（能转化为 Agent 指令）

### 4.2 Pattern 的字段定义

```json
{
  "name": "learning_style",
  "value": "principle_first",
  "confidence": 0.85,
  "first_observed": "2026-07-10",
  "last_observed": "2026-07-27",
  "observation_count": 5,
  "evidence": [
    "2026-07-10: 要求解释设计动机",
    "2026-07-16: 不喜欢复制代码",
    "2026-07-27: 主动问为什么这样设计"
  ],
  "derives_policy": "teaching_approach"
}
```

### 4.3 置信度（Confidence）

| 置信度范围 | 含义 | 行为 |
|-----------|------|------|
| 0.0 - 0.3 | 猜测 | 不写入 profile，仅记录 observation |
| 0.3 - 0.6 | 初步观察 | 写入 profile，标注 low confidence |
| 0.6 - 0.9 | 基本确认 | 写入 profile，生成对应 Policy |
| 0.9 - 1.0 | 高度确信 | 完全确定，无需用户确认 |

### 4.4 第一个 Pattern 类型：learning_style

V0.4 只实现这一个 Pattern 的完整闭环。

**可选的 values：**

| value | 特征 | 对应 Policy |
|-------|------|-------------|
| principle_first | 先理解原理再动手 | teaching_approach = explain_before_do |
| direct_answer | 直接要答案 | teaching_approach = direct_solution |
| compare_options | 喜欢对比方案 | teaching_approach = multi_option |
| hands_on | 边做边学 | teaching_approach = example_driven |

---

## 五、Policies 的定义

### 5.1 什么是 Policy

Policy 是**能直接改变 Agent 行为的指令**。

它由 Pattern 推导而来，格式为：**当 X 发生时，执行 Y**。

### 5.2 Policy 的字段定义

```json
{
  "name": "teaching_approach",
  "trigger": "用户提出技术问题 / 要求学习新知识",
  "instruction": "先解释该技术存在的背景和设计动机，再讲原理，最后给代码",
  "derived_from": "learning_style: principle_first",
  "confidence": 0.85,
  "effective": true
}
```

### 5.3 Policy 的注入方式

Policy 不单独存储为一个文件，而是**注入到每次对话的 system prompt 中**：

```
## 协作策略

当用户询问技术问题时：
  1. 先解释为什么需要这个技术（背景和动机）
  2. 再解释设计原理（为什么这么设计）
  3. 最后提供具体方案或代码

当用户提出自己的方案时：
  1. 先肯定尝试
  2. 再分析潜在问题
  3. 给改进建议
```

这是 Brain Echo 和 Claude Memory 的核心区别：
- Claude Memory 告诉 Agent **"用户是谁"**
- Brain Echo 告诉 Agent **"你应该怎么做"**

---

## 六、Evidence 的管理

### 6.1 什么应该进入 Evidence

每条进入 Evidence 的记录必须包含：

```json
{
  "date": "ISO 日期",
  "source": "用户表达 / 行为观察 / 初始化回答",
  "pattern": "对应的 pattern 名称",
  "value": "对应的 pattern 值",
  "confidence": 0.0-1.0,
  "raw_text": "用户原话或行为描述（可选）"
}
```

### 6.2 什么不应该进入 Evidence

- 完整的聊天记录（只存提炼后的证据片段）
- 代码内容（只存"用户擅长什么"不存具体代码）
- 情绪波动（只存"应对模式"不存"今天心情"）

---

## 七、处理流程（Pipeline）

```
用户输入
    │
    ▼
┌──────────────┐
│  Agent 响应   │  （Claude Codex 等正常对话）
└──────────────┘
    │
    ▼
┌──────────────┐
│  Logger      │  保存对话片段到 memory/observations/
└──────────────┘
    │
    ▼
┌──────────────┐
│  Extractor   │  分析对话，提取 Pattern 候选
└──────────────┘
    │
    ▼
┌──────────────┐
│  Evaluator   │  计算置信度，判断是否写入
└──────────────┘
    │
    ▼
┌──────────────┐
│  Confirmer   │  低置信度 → 询问用户确认
│              │  高置信度 → 直接写入
└──────────────┘
    │
    ▼
┌──────────────┐
│  Store       │  写入 profile.json
└──────────────┘
    │
    ▼
┌──────────────┐
│  Generator   │  重新生成 profile.md
└──────────────┘
    │
    ▼
下次启动 → 新 Policy 生效
```

---

## 八、V0.4 范围

### 8.1 做

| 模块 | 文件 | 说明 |
|------|------|------|
| Schema 重构 | `schema.py` | 五层结构，含 confidence/evidence |
| 问题内容更新 | `questions.py` | 从"收集标签"改为"收集场景偏向" |
| Generator 更新 | `generator.py` | 输出新结构，policies 写入 profile.md |
| Context 注入升级 | `context.py` | 包装头改为 Policy 指令风格 |
| Memory Logger | `memory/logger.py` | 保存对话片段 |
| Memory Extractor | `memory/extractor.py` | 提取 learning_style pattern |
| Memory Evaluator | `memory/evaluator.py` | 计算置信度 |
| Memory Confirmer | `memory/confirmer.py` | 用户确认交互 |
| Memory Store | `memory/store.py` | 写入 profile |

### 8.2 不做

| 技术 | 原因 |
|------|------|
| 向量数据库 | V0.4 的数据规模不需要 |
| RAG | Brain Echo 不是知识库 |
| 多 Agent 通信 | V1.0 阶段 |
| 自动修改所有 Memory | 先验证单个 Pattern 闭环 |
| 知识图谱 | 过度设计 |

### 8.3 验证标准

完成 V0.4 后运行：

```
实验组：brain "给我解释 Reactor 模式"
对照组：claude "给我解释 Reactor 模式"
```

差距：

- 对照组：直接给定义和代码
- 实验组：先解释为什么需要 Reactor，再讲设计，再给代码

如果你明显感觉实验组更贴近你的学习方式，闭环验证通过。

---

## 九、与 V0.3 的兼容性

| 组件 | 是否兼容 | 说明 |
|------|---------|------|
| `engine.py` | ✅ 完全兼容 | 问题内容和 schema 解耦，引擎不动 |
| `adapter/` | ✅ 完全兼容 | 不感知上层结构 |
| `main.py` | ✅ 完全兼容 | 只调 onboarding + context |
| `profile.json` | ⚠️ 格式变化 | 新字段写入，旧字段逐步废弃 |
| `context.py` | ✅ 接口兼容 | 内部实现升级，对外接口不变 |
