# 🤖 SQL Agent - 智能数据库问答系统

**用自然语言查询 SQL 数据库！** 无需编写 SQL，直接用中文或英文提问，系统自动生成 SQL 并返回结果。基于多模型协作的智能问答系统，还支持文档检索和多轮对话。

---

## ✨ 特性

- 🦙 **LlamaIndex 加持**: 基于 LlamaIndex 构建的 RAG 系统
- 🧠 **多模型协作**: Planner-Supervisor-Reporter 三模型协同工作
- 🔍 **混合检索**: 向量检索 + 关键词检索双引擎，结果融合提升召回率
- 💡 **智能重试**: SQL 错误自动修正，提高查询成功率
- 💬 **多轮对话**: 支持上下文感知的连贯对话
- 🎨 **现代界面**: Next.js + Tailwind CSS 打造流畅体验
- ⚡ **性能监控**: 详细的模块耗时统计（Planner、检索、执行各环节时间）
- 🔌 **可扩展API**: 基于 OpenAI 兼容接口，支持多种大模型

---

## 🚀 快速开始

### 📋 前置要求

- Python 3.10+
- Node.js 18+
- API Key（默认支持字节跳动豆包API，也可扩展支持其他OpenAI兼容API）
- 本地嵌入模型：`models/bge-base-zh-v1.5`（已包含在项目中）

### 🎯 启动方式

#### 方式一：使用启动脚本（Windows 推荐）

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API Key

# 2. 启动
start.bat
```

#### 方式二：手动启动

**步骤 1：启动后端**
```bash
python backend/app.py
```

**步骤 2：启动前端**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 访问应用

| 服务 | 地址 |
|------|------|
| 🏠 应用 | http://localhost:3000 |
| 🐍 后端 API | http://localhost:8000 |

---

## 🛑 停止服务

```bash
stop.bat        # Windows
```

---

## 🏗️ 架构说明

### 技术栈

**前端**:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Zustand
- Framer Motion

**后端**:
- Python 3.10+
- Flask
- LlamaIndex
- SQLite
- Sentence-Transformers

**AI 模型**:
- 豆包大模型 (Doubao) - 默认
- BGE-base-zh-v1.5

**API兼容性**:
- 基于 OpenAI 兼容接口设计
- 可扩展支持 DeepSeek、通义千问、GPT-4 等

### 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │────│   Backend       │────│   Planner       │
│  (Next.js 3000) │    │  (Flask 8000)  │    │  Supervisor     │
└─────────────────┘    └─────────────────┘    │  Reporter       │
                          │                      └─────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
    ┌─────────▼─────────┐   ┌───────▼────────┐
    │  Vector Search    │   │  Keyword Search │
    │  (LlamaIndex)     │   │                 │
    └─────────┬─────────┘   └───────┬────────┘
              │                       │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   Result Fusion        │
              └─────────────────────────┘
```

---

## 🔧 技术亮点

### 完整前后端分离架构
- 前端 Next.js 14 + 后端 Flask
- 清晰的模块划分和职责边界

### 三Agent智能协作
- **Planner Agent**: 分析用户查询，制定执行计划，决定调用哪些工具
- **Supervisor Agent**: 按计划执行步骤，执行 SQL 或其他工具
- **Reporter Agent**: 基于执行结果生成自然语言回答

### 工具定义与适配
- **SQLExecutor**: SQLite 数据库执行器，统一 JSON 输入输出规范
- **SchemaQuery**: 数据库 Schema 查询器，自动获取表结构信息
- **WebQuery**: 网页查询工具，支持外部信息获取

### 控制策略与工作流
- 智能重试机制：最大重试 1 次，自动修正 SQL 错误
- 支持 Plan-Execute 模式：先规划再执行，确保任务闭环

### 决策逻辑
- 三分类决策：根据查询类型自动选择工具
  - 数据库相关：使用 SQL 工具
  - 知识库相关：使用文档检索
  - 通用知识：直接回答
- 考虑对话历史，提供上下文感知的回答

### 监控与反馈
- 内置性能计时：详细记录 Planner、向量检索、关键词检索、结果融合、执行各环节耗时
- 本地嵌入模型：bge-base-zh-v1.5，零 API 依赖，保障数据隐私
- 索引持久化：首次运行后自动加载已有索引，避免重复创建

### API可扩展性
- 基于 OpenAI 兼容接口设计
- 支持配置 base_url 和 model_name
- 易于扩展到 DeepSeek、通义千问、GPT-4 等

---

## 💡 使用示例

```
用户: 2024年第三季度的总销售额是多少？
系统: 根据数据库记录，2024年第三季度的总销售额为 ¥1,234,567.89

用户: 与第二季度相比增长了多少百分比？
系统: 2024年第三季度相比第二季度销售额增长了 23.5%

用户: 法国的首都是哪里？
系统: 法国的首都是巴黎。
```

---

## 📚 项目亮点（求职向）

这个项目展示了以下 AGENT 开发核心能力：

✅ **RAG 技术**: 基于 LlamaIndex 的向量检索 + 关键词检索混合检索  
✅ **多 Agent 协作**: Planner-Supervisor-Reporter 三模型协同  
✅ **工具调用**: SQLExecutor、SchemaQuery、WebQuery 三大核心工具  
✅ **工程化能力**: Docker 部署支持、性能监控、索引持久化  
✅ **Prompt Engineering**: Few-shot、思维链（CoT）等技巧应用  
✅ **前后端全栈**: Next.js + Flask 完整应用开发  
✅ **API 兼容性**: OpenAI 兼容接口设计，支持多种大模型

---

## 📦 本地模型说明

### 嵌入模型
本项目使用 **BAAI/bge-base-zh-v1.5** 中文嵌入模型，已包含在 `models/bge-base-zh-v1.5` 目录中。

### 模型特点
- 专为中文文本优化
- 零API依赖，保障数据隐私
- 开箱即用，无需额外下载

### 重新下载模型
如果需要重新下载模型，可以运行：
```bash
python download_model.py
```

