# RAG (Retrieval-Augmented Generation) 系统

一个基于本地模型的智能文档问答系统，支持多种文档格式，具有智能相关性判断和对话历史管理功能。

## 功能特点

### 🔍 多文档格式支持
- **PDF文档**: 自动提取文本内容
- **Word文档 (.docx)**: 支持段落和表格
- **Excel文件 (.xls/.xlsx)**: 表格数据转换
- **CSV文件**: 结构化数据处理
- **HTML文件**: 网页内容提取

### 🤖 智能相关性判断
- 使用大模型判断检索文档的相关性
- 自动过滤不相关文档
- 避免使用无关信息生成错误回答

### 💬 对话历史管理
- 自动保存最近三次对话
- 智能合并历史上下文
- 提供连贯的对话体验

### 📊 详细的结果分析
- 显示检索到的完整文档内容
- 提供文档来源信息
- 统计文档分布情况

## 技术架构

### 核心组件
- **向量数据库**: ChromaDB (本地存储)
- **嵌入模型**: Ollama (nomic-embed-text)
- **大语言模型**: Ollama (deepseek-r1:8b)
- **文档处理**: LangChain

### 系统架构
```
用户查询 → 向量检索 → 相关性判断 → 智能回答 → 历史记录
    ↓           ↓           ↓           ↓           ↓
  问题输入   文档召回   大模型判断   RAG/直接回答   对话保存
```

## 安装和配置

### 1. 环境要求
- Python 3.8+
- Ollama (本地模型服务)
- 足够的磁盘空间用于向量数据库

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动Ollama服务
```bash
# 拉取嵌入模型
ollama pull nomic-embed-text

# 拉取大语言模型
ollama pull deepseek-r1:8b
```

### 4. 配置文件
创建 `config.json` 文件：
```json
{
    "embedding_model": "nomic-embed-text",
    "llm_model": "deepseek-r1:8b",
    "llm_temperature": 0.7,
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "vector_db_dir": "chroma_db",
    "search_k": 10
}
```

## 使用方法

### 基本使用

```python
from knowledgeApp.doc_process.rag import query_documents, setup_qa_chain

# 设置QA链
setup_qa_chain("pdfs")

# 查询文档
result = query_documents("什么是营养学？")
print(result["answer"])
```

### 高级功能

```python
# 清空对话历史
from knowledgeApp.doc_process.rag import clear_conversation_history
clear_conversation_history()

# 获取对话历史
from knowledgeApp.doc_process.rag import get_conversation_history
history = get_conversation_history()
print(history)
```

### 直接运行
```bash
python knowledgeApp/doc_process/rag.py
```

## 工作流程示例

### 1. 文档相关查询
```
用户问题: 什么是营养学？

系统处理:
1. 向量检索 → 找到3个相关文档
2. 相关性判断 → 大模型判断文档相关
3. RAG回答 → 基于文档内容生成回答
4. 历史记录 → 保存问答对

输出:
- 检索到的文档内容
- 相关性判断结果
- 基于文档的回答
- 文档引用信息
```

### 2. 文档不相关查询
```
用户问题: 今天天气怎么样？

系统处理:
1. 向量检索 → 找到3个文档（营养相关）
2. 相关性判断 → 大模型判断文档不相关
3. 直接回答 → 使用大模型知识回答
4. 历史记录 → 保存问答对

输出:
- 检索到的文档内容
- 相关性判断结果
- 直接大模型回答
```

## 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `embedding_model` | 嵌入模型名称 | nomic-embed-text |
| `llm_model` | 大语言模型名称 | deepseek-r1:8b |
| `llm_temperature` | 模型温度参数 | 0.7 |
| `chunk_size` | 文档分块大小 | 1000 |
| `chunk_overlap` | 分块重叠大小 | 200 |
| `vector_db_dir` | 向量数据库目录 | chroma_db |
| `search_k` | 检索文档数量 | 10 |

## 文件结构

```
knowledgeApp/doc_process/
├── rag.py                    # 主RAG系统
├── pdfs_import.py           # 文档导入工具
├── rag_test.py              # 测试脚本
└── chromadb_metadata_export.json  # 元数据导出
```

## 主要类和方法

### RAGSystem 类
- `setup_qa_chain()`: 初始化QA链
- `query_documents()`: 查询文档
- `add_to_history()`: 添加历史记录
- `get_history_context()`: 获取历史上下文
- `clear_history()`: 清空历史记录

### 独立函数
- `setup_qa_chain()`: 设置QA链
- `query_documents()`: 查询文档
- `clear_conversation_history()`: 清空对话历史
- `get_conversation_history()`: 获取对话历史

## 注意事项

1. **模型下载**: 确保Ollama服务正常运行，相关模型已下载
2. **文档格式**: 支持常见文档格式，确保文档编码正确
3. **存储空间**: ChromaDB会占用一定磁盘空间
4. **性能优化**: 可根据需要调整chunk_size和search_k参数

## 故障排除

### 常见问题
1. **模型未找到**: 检查Ollama服务状态和模型名称
2. **文档加载失败**: 检查文档格式和文件权限
3. **向量数据库错误**: 检查磁盘空间和目录权限

### 调试模式
系统提供详细的调试信息，包括：
- 检索到的文档内容
- 相关性判断过程
- 历史对话上下文
- 处理时间统计

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。 