# DeepAgents 深度搜索框架

> 基于 DeepAgents 框架构建的多智能体深度搜索系统 —— 多格式文档解析 × 联网搜索 × RAG 检索 × Agent 任务编排

## 目录

- [项目简介](#项目简介)
- [系统架构](#系统架构)
- [核心功能](#核心功能)
- [技术栈](#技术栈)
- [快速启动](#快速启动)
- [环境变量配置](#环境变量配置)
- [API 接口文档](#api-接口文档)
- [项目结构](#项目结构)
- [使用示例](#使用示例)
- [License](#license)

## 项目简介

DeepAgents 深度搜索框架是一个面向企业级知识检索场景的多智能体协作系统。系统通过一个**主智能体**协调三个专业子智能体（网络搜索、数据库查询、RAGFlow 知识库），实现复杂任务的自动分解与执行，并支持 PDF/Markdown 文档自动生成。

典型应用场景：药品信息查询、行业研究报告生成、企业内部知识问答、多源数据汇总分析。

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                   Vue 3 前端 (UI)                    │
│              WebSocket 实时通信 + 流式输出             │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / WebSocket
┌──────────────────────▼──────────────────────────────┐
│              FastAPI 后端 (API Server)                │
│   /api/task  /api/upload  /api/download  /api/files  │
│                  /ws/{thread_id}                      │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              主智能体 (Main Agent)                    │
│    任务分解 → 子智能体调度 → 结果汇总 → 文档生成       │
├────────┬──────────────┬─────────────────────────────┤
│ 工具层  │  generate_markdown · convert_md_to_pdf     │
│        │  read_file_content                          │
└───┬────┴──────┬───────┴────────────┬────────────────┘
    │           │                    │
┌───▼───┐  ┌───▼────────┐  ┌───────▼──────────┐
│ 网络   │  │  数据库     │  │  RAGFlow         │
│ 搜索   │  │  查询       │  │  知识库           │
│ 子智能体│  │  子智能体    │  │  子智能体          │
├───────┤  ├────────────┤  ├─────────────────┤
│Tavily │  │ MySQL      │  │ RAGFlow SDK      │
│Search │  │ Connector  │  │ 助手问答          │
└───────┘  └────────────┘  └─────────────────┘
```

## 核心功能

| 模块 | 能力 | 说明 |
|------|------|------|
| **多智能体编排** | 主 Agent + 3 子 Agent | 基于 DeepAgents 框架的 `create_deep_agent`，支持任务自动分解与委派 |
| **网络搜索** | Tavily 搜索引擎 | 支持 general / news / finance 分类检索，最多 3 轮多角度搜索 |
| **数据库查询** | MySQL 直连 | 提供表结构浏览、数据预览、自定义 SQL 执行三项工具 |
| **RAG 检索** | RAGFlow SDK | 自动发现知识库助手列表，按需向指定助手提问 |
| **文档生成** | Markdown + PDF | Agent 生成 Markdown 后可自动转换为 PDF，支持文件下载 |
| **文件管理** | 上传/下载/浏览 | 会话级文件隔离，支持多文件上传，路径安全校验防遍历攻击 |
| **流式交互** | WebSocket 实时推送 | 工具调用、子 Agent 进度、最终结果均实时推送到前端 |

## 技术栈

**后端**
- Python 3.12+ · FastAPI · Uvicorn
- DeepAgents（多智能体编排框架）
- LangChain OpenAI（通义千问 Plus 模型）
- Tavily SDK（联网搜索）· RAGFlow SDK 0.24（知识库检索）
- mysql-connector-python（数据库）· Pandas · PyPDF · python-docx

**前端**
- Vue 3 · TypeScript · Vite

**包管理**
- uv（Python 依赖管理）

## 快速启动

### 1. 克隆项目

```bash
git clone https://github.com/liyibo0410/deepagents-framework.git
cd deep_agent_search
```

### 2. 配置环境变量

复制 `.env.example` 并填写以下配置（详见[环境变量配置](#环境变量配置)）：

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Key 和数据库连接信息
```

### 3. 启动后端

```bash
# 安装依赖（使用 uv）
uv sync

# 启动服务（默认端口 8000）
python main.py
```

### 4. 启动前端

```bash
cd ui
npm install
npm run dev
```

访问 http://localhost:5173 打开深度搜索界面。

## 环境变量配置

项目通过 `.env` 文件管理敏感配置，启动时自动加载：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 是 | 阿里云 DashScope API Key（通义千问模型） |
| `DASHSCOPE_BASE_URL` | 是 | DashScope API 端点 |
| `LLM_QWEN_PLUS` | 是 | 模型名称，如 `qwen-plus` |
| `TAVILY_API_KEY` | 是 | Tavily 搜索引擎 API Key |
| `RAGFLOW_API_KEY` | 否 | RAGFlow 服务 API Key |
| `RAGFLOW_BASE_URL` | 否 | RAGFlow 服务地址 |
| `MYSQL_HOST` | 否 | MySQL 主机地址（默认 localhost） |
| `MYSQL_PORT` | 否 | MySQL 端口（默认 3306） |
| `MYSQL_USER` | 否 | MySQL 用户名 |
| `MYSQL_PASSWORD` | 否 | MySQL 密码 |
| `MYSQL_DATABASE` | 否 | MySQL 数据库名 |

## API 接口文档

后端服务启动后，可访问 http://localhost:8000/docs 查看 Swagger 文档。

### HTTP 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/task` | 提交任务，返回 `thread_id`，Agent 在后台异步执行 |
| `POST` | `/api/upload` | 上传文件到指定会话，支持多文件 |
| `GET` | `/api/download` | 根据路径下载输出目录中的文件 |
| `GET` | `/api/files` | 列出指定目录下的所有生成文件 |

### WebSocket 接口

| 路径 | 说明 |
|------|------|
| `/ws/{thread_id}` | 建立 WebSocket 长连接，实时接收任务进度推送 |

推送事件类型：
- `tool_start` — 工具开始执行
- `assistant_call` — 正在调用子智能体
- `task_result` — 任务执行完成，携带最终结果
- `session_created` — 会话工作目录已创建
- `error` — 执行异常

### 请求示例

```bash
# 提交搜索任务
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"query": "查询数据库中销量最高的5种药品", "thread_id": "demo-001"}'

# 上传文件
curl -X POST http://localhost:8000/api/upload \
  -F "thread_id=demo-001" \
  -F "files=@report.pdf"
```

## 项目结构

```
deep_agent_search/
├── agent/                    # 智能体核心逻辑
│   ├── main_agent.py         # 主智能体：任务编排、流式处理、会话管理
│   ├── llm.py                # LLM 模型初始化（通义千问 Plus）
│   ├── load_prompts.py       # Prompt 配置加载
│   └── sub_agents/           # 子智能体
│       ├── internet_sub_agent.py  # 网络搜索子智能体
│       ├── db_sub_agent.py        # 数据库查询子智能体
│       └── rag_sub_agent.py       # RAGFlow 知识库子智能体
├── api/                      # API 层
│   ├── server.py             # FastAPI 路由定义（任务/上传/下载/文件/WebSocket）
│   ├── monitor.py            # WebSocket 监控器（ToolMonitor 单例 + ConnectionManager）
│   └── context.py            # 会话上下文管理（ContextVar 线程安全）
├── tools/                    # 工具模块（LangChain @tool 装饰器）
│   ├── internet_search_tool.py  # Tavily 网络搜索
│   ├── mysql_tools.py           # MySQL 表浏览/数据预览/SQL 执行
│   ├── ragflow_tools.py         # RAGFlow 助手列表/提问
│   ├── markdown_tools.py        # Markdown 文件生成
│   ├── pdf_tools.py             # Markdown → PDF 转换
│   └── upload_file_read_tool.py # 上传文件内容读取
├── prompt/                   # Prompt 模板
│   └── prompts.yml           # 主/子智能体系统提示词配置
├── utils/                    # 工具函数
│   ├── logger_utils.py       # 日志配置（colorlog 彩色输出）
│   ├── converter_utils.py    # 数据转换
│   └── path_utils.py         # 路径处理
├── ui/                       # Vue 3 前端
│   ├── src/
│   │   ├── App.vue           # 主组件
│   │   └── style.css         # 样式
│   ├── package.json
│   └── vite.config.ts
├── sql/                      # 数据库脚本
│   ├── db.sql                # 建表语句
│   └── cps.yml               # 数据配置
├── main.py                   # 应用入口
├── pyproject.toml            # Python 项目配置（uv 管理依赖）
└── README.md
```

## 使用示例

### 示例 1：数据库查询 + 文档生成

在搜索框输入：

```
查询数据库中的药品信息，生成一个PDF报告
```

系统执行流程：
1. 主智能体分析任务，委派**数据库查询助手**获取药品数据
2. 数据库子智能体调用 `list_sql_tables` → `get_table_data` 获取数据
3. 主智能体收到数据后调用 `generate_markdown` 生成报告
4. 调用 `convert_md_to_pdf` 转换为 PDF
5. 前端实时展示每一步进度，最终提供文件下载

### 示例 2：联网搜索 + RAGFlow 知识库

```
搜索最新的AI药物研发趋势，结合内部知识库中的相关论文
```

系统执行流程：
1. **网络搜索助手**通过 Tavily 检索公开信息（多角度，最多 3 轮）
2. **RAGFlow 助手**查询内部知识库中的论文数据
3. 主智能体汇总两路结果，生成综合分析报告

## License

MIT
