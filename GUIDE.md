# Brain Echo User Study V0.1

# 实验环境配置手册（新手版）

## 目录

```
1. 实验说明
2. 安装 Linux 虚拟机
3. 配置 Linux 基础环境
4. 配置外网代理
5. 安装 Claude CLI
6. 配置 DeepSeek API
7. 测试完整环境
8. 开始实验
9. 常见问题
```

---

# 1. 实验说明

## 1.1 我们正在测试什么？

本实验用于研究：

> 一个刚认识用户的 AI Agent，需要哪些信息才能更好地帮助用户。

实验过程中，你会使用一个：

```
空白 AI Agent
```

也就是说：

第一次使用时：

AI 不知道：

* 你的专业；
* 你的工作；
* 你的学习目标；
* 你的习惯；
* 你的能力水平。

你需要像平时一样使用它。

我们会观察：

> AI 在什么地方不了解你。

---

## 1.2 实验环境结构

最终环境如下：

```
你的电脑

    ↓

Linux 虚拟机

    ↓

Claude CLI

    ↓

DeepSeek API

    ↓

DeepSeek 大模型
```

其中：

### Linux

提供运行环境。

---

### Claude CLI

负责：

* 接收你的问题；
* 管理任务；
* 调用工具；
* 与你交互。

它类似 AI 助手的大脑框架。

---

### DeepSeek API

负责：

* 理解你的问题；
* 生成回答。

它是真正运行的大模型。

---

# 2. 安装 Linux 虚拟机

## 2.1 安装 VMware

如果电脑没有虚拟机软件：

下载安装：

```
VMware Workstation
```

安装过程：

一路下一步即可。

安装完成后打开。

---

## 2.2 下载 Ubuntu

推荐版本：

```
Ubuntu 22.04 LTS
```

下载文件：

```
ubuntu-22.04-desktop-amd64.iso
```

文件大小约：

4GB。

下载完成后不要打开。

---

## 2.3 创建虚拟机

打开 VMware：

点击：

```
创建新的虚拟机
```

选择：

```
典型（推荐）
```

然后：

选择：

```
稍后安装操作系统
```

原因：

避免 VMware 自动安装导致配置错误。

---

选择系统：

```
Linux

Ubuntu 64-bit
```

---

虚拟机名称：

例如：

```
BrainEcho-Test
```

---

磁盘：

推荐：

```
40GB
```

选择：

```
将虚拟磁盘存储为单个文件
```

---

完成后修改配置。

推荐：

## CPU

至少：

```
2核心
```

---

## 内存

推荐：

```
4GB
```

如果电脑配置高：

```
8GB
```

更好。

---

## 网络

选择：

```
NAT
```

不要选择：

```
仅主机模式
```

因为需要访问外网。

---

# 3. 安装 Ubuntu

启动虚拟机。

选择：

```
Install Ubuntu
```

---

安装选项：

选择：

```
正常安装
```

不要选择：

```
最小安装
```

---

安装位置：

选择：

```
清除磁盘并安装 Ubuntu
```

注意：

这里清除的是：

> 虚拟机里的空磁盘

不会影响你的真实电脑。

---

创建用户：

例如：

用户名：

```
brain
```

密码：

自己设置。

记住密码。

Linux 后面执行 sudo 命令需要。

---

安装完成：

重启。

进入 Ubuntu 桌面。

---

# 4. Linux 基础配置

打开终端：

快捷键：

```
Ctrl + Alt + T
```

你之后所有操作基本都在这里完成。

---

## 4.1 更新系统

输入：

```bash
sudo apt update
```

作用：

刷新软件列表。

执行后可能要求输入密码。

输入时：

```
不会显示任何字符
```

这是正常的。

输入完成：

按 Enter。

---

继续：

```bash
sudo apt upgrade -y
```

作用：

升级系统软件。

等待完成。

---

## 4.2 安装基础工具

执行：

```bash
sudo apt install -y curl git python3
```

安装：

* curl：下载文件
* git：代码管理
* python3：运行脚本

---

检查：

```bash
python3 --version
```

正常：

类似：

```
Python 3.10.x
```

---

# 5. 配置外网代理

## 5.1 为什么需要代理？

Claude CLI 和 DeepSeek API 都需要访问互联网。

如果你的 Linux 无法访问：

* claude.ai
* api.deepseek.com

程序无法工作。

---

## 5.2 测试网络

输入：

```bash
ping www.google.com
```

正常：

看到：

```
64 bytes from ...
```

例如：

```
64 bytes from xxx
```

说明网络正常。

停止：

按：

```
Ctrl + C
```

---

## 5.3 如果无法访问

需要配置代理。

打开：

Ubuntu设置：

```
设置
 ↓
网络
 ↓
代理
```

选择：

```
手动
```

填写你的代理：

例如：

```
HTTP代理:
127.0.0.1

端口:
7890
```

（根据自己的代理软件修改）

---

测试：

```bash
curl www.google.com
```

如果返回网页内容：

成功。

---

# 6. 安装 Claude CLI

## 6.1 安装

执行：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

等待完成。

---

## 6.2 检查安装

输入：

```bash
claude --version
```

成功：

类似：

```
claude 1.x.x
```

---

如果提示：

```
command not found
```

执行：

```bash
source ~/.bashrc
```

再测试。

---

# 7. 配置 DeepSeek API

## 7.1 获取 API Key

打开 DeepSeek 开放平台。

注册账号。

创建 API Key。

获得：

类似：

```
sk-xxxxxxxxxxxx
```

注意：

这个相当于密码。

不要发给别人。

---

# 7.2 设置环境变量

打开：

```bash
nano ~/.bashrc
```

移动到文件最后。

添加：

```bash
export DEEPSEEK_API_KEY="你的API_KEY"
```

例如：

```bash
export DEEPSEEK_API_KEY="sk-xxxx"
```

---

保存：

键盘：

```
Ctrl + O
```

回车。

退出：

```
Ctrl + X
```

---

刷新：

```bash
source ~/.bashrc
```

---

检查：

```bash
echo $DEEPSEEK_API_KEY
```

如果显示：

```
sk-xxxx
```

成功。

---

# 8. 测试完整环境

## 8.1 测试 Claude

运行：

```bash
claude
```

进入交互模式。

输入：

```
你好
```

如果 AI 回复：

说明 Agent 正常。

---

退出：

```
Ctrl + C
```

---

## 8.2 创建实验目录

执行：

```bash
mkdir ~/brain-study
```

进入：

```bash
cd ~/brain-study
```

以后实验文件放这里。

---

# 9. 实验规则

## 第一阶段：空白 Agent

时间：

```
7天
```

要求：

不要主动告诉 AI：

* 你的个人介绍；
* 简历；
* 学习经历；
* 长期规划。

让 AI 自己通过交流理解你。

---

## 使用方式

正常使用：

例如：

* 写代码；
* 学习；
* 查资料；
* 做项目；
* 写文章。

---

## 记录内容

不要记录全部聊天。

只记录：

> “如果 AI 早点知道某个信息，回答会明显更好。”

模板：

```
时间：

我让AI做什么：

AI哪里理解错：

如果提前知道什么：
```

---

# 10. 遇到问题怎么办？

不要直接修改。

记录：

```
执行步骤：

执行命令：

错误信息：

截图：
```

发送给实验负责人。

---

# 配置完成标准

完成后应该满足：

✅ Ubuntu 可以联网

✅

```bash
python3 --version
```

正常

✅

```bash
claude --version
```

正常

✅

```bash
echo $DEEPSEEK_API_KEY
```

正常

✅

```bash
claude
```

可以聊天

完成后即可开始 Brain Echo 用户研究。
