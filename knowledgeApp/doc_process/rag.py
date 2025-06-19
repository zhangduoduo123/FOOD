# -*- coding: utf-8 -*-
from typing import Union, List, Optional, Dict
import os
import json
from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
# import logging
from mcp.server.fastmcp import FastMCP
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import traceback
from docx import Document as DocxDocument
import time
from functools import lru_cache

# 导入DeepSeek API密钥
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# from utils.env_info import DEEPSEEK_API_KEY

# 创建 FastMCP 实例
mcp = FastMCP("RAG")

# 全局RAG实例
_rag_instance = None

class Config:
    """配置管理类"""
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.default_config = {
            "embedding_model": "nomic-embed-text",
            "llm_model": "qwen2.5:7b",
            "llm_temperature": 0.7,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "vector_db_dir": "chroma_db",
            "search_k": 5
        }
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                # logger.error(f"加载配置文件失败: {str(e)}，使用默认配置")
                return self.default_config
        else:
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.default_config, f, indent=4, ensure_ascii=False)
                return self.default_config
            except Exception as e:
                # logger.error(f"创建配置文件失败: {str(e)}，使用默认配置")
                return self.default_config

    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)

class RAGSystem:
    """RAG系统主类"""
    def __init__(self, config_path: str = "config.json"):
        self.config = Config(config_path)
        self.qa_chain = None
        self._check_ollama_service()
        self.embeddings_model = None

    def _check_ollama_service(self):
        """检查Ollama服务是否运行"""
        try:
            # 尝试创建embeddings实例来检查服务
            OllamaEmbeddings(model=self.config.get("embedding_model"))
            print("[Ollama检查] ✓ 服务连接正常")
                
        except Exception as e:
            # logger.error(f"Ollama服务未运行或无法连接: {str(e)}")
            raise RuntimeError(f"Ollama服务未运行或无法连接: {str(e)}")

    def _check_pdf_path(self, pdf_path: Union[str, List[str]]):
        """检查PDF路径是否有效"""
        if isinstance(pdf_path, list):
            for path in pdf_path:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"文件不存在: {path}")
        elif os.path.isdir(pdf_path):
            if not any(f.endswith(('.pdf', '.csv', '.xls', '.xlsx', '.html', '.docx')) for f in os.listdir(pdf_path)):
                raise ValueError(f"目录中没有可用的知识文件: {pdf_path}")
        elif not os.path.exists(pdf_path):
            raise FileNotFoundError(f"文件不存在: {pdf_path}")

    def _ensure_vector_db_dir(self):
        """确保向量数据库目录存在且有写入权限"""
        db_dir = self.config.get("vector_db_dir")
        try:
            Path(db_dir).mkdir(parents=True, exist_ok=True)
            # 测试写入权限
            test_file = Path(db_dir) / ".test"
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            # logger.error(f"向量数据库目录权限错误: {str(e)}")
            raise RuntimeError(f"向量数据库目录权限错误: {str(e)}")

    def _load_table_file(self, file_path: str) -> list:
        """加载表格文件（csv, xlsx, html），返回文本块列表"""
        ext = os.path.splitext(file_path)[-1].lower()
        blocks = []
        if ext == '.csv':
            df = pd.read_csv(file_path)
            blocks = self._split_dataframe(df)
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
            blocks = self._split_dataframe(df)
        elif ext == '.html':
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                tables = soup.find_all('table')
                for table in tables:
                    df = pd.read_html(str(table))[0]
                    blocks.extend(self._split_dataframe(df))
        return blocks

    def _split_dataframe(self, df: pd.DataFrame) -> list:
        """将DataFrame每一行转为文本块"""
        blocks = []
        headers = df.columns.tolist()
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            block = '\n'.join([f"{h}: {row_dict[h]}" for h in headers])
            blocks.append(block)
        return blocks

    def _load_documents(self, pdf_path: Union[str, List[str]]) -> list:
        """加载PDF、表格和Word文件，返回所有文本块"""
        documents = []
        def load_docx(file_path):
            docx = DocxDocument(file_path)
            text = '\n'.join([para.text for para in docx.paragraphs if para.text.strip()])
            return [Document(page_content=text, metadata={})] if text else []
        if isinstance(pdf_path, list):
            for file_path in pdf_path:
                ext = os.path.splitext(file_path)[-1].lower()
                if ext in ['.pdf']:
                    loader = PyPDFLoader(file_path)
                    documents += loader.load()
                elif ext in ['.csv', '.xls', '.xlsx', '.html']:
                    table_blocks = self._load_table_file(file_path)
                    for block in table_blocks:
                        documents.append(Document(page_content=block, metadata={}))
                elif ext == '.docx':
                    documents += load_docx(file_path)
        elif os.path.isdir(pdf_path):
            # 目录下所有支持的文件
            for file in os.listdir(pdf_path):
                file_path = os.path.join(pdf_path, file)
                ext = os.path.splitext(file)[-1].lower()
                if ext == '.pdf':
                    loader = PyPDFLoader(file_path)
                    documents += loader.load()
                elif ext in ['.csv', '.xls', '.xlsx', '.html']:
                    table_blocks = self._load_table_file(file_path)
                    for block in table_blocks:
                        documents.append(Document(page_content=block, metadata={}))
                elif ext == '.docx':
                    documents += load_docx(file_path)
        else:
            ext = os.path.splitext(pdf_path)[-1].lower()
            if ext == '.pdf':
                loader = PyPDFLoader(pdf_path)
                documents += loader.load()
            elif ext in ['.csv', '.xls', '.xlsx', '.html']:
                table_blocks = self._load_table_file(pdf_path)
                for block in table_blocks:
                    documents.append(Document(page_content=block, metadata={}))
            elif ext == '.docx':
                documents += load_docx(pdf_path)
        return documents

    def setup_qa_chain(self, pdf_path: Union[str, List[str]] = "pdfs"):
        """设置QA链，支持处理PDF、表格文件、文件列表或目录"""
        try:
            t0 = time.time()
            print("[setup_qa_chain] 开始检查PDF路径")
            self._check_pdf_path(pdf_path)
            t1 = time.time()
            print(f"[setup_qa_chain] 检查PDF路径完成，耗时: {t1-t0:.2f}s")

            print("[setup_qa_chain] 确保向量数据库目录存在")
            self._ensure_vector_db_dir()
            t2 = time.time()
            print(f"[setup_qa_chain] 向量数据库目录检查完成，耗时: {t2-t1:.2f}s")

            db_dir = self.config.get("vector_db_dir")
            embeddings = OllamaEmbeddings(model=self.config.get("embedding_model"))
            vectordb = None

            # 判断ChromaDB是否已存在
            if os.path.exists(db_dir) and os.listdir(db_dir):
                print("[setup_qa_chain] ChromaDB目录下有文件，直接加载")
                vectordb = Chroma(persist_directory=db_dir, embedding_function=embeddings)
                t3 = time.time()
                print(f"[setup_qa_chain] 加载ChromaDB完成，耗时: {t3-t2:.2f}s")
            else:
                print("[setup_qa_chain] 加载文档和表格")
                documents = self._load_documents(pdf_path)
                t3 = time.time()
                print(f"[setup_qa_chain] 文档加载完成，共{len(documents)}个文档，耗时: {t3-t2:.2f}s")
                # 统一转换为Document对象
                documents = [
                    doc if isinstance(doc, Document) else Document(page_content=doc.get("page_content", ""), metadata=doc.get("metadata", {}))
                    for doc in documents
                ]
                print("[setup_qa_chain] 文档对象转换完成")
                # 文本分割
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.config.get("chunk_size"),
                    chunk_overlap=self.config.get("chunk_overlap")
                )
                texts = text_splitter.split_documents(documents)
                t4 = time.time()
                print(f"[setup_qa_chain] 文本分割完成，共{len(texts)}个分块，耗时: {t4-t3:.2f}s")
                # 初始化ChromaDB
                vectordb = Chroma.from_documents(
                    texts,
                    embeddings,
                    persist_directory=db_dir
                )
                t5 = time.time()
                print(f"[setup_qa_chain] ChromaDB已新建并持久化，耗时: {t5-t4:.2f}s")

            print("[setup_qa_chain] 初始化生成模型")
            llm = ChatOllama(
                model=self.config.get("llm_model"),
                temperature=self.config.get("llm_temperature")
            )
            t6 = time.time()
            print(f"[setup_qa_chain] 生成模型初始化完成，耗时: {t6-(t5 if 't5' in locals() else t3):.2f}s")

            print("[setup_qa_chain] 构建QA链")
            qa_prompt = PromptTemplate(
                template="你是一个专业的知识助手，根据以下上下文回答用户的问题。如果不知道答案，请诚实说明。\n"
                         "重要提示：以下上下文中的每个文档都包含类别信息（class）、质量得分（score）和来源名称（name）。"
                         "请充分利用这些信息来提供更准确的答案：\n"
                         "1. 优先参考与问题最相关的类别文档\n"
                         "2. 考虑文档的质量得分，得分越高的文档越可靠\n"
                         "3. 注意文档来源的权威性\n"
                         "4. 如果不同类别的文档有冲突，请综合判断并说明\n\n"
                         "5. 文档名称也是重要的分类依据\n\n"
                         "上下文信息：\n{context}\n\n"
                         "用户问题：{question}\n\n"
                         "请根据上述上下文，结合文档的类别、质量和来源信息，提供准确、全面的回答。"
                         "如果不知道答案，请诚实说明。回答要结构清晰，重点突出。\n\n",
                input_variables=["context", "question"]
            )

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectordb.as_retriever(
                    search_kwargs={"k": self.config.get("search_k")}
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": qa_prompt}
            )
            t7 = time.time()
            print(f"[setup_qa_chain] QA链构建完成，耗时: {t7-t6:.2f}s，总耗时: {t7-t0:.2f}s")
            return True
        except Exception as e:
            print("[setup_qa_chain] 异常：", e)
            return False

    @lru_cache(maxsize=1000)
    def get_embedding(self, text: str):
        return self.embeddings_model.embed_query(text)

    def monitor_llm_performance(self, query: str, docs: list) -> Dict:
        """监控LLM推理性能"""
        try:
            t0 = time.time()
            
            # 计算输入长度
            total_input_length = len(query) + sum(len(doc.page_content) for doc in docs)
            
            # 执行推理
            result = self.qa_chain.combine_documents_chain.run({
                "input_documents": docs, 
                "question": query
            })
            
            t1 = time.time()
            inference_time = t1 - t0
            
            # 性能分析
            performance_info = {
                "inference_time": inference_time,
                "input_length": total_input_length,
                "docs_count": len(docs),
                "chars_per_second": total_input_length / inference_time if inference_time > 0 else 0,
                "model": self.config.get("llm_model"),
                "performance_level": self._assess_performance_level(inference_time, total_input_length)
            }
            
            print(f"[性能监控] 推理时间: {inference_time:.2f}s")
            print(f"[性能监控] 输入长度: {total_input_length} 字符")
            print(f"[性能监控] 处理速度: {performance_info['chars_per_second']:.0f} 字符/秒")
            print(f"[性能监控] 性能等级: {performance_info['performance_level']}")
            
            return performance_info
            
        except Exception as e:
            return {"error": str(e)}

    def _assess_performance_level(self, inference_time: float, input_length: int) -> str:
        """评估性能等级"""
        chars_per_second = input_length / inference_time if inference_time > 0 else 0
        
        if chars_per_second > 1000:
            return "优秀"
        elif chars_per_second > 500:
            return "良好"
        elif chars_per_second > 200:
            return "一般"
        else:
            return "较慢"

@mcp.tool()
def setup_qa_chain(pdf_path: Union[str, List[str]] = "pdfs") -> Dict:
    """设置QA链，支持处理单个文件、文件列表或目录"""
    global _rag_instance
    try:
        if _rag_instance is None:
            _rag_instance = RAGSystem()
        
        success = _rag_instance.setup_qa_chain(pdf_path)
        if success:
            return {"status": "success", "message": "QA chain setup completed"}
        else:
            return {"status": "error", "message": "Failed to setup QA chain"}
    except Exception as e:
        # logger.error(f"Error in setup_qa_chain: {e}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
def query_documents(query: str, pdf_path: Optional[Union[str, List[str]]] = None) -> Dict:
    """查询文档并返回答案"""
    global _rag_instance
    try:
        t0 = time.time()
        if _rag_instance is None:
            _rag_instance = RAGSystem()
        t1 = time.time()
        if pdf_path is not None or _rag_instance.qa_chain is None:
            success = _rag_instance.setup_qa_chain(pdf_path or "pdfs")
            if not success:
                return {"status": "error", "message": "Failed to setup QA chain"}
        t2 = time.time()
        if _rag_instance.qa_chain is None:
            return {"status": "error", "message": "QA chain not initialized"}
        
        # 召回文档
        retriever = _rag_instance.qa_chain.retriever
        docs = retriever.get_relevant_documents(query)
        t3 = time.time()
        
        # 用召回的文档做QA
        result = _rag_instance.qa_chain.combine_documents_chain.run({"input_documents": docs, "question": query})
        t4 = time.time()
        
        print(f"[耗时分析] 初始化RAG: {t1-t0:.2f}s, QA链setup: {t2-t1:.2f}s, 文档召回: {t3-t2:.2f}s, LLM推理: {t4-t3:.2f}s, 总计: {t4-t0:.2f}s")
        
        return {
            "status": "success",
            "answer": result,
            "sources": [doc.page_content for doc in docs],
            "topk_contents": [doc.page_content for doc in docs]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # logger.info("Starting RAG server through MCP")
    mcp.run(transport="stdio") 