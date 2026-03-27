<<<<<<< HEAD
# 🤖 SQL Agent - 智能数据库问答系统

**用自然语言查询 SQL 数据库！** 无需编写 SQL，直接用中文或英文提问，系统自动生成 SQL 并返回结果。基于多模型协作的智能问答系统，还支持文档检索和多轮对话。

---

## ✨ 特性

- 🦙 **LlamaIndex 加持**: 基于 LlamaIndex 构建的 RAG 系统
- 🧠 **多模型协作**: Planner-Supervisor-Reporter 三模型协同工作
- 🔍 **混合检索**: 向量检索 + 关键词检索双引擎
- 💡 **智能重试**: SQL 错误自动修正，提高查询成功率
- 💬 **多轮对话**: 支持上下文感知的连贯对话
- 🎨 **现代界面**: Next.js + Tailwind CSS 打造流畅体验
- ⚡ **性能监控**: 详细的模块耗时统计

---

## 🚀 快速开始

### 📋 前置要求

- Python 3.10+
- Node.js 18+
- ARK API Key

### 🎯 启动方式

#### 方式一：使用启动脚本（Windows 推荐）

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 ARK_API_KEY

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
- 豆包大模型 (Doubao)
- BGE-base-zh-v1.5

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

## 💡 使用示例

```
用户: 2024年第三季度的总销售额是多少？
系统: 根据数据库记录，2024年第三季度的总销售额为 ¥1,234,567.89

用户: 与第二季度相比增长了多少百分比？
系统: 2024年第三季度相比第二季度销售额增长了 23.5%

用户: 法国的首都是哪里？
系统: 法国的首都是巴黎。
```


=======
# sql-agent
>>>>>>> 6949735016edfaebf3a9ee99068765731df38592
