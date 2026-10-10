<div align="center">

# agent-paradigms

**用统一工程结构实现智能体的经典范式：ReAct · Plan-and-Solve · Reflection**

[![Python](https://img.shields.io/badge/Python-%3E%3D3.9-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-如何扩展新范式)

</div>

---

## 📖 项目简介

`agent-paradigms` 是一个面向学习的 **智能体（Agent）经典范式** 实现集合。
它把「大模型调用、工具、工具执行器」等**公共能力**抽取到 `common/`，每种范式各自一个独立子目录，
因此新增一种范式时无需重复造轮子，只需专注该范式自身的思考流程。

项目目前实现了三种最经典、也最常用的 Agent 范式：

| 范式 | 一句话说明 | 核心思想 |
| --- | --- | --- |
| **ReAct** | 边想边做、边做边想 | Reasoning + Acting：`Thought → Action → Observation` 循环 |
| **Plan-and-Solve** | 先规划，再执行 | 先把复杂问题拆成子任务，再逐步求解 |
| **Reflection** | 先做一版，再自我批评并改进 | 生成 → 反思 → 优化 的迭代闭环 |

---

## ✨ 项目特色

- **结构统一**：三种范式共用同一套工程骨架，便于横向对比与扩展。
- **职责清晰**：提示词、智能体逻辑、运行入口分文件存放，公共能力统一收敛到 `common/`。
- **易于运行**：仅需配置一个兼容 OpenAI 接口的模型服务即可开始。

---

## 🗂️ 目录结构

```
agent-paradigms/
├── .env                      # 你的私有配置（已在 .gitignore 中排除，请勿提交）
├── .env.example              # 配置模板，复制为 .env 后填写
├── .gitignore
├── requirements.txt          # 依赖清单
├── README.md
├── common/                   # 公共基础能力（所有范式共用）
│   ├── __init__.py
│   ├── llm.py                # LLMClient：兼容 OpenAI 接口，流式输出
│   ├── tool_executor.py      # ToolExecutor：工具注册 / 执行器
│   └── tools.py              # 具体工具实现（Kimi / Moonshot 联网搜索）
├── ReAct/                    # 范式一：ReAct
│   ├── __init__.py
│   ├── prompt.py             # ReAct 提示词模板
│   ├── agent.py              # ReActAgent：Thought → Action → Observation
│   └── main.py               # 运行入口
├── PlanAndSolve/             # 范式二：Plan-and-Solve
│   ├── __init__.py
│   ├── prompt.py             # 规划器 / 执行器提示词模板
│   ├── agent.py              # Planner + Executor + PlanAndSolveAgent
│   └── main.py               # 运行入口
└── Reflection/               # 范式三：Reflection
    ├── __init__.py
    ├── prompt.py             # 初始 / 反思 / 优化提示词模板
    ├── memory.py             # ReflectionMemory：记录执行与反思轨迹
    ├── agent.py              # ReflectionAgent
    └── main.py               # 运行入口
```

---

## ⚙️ 环境要求

- **Python >= 3.9**（推荐 3.10 / 3.11；代码使用了 `list[str]` 等内建泛型注解）
- 一个可用的、**兼容 OpenAI 接口**的大模型服务（如 DeepSeek、Kimi、OpenAI 等）
- 如需使用联网搜索工具，还需要 Kimi（Moonshot）的搜索 API

---

## 🚀 快速开始

### 第 0 步：获取代码

```bash
git clone <your-repo-url> agent-paradigms
cd agent-paradigms
```

### 第 1 步：创建虚拟环境（conda / venv / uv 三选一）

<details open>
<summary><b>方式 A · conda（推荐给数据科学用户）</b></summary>

```bash
# 创建并激活
conda create -n agent-paradigms python=3.11 -y
conda activate agent-paradigms

# 安装依赖
pip install -r requirements.txt
```

</details>

<details>
<summary><b>方式 B · venv（Python 自带，零额外依赖）</b></summary>

```bash
# 创建虚拟环境
python -m venv .venv

# 激活
# Windows (PowerShell / CMD)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

</details>

<details>
<summary><b>方式 C · uv（最快，推荐）</b></summary>

```bash
# 安装 uv（若尚未安装，任选其一）
pip install uv
# 或：curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建并激活虚拟环境
uv venv
# Windows (PowerShell / CMD)
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 安装依赖（uv 会显著加速）
uv pip install -r requirements.txt
```

</details>

### 第 2 步：配置 `.env` 环境变量

把模板复制为 `.env`，并填入你自己的密钥：

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

`.env` 需要放在**项目根目录**（`agent-paradigms/` 下）。程序通过 `python-dotenv` 的
`load_dotenv()` 自动向上查找，因此无论从哪个子模块运行都能读到它。

各变量含义如下：

| 变量名 | 是否必填 | 说明 | 示例 |
| --- | :---: | --- | --- |
| `LLM_API_KEY` | ✅ | 大模型 API Key | `sk-xxxxxxxx` |
| `LLM_MODEL_ID` | ✅ | 模型 ID（按你的服务商填写） | `deepseek-chat` |
| `LLM_BASE_URL` | ✅ | 兼容 OpenAI 的接口地址 | `https://api.deepseek.com` |
| `LLM_TIMEOUT` | ⬜ | 请求超时时间（秒），默认 60 | `60` |
| `MOONSHOT_API_KEY` | ⬜ | Kimi（Moonshot）搜索工具的 Key | `sk-xxxxxxxx` |
| `MOONSHOT_BASE_URL` | ⬜ | Kimi 搜索接口地址，ReAct 联网搜索用 | `https://api.moonshot.cn/v1/tools/search` |

> `MOONSHOT_*` 仅在使用 ReAct 的 `Search` 工具时需要；不使用联网搜索可不填。

### 第 3 步：运行

⚠️ 请务必在**项目根目录**、以 `-m` 模块方式运行，这样 `common` / `ReAct` / `PlanAndSolve` / `Reflection`
才能被正确导入：

```bash
# 运行 ReAct（会调用联网搜索工具）
python -m ReAct.main

# 运行 Plan-and-Solve
python -m PlanAndSolve.main

# 运行 Reflection
python -m Reflection.main
```

> 不要使用 `python ReAct/main.py` 这种直接执行脚本的方式：那会把 `ReAct/` 当作 `sys.path` 根，
> 导致 `common` 导入失败。

---

## 🧠 范式详解

### 1. ReAct —— Reasoning + Acting

**思想**：让大模型在“思考”和“行动”之间交替循环。每一步先推理当前该做什么（`Thought`），
再决定调用哪个工具（`Action`），拿到工具结果（`Observation`）后作为下一轮的依据；
当信息足够时，用 `Finish[最终答案]` 收尾。

**循环流程**：

```
Question
   │
   ▼
┌──────────────┐
│   Thought    │  大模型推理下一步
└──────┬───────┘
       ▼
┌──────────────┐
│    Action    │  调用工具 Tool[input]  或  Finish[answer]
└──────┬───────┘
       ▼
┌──────────────┐
│ Observation  │  工具真实执行结果
└──────┬───────┘
       │  追加到历史，进入下一轮
       └────────► 直到 Finish 或达到 max_steps
```

**涉及文件**：

- `ReAct/prompt.py`：`REACT_PROMPT_TEMPLATE`，规定 `Thought` / `Action` 的输出格式。
- `ReAct/agent.py`：`ReActAgent`，主循环与输出解析（`_parse_output` / `_parse_action`）。
- `common/tools.py`：具体工具（Kimi 联网搜索）。
- `common/tool_executor.py`：工具注册与执行。

**运行**：`python -m ReAct.main`

---

### 2. Plan-and-Solve —— 先规划，再执行

**思想**：把「规划」和「执行」拆成两个阶段。先让大模型把复杂问题分解成一个有序的子任务清单，
再严格按清单一步步求解，每一步都带上原始问题、完整计划和已完成的历史。

**流程**：

```
Question
   │
   ▼
┌─────────────────┐
│ Planner.plan()  │  大模型输出一个 Python 列表：["步骤1", "步骤2", ...]
└────────┬────────┘
         ▼
┌─────────────────┐
│ Executor.execute│  逐条执行：问题 + 完整计划 + 历史 + 当前步骤 → 该步答案
└────────┬────────┘
         ▼
      最终答案（最后一步的输出）
```

**涉及文件**：

- `PlanAndSolve/prompt.py`：`PLANNER_PROMPT_TEMPLATE`、`EXECUTOR_PROMPT_TEMPLATE`。
- `PlanAndSolve/agent.py`：`Planner`（生成计划）、`Executor`（执行计划）、`PlanAndSolveAgent`（编排）。

**运行**：`python -m PlanAndSolve.main`

---

### 3. Reflection —— 生成 → 反思 → 优化

**思想**：让智能体“自我批评”。先给出初版答案（例如一段代码），再让另一个“评审员”角色挑毛病，
根据反馈生成改进版，如此迭代，直到评审认为“无需改进”或达到最大轮数。

**流程**：

```
Task
  │
  ▼
┌──────────────────┐
│ 初始执行 (Initial)│  生成初版代码，写入 Memory
└────────┬─────────┘
         ▼
   ┌─────────────┐
   │  反思 Reflect│  审查上一版，给出反馈
   └──────┬──────┘
          │ "无需改进" ? ──是──► 结束，返回最后一版
          ▼ 否
   ┌─────────────┐
   │  优化 Refine │  结合反馈生成新版代码，写入 Memory
   └──────┬──────┘
          └────────► 回到反思（最多 max_iterations 轮）
```

**涉及文件**：

- `Reflection/prompt.py`：`INITIAL_PROMPT_TEMPLATE`、`REFLECT_PROMPT_TEMPLATE`、`REFINE_PROMPT_TEMPLATE`。
- `Reflection/memory.py`：`ReflectionMemory`，按时间顺序记录 `execution` / `reflection` 轨迹。
- `Reflection/agent.py`：`ReflectionAgent`，编排整个迭代过程。

**运行**：`python -m Reflection.main`

---

## 🧩 如何扩展新范式

以新增 `MyPattern` 为例：

```bash
mkdir MyPattern
touch MyPattern/__init__.py MyPattern/prompt.py MyPattern/agent.py MyPattern/main.py
```

1. `MyPattern/prompt.py`：放该范式的提示词模板。
2. `MyPattern/agent.py`：实现核心类，复用 `common.llm.LLM` 等公共能力。
3. `MyPattern/main.py`：组装并运行：

   ```python
   from common.llm import LLMClient
   from MyPattern.agent import MyPatternAgent

   agent = MyPatternAgent(LLMClient())
   agent.run("你的问题")
   ```

4. 运行：`python -m MyPattern.main`
5. 在 README 的范式列表与目录结构中补上一行。

**约定**：所有范式共享 `common/`，不要复制公共代码；提示词与主逻辑分文件；入口只负责组装。

---

## ❓ 常见问题（FAQ）

**Q1：为什么必须用 `python -m ReAct.main`？**

因为导入路径是包路径（`from common.llm import LLMClient`、`from ReAct.agent import ...`）。
`-m` 会把项目根目录加入 `sys.path`，直接 `python ReAct/main.py` 则不行。

**Q2：报错“模型 ID、API 密钥和服务地址必须通过参数传入或在 .env 文件中配置”？**

说明根目录 `.env` 缺失或变量没填对，请对照上面的变量表检查。

**Q3：ReAct 一直没有 `Finish`，跑满 `max_steps`？**

通常是：模型输出格式不符合 `Thought:` / `Action:`；或搜索工具返回错误/无关内容，
模型只能反复重试。可检查 `MOONSHOT_*` 配置与 `tools.py` 的返回内容。

**Q4：Windows 下中文/emoji 报 `UnicodeEncodeError`？**

导入 `common` 包时会自动把标准输出与标准错误切换为 UTF-8，通常无需额外处理；
若仍异常，可在命令行设置 `set PYTHONIOENCODING=utf-8`（Windows）或
`export PYTHONIOENCODING=utf-8`（macOS/Linux）。

---

## 📄 开源许可

本项目基于 **MIT License** 发布，完整协议文本见 [`LICENSE`](./LICENSE)。

Copyright (c) 2026 Cookie

你可以自由地使用、修改、分发本项目（包括商业用途），只需在副本或重要部分中保留上述版权声明与许可声明即可。

> 本项目仅用于学习与交流。

---

<div align="center">

如果这个项目对你有帮助，欢迎 ⭐ Star 支持一下～

</div>
