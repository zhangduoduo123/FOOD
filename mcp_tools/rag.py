# -*- coding: utf-8 -*-
from typing import Union, List, Optional
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
            "search_k": 3
        }
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}，使用默认配置")
                return self.default_config
        else:
            try:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.default_config, f, indent=4, ensure_ascii=False)
                return self.default_config
            except Exception as e:
                print(f"创建配置文件失败: {str(e)}，使用默认配置")
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

    def _check_ollama_service(self):
        """检查Ollama服务是否运行"""
        try:
            # 尝试创建embeddings实例来检查服务
            OllamaEmbeddings(model=self.config.get("embedding_model"))
        except Exception as e:
            raise RuntimeError(f"Ollama服务未运行或无法连接: {str(e)}")

    def _check_pdf_path(self, pdf_path: Union[str, List[str]]):
        """检查PDF路径是否有效"""
        if isinstance(pdf_path, list):
            for path in pdf_path:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"PDF文件不存在: {path}")
        elif os.path.isdir(pdf_path):
            if not any(f.endswith('.pdf') for f in os.listdir(pdf_path)):
                raise ValueError(f"目录中没有PDF文件: {pdf_path}")
        elif not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

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
            raise RuntimeError(f"向量数据库目录权限错误: {str(e)}")

    def setup_qa_chain(self, pdf_path: Union[str, List[str]] = "pdfs"):
        """设置QA链，支持处理单个文件、文件列表或目录"""
        self._check_pdf_path(pdf_path)
        self._ensure_vector_db_dir()

        # 加载文档
        if isinstance(pdf_path, list):
            documents = []
            for file_path in pdf_path:
                loader = PyPDFLoader(file_path)
                documents += loader.load()
        elif os.path.isdir(pdf_path):
            loader = DirectoryLoader(pdf_path, glob="*.pdf", loader_cls=PyPDFLoader)
            documents = loader.load()
        else:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

        # 文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.get("chunk_size"),
            chunk_overlap=self.config.get("chunk_overlap")
        )
        texts = text_splitter.split_documents(documents)

        # 初始化Ollama嵌入模型
        embeddings = OllamaEmbeddings(model=self.config.get("embedding_model"))

        # 初始化ChromaDB
        vectordb = Chroma.from_documents(
            texts,
            embeddings,
            persist_directory=self.config.get("vector_db_dir")
        )

        # 初始化生成模型
        llm = ChatOllama(
            model=self.config.get("llm_model"),
            temperature=self.config.get("llm_temperature")
        )

        # 定义自定义的提示模板
        qa_prompt = PromptTemplate(
            template="你是一个专业的知识助手，根据以下上下文回答用户的问题。如果不知道答案，请诚实说明。\n"
                     "上下文：\n{context}\n"
                     "问题：\n{question}\n"
                     "回答：",
            input_variables=["context", "question"]
        )

        # 构建问答链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(
                search_kwargs={"k": self.config.get("search_k")}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": qa_prompt}
        )

        return self.qa_chain

    def query_documents(self, query: str, pdf_path: Optional[Union[str, List[str]]] = None) -> str:
        """
        查询文档并返回答案
        
        Args:
            query: 用户的问题
            pdf_path: PDF文件路径或目录路径，如果为None则使用已存在的QA链
            
        Returns:
            str: 回答结果
        """
        try:
            if pdf_path is not None or self.qa_chain is None:
                self.setup_qa_chain(pdf_path or "pdfs")
            
            result = self.qa_chain({"query": query})
            return result["result"]
        except Exception as e:
            return f"处理请求时出错：{str(e)}"


def main():
    """
    主函数，提供命令行交互界面
    """
    try:
        rag = RAGSystem()
        print("欢迎使用文档问答系统！")
        print("输入 'quit' 或 'exit' 退出程序")
        print("输入 'reload' 重新加载文档")
        
        while True:
            query = input("\n请输入您的问题: ").strip()
            
            if query.lower() in ['quit', 'exit']:
                print("感谢使用，再见！")
                break
                
            if not query:
                print("问题不能为空，请重新输入！")
                continue
                
            if query.lower() == 'reload':
                pdf_path = input("请输入PDF文件或目录路径: ").strip()
                if pdf_path:
                    rag.setup_qa_chain(pdf_path)
                    print("文档重新加载完成！")
                continue
                
            response = rag.query_documents(query)
            print("\n回答:", response)
            
    except Exception as e:
        print(f"系统错误: {str(e)}")


if __name__ == "__main__":
    main() 