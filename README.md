<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Tests-52%20Passed-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Dependencies-Zero-success.svg" alt="Zero Dependencies">
</p>

<p align="center">
  <strong>AgentForge-CLI</strong> &mdash; AI Agent 工程化脚手架与合规检查引擎
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> &bull;
  <a href="#繁體中文">繁體中文</a> &bull;
  <a href="#english">English</a>
</p>

---

<a id="简体中文"></a>

# 🎉 项目介绍

**AgentForge-CLI** 是一款专为 AI Agent 开发者打造的命令行工程化工具。它不仅仅是一个脚手架生成器，更是一套完整的 Agent 项目工程化解决方案——从项目初始化、代码规范检查到健康诊断，覆盖 Agent 项目全生命周期。

## 解决的痛点

在 AI Agent 快速发展的今天，开发者面临着诸多工程化挑战：

- **项目结构混乱**：每个开发者都有自己的项目组织方式，缺乏统一标准，团队协作成本高
- **最佳实践难以落地**：12-Factor Agent 等优秀方法论停留在文档层面，缺乏自动化工具支撑
- **代码质量参差不齐**：缺少针对 Agent 项目的 Lint 工具，安全性、可维护性难以保障
- **从零开始成本高**：每次新建 Agent 项目都要重复搭建基础结构，浪费时间

## 差异化优势

与 [12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents) 方法论（仅提供文档规范）不同，AgentForge-CLI 将理念转化为**可执行的工具链**：

| 维度 | 12-Factor Agents 文档 | AgentForge-CLI |
|------|----------------------|----------------|
| 形式 | 纯文档规范 | 可执行的 CLI 工具 |
| 项目初始化 | 手动参照 | 一键脚手架生成 |
| 合规检查 | 人工审查 | 自动化 Lint 检测 |
| 健康诊断 | 无 | 6 大维度自动诊断 |
| 模板支持 | 无 | 3 套内置模板 |

## 灵感来源

本项目灵感来源于经典软件工程方法论 **[The Twelve-Factor App](https://12factor.net/)** 以及 **[12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents)** 的 Agent 领域扩展。我们坚信：好的工程实践不应该只是文档，而应该是开发者日常工作中触手可及的工具。

---

# ✨ 核心特性

- 🔧 **`agentforge init`** — 从模板一键生成标准化 Agent 项目，支持 3 种内置模板
- 🔍 **`agentforge lint`** — 基于 12-Factor Agent 方法论的自动化合规检查，输出 0-100 评分
- 🩺 **`agentforge doctor`** — 6 大维度健康诊断，快速定位项目隐患
- 📋 **`agentforge template`** — 浏览和管理内置项目模板
- 📏 **12-Factor 合规检查** — 覆盖上下文隔离、工具接口、控制流、状态管理等 12 个核心因子
- 📦 **3 套内置模板** — minimal（轻量）、full（完整）、mcp（MCP 协议兼容）
- 🚫 **零外部依赖** — 完全基于 Python 标准库，安装即用，无任何第三方包
- 🎨 **彩色终端输出** — 美观的 ANSI 彩色表格、状态标识和进度指示器

---

# 🚀 快速开始

## 环境要求

- **Python 3.8+**（支持 3.8、3.9、3.10、3.11、3.12）
- pip 包管理器
- 终端支持 ANSI 颜色（可选，自动检测）

## 安装

```bash
# 通过 pip 安装（推荐）
pip install agentforge-cli

# 验证安装
agentforge --version
```

## 三步上手

```bash
# 1️⃣ 创建一个新的 Agent 项目
agentforge init --name my-agent --template full

# 2️⃣ 进入项目目录并安装依赖
cd my-agent && pip install -r requirements.txt

# 3️⃣ 检查项目合规性
agentforge lint
```

## 更多命令

```bash
# 查看所有可用命令
agentforge --help

# 运行健康诊断
agentforge doctor

# 以 JSON 格式输出合规报告
agentforge lint --format json

# 查看可用模板
agentforge template --list
```

---

# 📖 详细使用指南

## 4.1 `agentforge init` — 项目脚手架

从内置模板快速生成标准化的 AI Agent 项目结构。

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--name` | ✅ | — | 项目名称，用于目录和包命名 |
| `--template` | ❌ | `minimal` | 模板类型：`minimal`、`full`、`mcp` |
| `--output-dir` | ❌ | `.`（当前目录） | 项目创建的目标目录 |
| `--description` | ❌ | `An AI agent built with AgentForge` | 项目描述，写入 README 和元数据 |

### 使用示例

```bash
# 使用 full 模板创建项目
agentforge init --name my-agent --template full

# 使用 mcp 模板创建项目到指定目录
agentforge init --name mcp-server --template mcp --output-dir ./projects

# 创建项目并添加自定义描述
agentforge init --name chatbot --template minimal --description "A customer service chatbot"
```

### 模板对比

| 特性 | minimal | full | mcp |
|------|---------|------|-----|
| 定位 | 轻量入门 | 完整生产级 | MCP 协议服务 |
| 核心文件 | agent.py, config.py, tools.py | agent.py, config.py, tools.py, memory.py, prompts.py | server.py, tools.py, config.py |
| 记忆管理 | ❌ | ✅ | ❌ |
| 提示词模板 | ❌ | ✅ | ❌ |
| 单元测试 | ❌ | ✅ | ❌ |
| .env 配置 | ✅ | ✅ | ✅ |
| 适用场景 | 简单聊天机器人、单任务 Agent、原型验证 | 生产级 Agent、复杂工作流、多工具 Agent | MCP 工具服务器、IDE 集成、标准化工具暴露 |

---

## 4.2 `agentforge lint` — 合规检查

基于 12-Factor Agent 方法论对项目进行自动化合规检查，输出 0-100 的综合评分及详细改进建议。

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--path` | ❌ | `.`（当前目录） | 待检查的项目目录路径 |
| `--format` | ❌ | `table` | 输出格式：`table`（表格）或 `json` |
| `--rules` | ❌ | 全部规则 | 指定检查的规则 ID，如 `F01 F02`（空格分隔） |

### 使用示例

```bash
# 检查当前目录
agentforge lint

# 检查指定目录
agentforge lint --path ./my-agent

# 仅检查安全和测试相关规则
agentforge lint --rules F07 F08

# 输出 JSON 格式报告（便于 CI/CD 集成）
agentforge lint --format json
```

### 12-Factor 规则说明

| 规则 ID | 因子名称 | 权重 | 说明 |
|---------|---------|------|------|
| F01 | 上下文隔离 (Context Isolation) | 2 | Agent 是否分离了系统/用户/工具上下文 |
| F02 | 工具接口 (Tool Interface) | 2 | 工具是否有清晰的输入/输出 Schema |
| F03 | 控制流 (Control Flow) | 2 | Agent 是否有显式的控制流逻辑和循环限制 |
| F04 | 状态管理 (State Management) | 2 | Agent 状态是否可持久化（非仅内存） |
| F05 | 错误处理 (Error Handling) | 2 | 是否有异常处理、重试逻辑和降级方案 |
| F06 | 可观测性 (Observability) | 1 | 是否配置了日志和链路追踪 |
| F07 | 安全性 (Security) | 3 | 是否有输入验证、无硬编码密钥 |
| F08 | 测试 (Testing) | 2 | 是否有单元测试覆盖 |
| F09 | 配置管理 (Configuration) | 2 | 是否使用环境变量管理配置 |
| F10 | 文档 (Documentation) | 1 | 是否有 README 和代码文档 |
| F11 | 依赖管理 (Dependency Management) | 1 | 是否有 requirements.txt 或 pyproject.toml |
| F12 | 部署 (Deployment) | 1 | 是否有 Docker 支持或部署文档 |

### 示例输出

```
  12-Factor Agent Compliance Report
  Project: /home/user/my-agent

  Overall Score: 75/100
  Checks: 18 passed, 6 failed, 24 total

  ID    Factor                  Weight  Status   Details
  ───   ──────────────────────  ──────  ───────  ──────────────────────
  F01   Context Isolation       2       PASS     3/3
  F02   Tool Interface          2       PARTIAL  2/3 - Tools use structured input/output types
  F03   Control Flow            2       PASS     2/2
  F07   Security                3       FAIL     1/3 - .env.example missing
  ...

  Suggestions:
  [!] [F07] Create a .env.example file documenting required environment variables.
  [!] [F08] Create a tests/ directory with unit tests.
```

---

## 4.3 `agentforge doctor` — 健康诊断

对 AI Agent 项目进行全面的健康检查，涵盖 6 大诊断类别，帮助开发者快速发现潜在问题。

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--path` | ❌ | `.`（当前目录） | 待诊断的项目目录路径 |
| `--verbose` | ❌ | `false` | 显示详细诊断信息 |

### 6 大诊断类别

| 类别 | 检查内容 |
|------|---------|
| **Environment（环境）** | Python 版本兼容性检测 |
| **Project Structure（项目结构）** | 必需文件检查（README、requirements.txt、.env.example、.gitignore 等） |
| **Security（安全）** | .env 文件保护、硬编码密钥检测 |
| **Dependencies（依赖）** | 依赖列表完整性、版本锁定检查 |
| **Code Quality（代码质量）** | 类型注解使用率、文档字符串覆盖率 |
| **Agent（Agent 专项）** | LLM 框架检测、工具定义、提示词管理 |

### 使用示例

```bash
# 运行基础诊断
agentforge doctor

# 运行详细诊断
agentforge doctor --verbose

# 诊断指定项目
agentforge doctor --path ./my-agent
```

### 示例输出

```
  ============================================================
    AgentForge Doctor - Health Diagnostics
  ============================================================

  Summary: 8 passed, 2 warnings, 0 failures

  Environment
  [OK]   Python 3.11.5
  [OK]   Compatible with Python >= 3.8

  Project Structure
  [OK]   README.md found
  [OK]   requirements.txt found
  [WARN] .env.example missing
  [OK]   Agent module found

  Security
  [OK]   No hardcoded secrets detected

  Dependencies
  [OK]   5 dependencies listed
  [WARN] 3/5 dependencies have pinned versions

  Code Quality
  [OK]   8 Python file(s) found
  [OK]   6/8 files use type hints
  [OK]   7/8 files have docstrings

  Agent
  [OK]   Using: OpenAI, LangChain
  [OK]   Tool definitions found
  [OK]   Prompt management found
```

---

## 4.4 `agentforge template` — 模板管理

浏览和查看 AgentForge-CLI 内置的项目模板详细信息。

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--list` | ❌ | 列出所有可用模板 |
| `--info <NAME>` | ❌ | 查看指定模板的详细信息 |

### 使用示例

```bash
# 列出所有模板
agentforge template --list

# 查看 full 模板详情
agentforge template --info full

# 查看 mcp 模板详情
agentforge template --info mcp
```

### 内置模板一览

| 模板 | 名称 | 适用场景 |
|------|------|---------|
| `minimal` | 轻量 Agent | 简单聊天机器人、单任务 Agent、快速原型 |
| `full` | 完整 Agent | 生产级 Agent、复杂工作流、多工具协作 |
| `mcp` | MCP 兼容服务 | MCP 工具服务器、IDE 集成、标准化工具暴露 |

---

# 💡 设计思路与迭代规划

## 设计原则

### 🚫 零依赖 (Zero Dependencies)

AgentForge-CLI 完全基于 Python 标准库构建，不依赖任何第三方包。这意味着：

- 安装速度极快，无需等待依赖解析
- 无版本冲突风险
- 可在受限网络环境下使用
- 减少供应链安全风险

### 📐 约定优于配置 (Convention over Configuration)

内置模板和检查规则遵循业界最佳实践，开发者无需从零开始思考项目结构。同时保留足够的灵活性——模板生成的代码完全可定制。

### 🧑‍💻 开发者体验优先 (Developer Experience First)

- 彩色终端输出，信息层次清晰
- 友好的错误提示和改进建议
- 一条命令完成复杂操作
- 详细的帮助文档和示例

## 为什么是 12-Factor for Agents？

传统的 12-Factor App 方法论为 Web 应用提供了优秀的工程化指导。然而，AI Agent 有着独特的工程挑战：

- **上下文管理**：Agent 需要处理系统提示、用户输入、工具返回等多种上下文
- **工具接口**：Agent 的能力通过工具暴露，需要严格的 Schema 定义
- **控制流**：Agent 的推理-行动循环需要循环限制和安全保障
- **状态持久化**：Agent 的记忆和状态需要可靠的外部存储

AgentForge-CLI 将这些 Agent 特有的工程需求转化为可自动检查的规则，帮助团队建立统一的工程标准。

## 迭代规划

- [ ] **更多模板**：支持 LangGraph、CrewAI、AutoGen 等框架模板
- [ ] **CI/CD 集成**：提供 GitHub Actions / GitLab CI 预配置
- [ ] **VS Code 扩展**：在编辑器内直接使用 AgentForge 功能
- [ ] **自定义规则**：支持用户编写和加载自定义检查规则
- [ ] **模板市场**：社区模板共享和安装机制
- [ ] **项目升级**：检测模板版本更新并辅助迁移

---

# 📦 安装与部署

## pip 安装（推荐）

```bash
pip install agentforge-cli
```

## pipx 安装（隔离环境，推荐用于工具类 CLI）

```bash
# 安装 pipx（如尚未安装）
pip install pipx

# 通过 pipx 安装 agentforge-cli
pipx install agentforge-cli
```

## 从源码安装

```bash
# 克隆仓库
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# 安装（开发模式）
pip install -e .

# 或安装为普通包
pip install .
```

## Docker（可选）

```bash
# 拉取镜像
docker pull agentforge/cli:latest

# 运行合规检查
docker run --rm -v $(pwd):/workspace agentforge/cli:latest lint --path /workspace

# 创建新项目
docker run --rm -v $(pwd):/workspace agentforge/cli:latest init --name my-agent --template full --output-dir /workspace
```

---

# 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！无论是提交 Bug 报告、改进文档还是贡献代码。

## 提交 Pull Request

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 编写代码并确保通过所有测试：`pytest tests/`
4. 提交变更：`git commit -m "feat: add your feature description"`
5. 推送分支：`git push origin feature/your-feature-name`
6. 提交 **Pull Request**

## 提交 Issue

- **Bug 报告**：请包含复现步骤、预期行为、实际行为以及运行环境信息
- **功能建议**：请描述使用场景和期望的行为
- **问题咨询**：请先查阅文档和已有 Issue

## 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=agentforge --cov-report=term-missing
```

---

# 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<a id="繁體中文"></a>

# 🎉 項目介紹

**AgentForge-CLI** 是一款專為 AI Agent 開發者打造的命令列工程化工具。它不僅僅是一個腳手架生成器，更是一套完整的 Agent 專案工程化解決方案——從專案初始化、程式碼規範檢查到健康診斷，涵蓋 Agent 專案全生命週期。

## 解決的痛點

在 AI Agent 快速發展的今天，開發者面臨著諸多工程化挑戰：

- **專案結構混亂**：每個開發者都有自己的專案組織方式，缺乏統一標準，團隊協作成本高
- **最佳實踐難以落地**：12-Factor Agent 等優秀方法論停留在文件層面，缺乏自動化工具支撐
- **程式碼品質參差不齊**：缺少針對 Agent 專案的 Lint 工具，安全性、可維護性難以保障
- **從零開始成本高**：每次新建 Agent 專案都要重複搭建基礎結構，浪費時間

## 差異化優勢

與 [12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents) 方法論（僅提供文件規範）不同，AgentForge-CLI 將理念轉化為**可執行的工具鏈**：

| 維度 | 12-Factor Agents 文件 | AgentForge-CLI |
|------|----------------------|----------------|
| 形式 | 純文件規範 | 可執行的 CLI 工具 |
| 專案初始化 | 手動參照 | 一鍵腳手架生成 |
| 合規檢查 | 人工審查 | 自動化 Lint 偵測 |
| 健康診斷 | 無 | 6 大維度自動診斷 |
| 範本支援 | 無 | 3 套內建範本 |

## 靈感來源

本專案靈感來源於經典軟體工程方法論 **[The Twelve-Factor App](https://12factor.net/)** 以及 **[12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents)** 的 Agent 領域擴展。我們堅信：好的工程實踐不應該只是文件，而應該是開發者日常工作中觸手可及的工具。

---

# ✨ 核心特性

- 🔧 **`agentforge init`** — 從範本一鍵生成標準化 Agent 專案，支援 3 種內建範本
- 🔍 **`agentforge lint`** — 基於 12-Factor Agent 方法論的自動化合規檢查，輸出 0-100 評分
- 🩺 **`agentforge doctor`** — 6 大維度健康診斷，快速定位專案隱患
- 📋 **`agentforge template`** — 瀏覽和管理內建專案範本
- 📏 **12-Factor 合規檢查** — 涵蓋上下文隔離、工具介面、控制流程、狀態管理等 12 個核心因子
- 📦 **3 套內建範本** — minimal（輕量）、full（完整）、mcp（MCP 協議相容）
- 🚫 **零外部依賴** — 完全基於 Python 標準函式庫，安裝即用，無任何第三方套件
- 🎨 **彩色終端輸出** — 美觀的 ANSI 彩色表格、狀態標識和進度指示器

---

# 🚀 快速開始

## 環境需求

- **Python 3.8+**（支援 3.8、3.9、3.10、3.11、3.12）
- pip 套件管理器
- 終端支援 ANSI 顏色（可選，自動偵測）

## 安裝

```bash
# 透過 pip 安裝（推薦）
pip install agentforge-cli

# 驗證安裝
agentforge --version
```

## 三步上手

```bash
# 1️⃣ 建立一個新的 Agent 專案
agentforge init --name my-agent --template full

# 2️⃣ 進入專案目錄並安裝依賴
cd my-agent && pip install -r requirements.txt

# 3️⃣ 檢查專案合規性
agentforge lint
```

## 更多指令

```bash
# 查看所有可用指令
agentforge --help

# 執行健康診斷
agentforge doctor

# 以 JSON 格式輸出合規報告
agentforge lint --format json

# 查看可用範本
agentforge template --list
```

---

# 📖 詳細使用指南

## 4.1 `agentforge init` — 專案腳手架

從內建範本快速生成標準化的 AI Agent 專案結構。

### 參數說明

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `--name` | ✅ | — | 專案名稱，用於目錄和套件命名 |
| `--template` | ❌ | `minimal` | 範本類型：`minimal`、`full`、`mcp` |
| `--output-dir` | ❌ | `.`（目前目錄） | 專案建立的目標目錄 |
| `--description` | ❌ | `An AI agent built with AgentForge` | 專案描述，寫入 README 和元資料 |

### 使用範例

```bash
# 使用 full 範本建立專案
agentforge init --name my-agent --template full

# 使用 mcp 範本建立專案到指定目錄
agentforge init --name mcp-server --template mcp --output-dir ./projects

# 建立專案並加入自訂描述
agentforge init --name chatbot --template minimal --description "A customer service chatbot"
```

### 範本比較

| 特性 | minimal | full | mcp |
|------|---------|------|-----|
| 定位 | 輕量入門 | 完整生產級 | MCP 協議服務 |
| 核心檔案 | agent.py, config.py, tools.py | agent.py, config.py, tools.py, memory.py, prompts.py | server.py, tools.py, config.py |
| 記憶管理 | ❌ | ✅ | ❌ |
| 提示詞範本 | ❌ | ✅ | ❌ |
| 單元測試 | ❌ | ✅ | ❌ |
| .env 設定 | ✅ | ✅ | ✅ |
| 適用場景 | 簡單聊天機器人、單任務 Agent、原型驗證 | 生產級 Agent、複雜工作流、多工具 Agent | MCP 工具伺服器、IDE 整合、標準化工具暴露 |

---

## 4.2 `agentforge lint` — 合規檢查

基於 12-Factor Agent 方法論對專案進行自動化合規檢查，輸出 0-100 的綜合評分及詳細改進建議。

### 參數說明

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `--path` | ❌ | `.`（目前目錄） | 待檢查的專案目錄路徑 |
| `--format` | ❌ | `table` | 輸出格式：`table`（表格）或 `json` |
| `--rules` | ❌ | 全部規則 | 指定檢查的規則 ID，如 `F01 F02`（空格分隔） |

### 使用範例

```bash
# 檢查目前目錄
agentforge lint

# 檢查指定目錄
agentforge lint --path ./my-agent

# 僅檢查安全和測試相關規則
agentforge lint --rules F07 F08

# 輸出 JSON 格式報告（便於 CI/CD 整合）
agentforge lint --format json
```

### 12-Factor 規則說明

| 規則 ID | 因子名稱 | 權重 | 說明 |
|---------|---------|------|------|
| F01 | 上下文隔離 (Context Isolation) | 2 | Agent 是否分離了系統/使用者/工具上下文 |
| F02 | 工具介面 (Tool Interface) | 2 | 工具是否有清晰的輸入/輸出 Schema |
| F03 | 控制流程 (Control Flow) | 2 | Agent 是否有顯式的控制流程邏輯和迴圈限制 |
| F04 | 狀態管理 (State Management) | 2 | Agent 狀態是否可持久化（非僅記憶體） |
| F05 | 錯誤處理 (Error Handling) | 2 | 是否有例外處理、重試邏輯和降級方案 |
| F06 | 可觀測性 (Observability) | 1 | 是否設定了日誌和鏈路追蹤 |
| F07 | 安全性 (Security) | 3 | 是否有輸入驗證、無硬編碼密鑰 |
| F08 | 測試 (Testing) | 2 | 是否有單元測試覆蓋 |
| F09 | 設定管理 (Configuration) | 2 | 是否使用環境變數管理設定 |
| F10 | 文件 (Documentation) | 1 | 是否有 README 和程式碼文件 |
| F11 | 依賴管理 (Dependency Management) | 1 | 是否有 requirements.txt 或 pyproject.toml |
| F12 | 部署 (Deployment) | 1 | 是否有 Docker 支援或部署文件 |

### 範例輸出

```
  12-Factor Agent Compliance Report
  Project: /home/user/my-agent

  Overall Score: 75/100
  Checks: 18 passed, 6 failed, 24 total

  ID    Factor                  Weight  Status   Details
  ───   ──────────────────────  ──────  ───────  ──────────────────────
  F01   Context Isolation       2       PASS     3/3
  F02   Tool Interface          2       PARTIAL  2/3 - Tools use structured input/output types
  F03   Control Flow            2       PASS     2/2
  F07   Security                3       FAIL     1/3 - .env.example missing
  ...

  Suggestions:
  [!] [F07] Create a .env.example file documenting required environment variables.
  [!] [F08] Create a tests/ directory with unit tests.
```

---

## 4.3 `agentforge doctor` — 健康診斷

對 AI Agent 專案進行全面的健康檢查，涵蓋 6 大診斷類別，幫助開發者快速發現潛在問題。

### 參數說明

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `--path` | ❌ | `.`（目前目錄） | 待診斷的專案目錄路徑 |
| `--verbose` | ❌ | `false` | 顯示詳細診斷資訊 |

### 6 大診斷類別

| 類別 | 檢查內容 |
|------|---------|
| **Environment（環境）** | Python 版本相容性偵測 |
| **Project Structure（專案結構）** | 必要檔案檢查（README、requirements.txt、.env.example、.gitignore 等） |
| **Security（安全）** | .env 檔案保護、硬編碼密鑰偵測 |
| **Dependencies（依賴）** | 依賴清單完整性、版本鎖定檢查 |
| **Code Quality（程式碼品質）** | 型別註解使用率、文件字串覆蓋率 |
| **Agent（Agent 專項）** | LLM 框架偵測、工具定義、提示詞管理 |

### 使用範例

```bash
# 執行基礎診斷
agentforge doctor

# 執行詳細診斷
agentforge doctor --verbose

# 診斷指定專案
agentforge doctor --path ./my-agent
```

### 範例輸出

```
  ============================================================
    AgentForge Doctor - Health Diagnostics
  ============================================================

  Summary: 8 passed, 2 warnings, 0 failures

  Environment
  [OK]   Python 3.11.5
  [OK]   Compatible with Python >= 3.8

  Project Structure
  [OK]   README.md found
  [OK]   requirements.txt found
  [WARN] .env.example missing
  [OK]   Agent module found

  Security
  [OK]   No hardcoded secrets detected

  Dependencies
  [OK]   5 dependencies listed
  [WARN] 3/5 dependencies have pinned versions

  Code Quality
  [OK]   8 Python file(s) found
  [OK]   6/8 files use type hints
  [OK]   7/8 files have docstrings

  Agent
  [OK]   Using: OpenAI, LangChain
  [OK]   Tool definitions found
  [OK]   Prompt management found
```

---

## 4.4 `agentforge template` — 範本管理

瀏覽和查看 AgentForge-CLI 內建的專案範本詳細資訊。

### 參數說明

| 參數 | 必填 | 說明 |
|------|------|------|
| `--list` | ❌ | 列出所有可用範本 |
| `--info <NAME>` | ❌ | 查看指定範本的詳細資訊 |

### 使用範例

```bash
# 列出所有範本
agentforge template --list

# 查看 full 範本詳情
agentforge template --info full

# 查看 mcp 範本詳情
agentforge template --info mcp
```

### 內建範本一覽

| 範本 | 名稱 | 適用場景 |
|------|------|---------|
| `minimal` | 輕量 Agent | 簡單聊天機器人、單任務 Agent、快速原型 |
| `full` | 完整 Agent | 生產級 Agent、複雜工作流、多工具協作 |
| `mcp` | MCP 相容服務 | MCP 工具伺服器、IDE 整合、標準化工具暴露 |

---

# 💡 設計思路與迭代規劃

## 設計原則

### 🚫 零依賴 (Zero Dependencies)

AgentForge-CLI 完全基於 Python 標準函式庫構建，不依賴任何第三方套件。這意味著：

- 安裝速度極快，無需等待依賴解析
- 無版本衝突風險
- 可在受限網路環境下使用
- 減少供應鏈安全風險

### 📐 約定優於設定 (Convention over Configuration)

內建範本和檢查規則遵循業界最佳實踐，開發者無需從零開始思考專案結構。同時保留足夠的彈性——範本生成的程式碼完全可自訂。

### 🧑‍💻 開發者體驗優先 (Developer Experience First)

- 彩色終端輸出，資訊層次清晰
- 友善的錯誤提示和改進建議
- 一條指令完成複雜操作
- 詳細的說明文件和範例

## 為什麼是 12-Factor for Agents？

傳統的 12-Factor App 方法論為 Web 應用提供了優秀的工程化指導。然而，AI Agent 有著獨特的工程挑戰：

- **上下文管理**：Agent 需要處理系統提示、使用者輸入、工具返回等多種上下文
- **工具介面**：Agent 的能力透過工具暴露，需要嚴格的 Schema 定義
- **控制流程**：Agent 的推理-行動迴圈需要迴圈限制和安全保障
- **狀態持久化**：Agent 的記憶和狀態需要可靠的外部儲存

AgentForge-CLI 將這些 Agent 特有的工程需求轉化為可自動檢查的規則，幫助團隊建立統一的工程標準。

## 迭代規劃

- [ ] **更多範本**：支援 LangGraph、CrewAI、AutoGen 等框架範本
- [ ] **CI/CD 整合**：提供 GitHub Actions / GitLab CI 預配置
- [ ] **VS Code 擴充功能**：在編輯器內直接使用 AgentForge 功能
- [ ] **自訂規則**：支援使用者編寫和載入自訂檢查規則
- [ ] **範本市集**：社群範本共享和安裝機制
- [ ] **專案升級**：偵測範本版本更新並輔助遷移

---

# 📦 安裝與部署

## pip 安裝（推薦）

```bash
pip install agentforge-cli
```

## pipx 安裝（隔離環境，推薦用於工具類 CLI）

```bash
# 安裝 pipx（如尚未安裝）
pip install pipx

# 透過 pipx 安裝 agentforge-cli
pipx install agentforge-cli
```

## 從原始碼安裝

```bash
# 複製倉庫
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# 安裝（開發模式）
pip install -e .

# 或安裝為一般套件
pip install .
```

## Docker（可選）

```bash
# 拉取映像
docker pull agentforge/cli:latest

# 執行合規檢查
docker run --rm -v $(pwd):/workspace agentforge/cli:latest lint --path /workspace

# 建立新專案
docker run --rm -v $(pwd):/workspace agentforge/cli:latest init --name my-agent --template full --output-dir /workspace
```

---

# 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論是提交 Bug 回報、改進文件還是貢獻程式碼。

## 提交 Pull Request

1. **Fork** 本倉庫
2. 建立特性分支：`git checkout -b feature/your-feature-name`
3. 撰寫程式碼並確保通過所有測試：`pytest tests/`
4. 提交變更：`git commit -m "feat: add your feature description"`
5. 推送分支：`git push origin feature/your-feature-name`
6. 提交 **Pull Request**

## 提交 Issue

- **Bug 回報**：請包含重現步驟、預期行為、實際行為以及執行環境資訊
- **功能建議**：請描述使用場景和期望的行為
- **問題諮詢**：請先查閱文件和已有 Issue

## 開發環境搭建

```bash
# 複製倉庫
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/ -v

# 執行測試並產生覆蓋率報告
pytest tests/ --cov=agentforge --cov-report=term-missing
```

---

# 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<a id="english"></a>

# 🎉 Project Introduction

**AgentForge-CLI** is a command-line engineering tool purpose-built for AI Agent developers. It is more than just a project scaffolder -- it is a comprehensive engineering solution that covers the entire AI Agent project lifecycle, from initialization and code compliance checking to health diagnostics.

## Pain Points It Solves

As AI Agents rapidly evolve, developers face numerous engineering challenges:

- **Messy project structures**: Every developer organizes their projects differently, lacking unified standards and driving up collaboration costs
- **Best practices remain on paper**: Methodologies like 12-Factor Agents exist only as documentation, without automated tooling to enforce them
- **Inconsistent code quality**: No linter tools tailored for Agent projects, making it hard to ensure security and maintainability
- **High cost of starting from scratch**: Every new Agent project requires rebuilding the same foundational structure, wasting valuable time

## What Makes Us Different

Unlike the [12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents) methodology (which provides documentation only), AgentForge-CLI turns those principles into an **executable toolchain**:

| Dimension | 12-Factor Agents Docs | AgentForge-CLI |
|-----------|----------------------|----------------|
| Form | Documentation only | Executable CLI tool |
| Project init | Manual reference | One-command scaffolding |
| Compliance | Manual review | Automated lint checks |
| Health diagnostics | None | 6-category automated diagnostics |
| Template support | None | 3 built-in templates |

## Inspiration

This project draws inspiration from the classic software engineering methodology **[The Twelve-Factor App](https://12factor.net/)** and its Agent-domain extension **[12-Factor Agents](https://github.com/AI-Agent-Engineering/12-factor-agents)**. We believe that good engineering practices should not just live in documents -- they should be accessible tools that developers use every day.

---

# ✨ Core Features

- 🔧 **`agentforge init`** -- Generate standardized Agent projects from templates with a single command, supporting 3 built-in templates
- 🔍 **`agentforge lint`** -- Automated 12-Factor Agent compliance checking with a 0-100 score and actionable suggestions
- 🩺 **`agentforge doctor`** -- 6-category health diagnostics to quickly identify project risks
- 📋 **`agentforge template`** -- Browse and inspect built-in project templates
- 📏 **12-Factor Compliance** -- Covers 12 core factors including context isolation, tool interfaces, control flow, and state management
- 📦 **3 Built-in Templates** -- minimal (lightweight), full (production-ready), mcp (MCP protocol compatible)
- 🚫 **Zero Dependencies** -- Built entirely on the Python standard library; install and run with no third-party packages
- 🎨 **Colorful Terminal Output** -- Beautiful ANSI-colored tables, status indicators, and progress spinners

---

# 🚀 Quick Start

## Requirements

- **Python 3.8+** (supports 3.8, 3.9, 3.10, 3.11, 3.12)
- pip package manager
- ANSI color-capable terminal (optional, auto-detected)

## Installation

```bash
# Install via pip (recommended)
pip install agentforge-cli

# Verify installation
agentforge --version
```

## Three Steps to Get Started

```bash
# 1️⃣ Scaffold a new Agent project
agentforge init --name my-agent --template full

# 2️⃣ Enter the project and install dependencies
cd my-agent && pip install -r requirements.txt

# 3️⃣ Check project compliance
agentforge lint
```

## More Commands

```bash
# View all available commands
agentforge --help

# Run health diagnostics
agentforge doctor

# Output compliance report in JSON format
agentforge lint --format json

# List available templates
agentforge template --list
```

---

# 📖 Detailed Usage Guide

## 4.1 `agentforge init` -- Project Scaffolding

Quickly generate a standardized AI Agent project structure from built-in templates.

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--name` | Yes | -- | Project name (used for directory and package naming) |
| `--template` | No | `minimal` | Template type: `minimal`, `full`, or `mcp` |
| `--output-dir` | No | `.` (current dir) | Target directory for project creation |
| `--description` | No | `An AI agent built with AgentForge` | Project description for README and metadata |

### Examples

```bash
# Create a project using the full template
agentforge init --name my-agent --template full

# Create an MCP project in a specific directory
agentforge init --name mcp-server --template mcp --output-dir ./projects

# Create a project with a custom description
agentforge init --name chatbot --template minimal --description "A customer service chatbot"
```

### Template Comparison

| Feature | minimal | full | mcp |
|---------|---------|------|-----|
| Focus | Lightweight starter | Production-ready | MCP protocol server |
| Core files | agent.py, config.py, tools.py | agent.py, config.py, tools.py, memory.py, prompts.py | server.py, tools.py, config.py |
| Memory management | No | Yes | No |
| Prompt templates | No | Yes | No |
| Unit tests | No | Yes | No |
| .env configuration | Yes | Yes | Yes |
| Best for | Simple chatbots, single-task agents, prototyping | Production agents, complex workflows, multi-tool agents | MCP tool servers, IDE integrations, standardized tool exposure |

---

## 4.2 `agentforge lint` -- Compliance Checking

Run automated 12-Factor Agent compliance checks on your project, producing a 0-100 score with detailed improvement suggestions.

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--path` | No | `.` (current dir) | Path to the project directory to check |
| `--format` | No | `table` | Output format: `table` or `json` |
| `--rules` | No | All rules | Specific rule IDs to check (e.g., `F01 F02`, space-separated) |

### Examples

```bash
# Check the current directory
agentforge lint

# Check a specific directory
agentforge lint --path ./my-agent

# Check only security and testing rules
agentforge lint --rules F07 F08

# Output JSON report (for CI/CD integration)
agentforge lint --format json
```

### 12-Factor Rules Reference

| Rule ID | Factor | Weight | Description |
|---------|--------|--------|-------------|
| F01 | Context Isolation | 2 | Agent separates system/user/tool contexts |
| F02 | Tool Interface | 2 | Tools have clear input/output schemas |
| F03 | Control Flow | 2 | Agent has explicit control flow logic and loop limits |
| F04 | State Management | 2 | Agent state is externalized (not in-memory only) |
| F05 | Error Handling | 2 | Exception handling, retry logic, and fallback mechanisms |
| F06 | Observability | 1 | Logging and tracing are configured |
| F07 | Security | 3 | Input validation, no hardcoded secrets |
| F08 | Testing | 2 | Unit test coverage exists |
| F09 | Configuration | 2 | Environment-based configuration management |
| F10 | Documentation | 1 | README and code documentation present |
| F11 | Dependency Management | 1 | requirements.txt or pyproject.toml exists |
| F12 | Deployment | 1 | Docker support or deployment documentation |

### Example Output

```
  12-Factor Agent Compliance Report
  Project: /home/user/my-agent

  Overall Score: 75/100
  Checks: 18 passed, 6 failed, 24 total

  ID    Factor                  Weight  Status   Details
  ---   ----------------------  ------  -------  -----------------------------------
  F01   Context Isolation       2       PASS     3/3
  F02   Tool Interface          2       PARTIAL  2/3 - Tools use structured input/output types
  F03   Control Flow            2       PASS     2/2
  F07   Security                3       FAIL     1/3 - .env.example missing
  ...

  Suggestions:
  [!] [F07] Create a .env.example file documenting required environment variables.
  [!] [F08] Create a tests/ directory with unit tests.
```

---

## 4.3 `agentforge doctor` -- Health Diagnostics

Perform comprehensive health checks on your AI Agent project across 6 diagnostic categories, helping you quickly identify potential issues.

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--path` | No | `.` (current dir) | Path to the project directory to diagnose |
| `--verbose` | No | `false` | Show detailed diagnostic information |

### 6 Diagnostic Categories

| Category | What It Checks |
|----------|---------------|
| **Environment** | Python version compatibility |
| **Project Structure** | Required files (README, requirements.txt, .env.example, .gitignore, etc.) |
| **Security** | .env file protection, hardcoded secret detection |
| **Dependencies** | Dependency list completeness, version pinning |
| **Code Quality** | Type hint usage, docstring coverage |
| **Agent** | LLM framework detection, tool definitions, prompt management |

### Examples

```bash
# Run basic diagnostics
agentforge doctor

# Run verbose diagnostics
agentforge doctor --verbose

# Diagnose a specific project
agentforge doctor --path ./my-agent
```

### Example Output

```
  ============================================================
    AgentForge Doctor - Health Diagnostics
  ============================================================

  Summary: 8 passed, 2 warnings, 0 failures

  Environment
  [OK]   Python 3.11.5
  [OK]   Compatible with Python >= 3.8

  Project Structure
  [OK]   README.md found
  [OK]   requirements.txt found
  [WARN] .env.example missing
  [OK]   Agent module found

  Security
  [OK]   No hardcoded secrets detected

  Dependencies
  [OK]   5 dependencies listed
  [WARN] 3/5 dependencies have pinned versions

  Code Quality
  [OK]   8 Python file(s) found
  [OK]   6/8 files use type hints
  [OK]   7/8 files have docstrings

  Agent
  [OK]   Using: OpenAI, LangChain
  [OK]   Tool definitions found
  [OK]   Prompt management found
```

---

## 4.4 `agentforge template` -- Template Management

Browse and inspect the built-in project templates available in AgentForge-CLI.

### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--list` | No | List all available templates |
| `--info <NAME>` | No | Show detailed information about a specific template |

### Examples

```bash
# List all templates
agentforge template --list

# Show details for the full template
agentforge template --info full

# Show details for the mcp template
agentforge template --info mcp
```

### Built-in Templates Overview

| Template | Name | Best For |
|----------|------|----------|
| `minimal` | Minimal Agent | Simple chatbots, single-task agents, rapid prototyping |
| `full` | Full-Featured Agent | Production agents, complex workflows, multi-tool agents |
| `mcp` | MCP-Compatible Agent | MCP tool servers, IDE integrations, standardized tool exposure |

---

# 💡 Design Philosophy & Roadmap

## Design Principles

### 🚫 Zero Dependencies

AgentForge-CLI is built entirely on the Python standard library with no third-party packages. This means:

- Lightning-fast installation with no dependency resolution
- Zero version conflict risk
- Works in restricted network environments
- Reduced supply chain security risk

### 📐 Convention over Configuration

Built-in templates and lint rules follow industry best practices, so developers don't need to design project structures from scratch. At the same time, full flexibility is preserved -- template-generated code is completely customizable.

### 🧑‍💻 Developer Experience First

- Colorful terminal output with clear information hierarchy
- Friendly error messages and actionable improvement suggestions
- Complex operations completed with a single command
- Comprehensive documentation and examples

## Why 12-Factor for Agents?

The classic 12-Factor App methodology provides excellent engineering guidance for web applications. However, AI Agents present unique engineering challenges:

- **Context management**: Agents need to handle system prompts, user input, tool returns, and other context types
- **Tool interfaces**: Agent capabilities are exposed through tools that require strict schema definitions
- **Control flow**: The agent's reasoning-action loop requires loop limits and safety guarantees
- **State persistence**: Agent memory and state need reliable external storage

AgentForge-CLI transforms these Agent-specific engineering requirements into automatically checkable rules, helping teams establish unified engineering standards.

## Roadmap

- [ ] **More templates**: Support for LangGraph, CrewAI, AutoGen, and other framework templates
- [ ] **CI/CD integration**: Pre-configured GitHub Actions / GitLab CI pipelines
- [ ] **VS Code extension**: Use AgentForge features directly inside the editor
- [ ] **Custom rules**: Support for user-defined lint rules and plugins
- [ ] **Template marketplace**: Community template sharing and installation
- [ ] **Project upgrade**: Detect template version updates and assist with migration

---

# 📦 Installation & Deployment

## pip Install (Recommended)

```bash
pip install agentforge-cli
```

## pipx Install (Isolated Environment, Recommended for CLI Tools)

```bash
# Install pipx (if not already installed)
pip install pipx

# Install agentforge-cli via pipx
pipx install agentforge-cli
```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# Install in development mode
pip install -e .

# Or install as a regular package
pip install .
```

## Docker (Optional)

```bash
# Pull the image
docker pull agentforge/cli:latest

# Run compliance checks
docker run --rm -v $(pwd):/workspace agentforge/cli:latest lint --path /workspace

# Scaffold a new project
docker run --rm -v $(pwd):/workspace agentforge/cli:latest init --name my-agent --template full --output-dir /workspace
```

---

# 🤝 Contributing

We welcome and appreciate contributions of all forms -- whether it's filing bug reports, improving documentation, or contributing code.

## Submitting a Pull Request

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Write code and ensure all tests pass: `pytest tests/`
4. Commit your changes: `git commit -m "feat: add your feature description"`
5. Push the branch: `git push origin feature/your-feature-name`
6. Open a **Pull Request**

## Filing Issues

- **Bug reports**: Please include reproduction steps, expected behavior, actual behavior, and environment details
- **Feature requests**: Describe the use case and expected behavior
- **Questions**: Please check the documentation and existing issues first

## Development Setup

```bash
# Clone the repository
git clone https://github.com/agentforge/agentforge-cli.git
cd agentforge-cli

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=agentforge --cov-report=term-missing
```

---

# 📄 License

This project is released under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 AgentForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```
