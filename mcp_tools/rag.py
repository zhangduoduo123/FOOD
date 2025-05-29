# -*- coding: utf-8 -*-
from typing import Union, List
import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def setup_qa_chain(pdf_path: Union[str, List[str]] = "pdfs"):
    """支持处理单个文件、文件列表或目录"""
    # 加载文档
    if isinstance(pdf_path, list):
        # 处理文件列表
        documents = []
        for file_path in pdf_path:
            loader = PyPDFLoader(file_path)
            documents += loader.load()
    elif os.path.isdir(pdf_path):
        # 处理目录
        loader = DirectoryLoader(pdf_path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
    else:
        # 处理单个文件
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    # 初始化Ollama嵌入模型
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 初始化ChromaDB
    vectordb = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory="chroma_db"
    )

    # 初始化生成模型
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)

    # 定义自定义的提示模板
    qa_prompt = PromptTemplate(
        template="你是一个专业的知识助手，根据以下上下文回答用户的问题。如果不知道答案，请诚实说明。\n"
                 "上下文：\n{context}\n"
                 "问题：\n{question}\n"
                 "回答：",
        input_variables=["context", "question"]
    )

    # 构建问答链，传入自定义的提示模板
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": qa_prompt}
    )

    return qa_chain


def query_documents(query: str, pdf_path: Union[str, List[str]] = "pdfs") -> str:
    """
    查询文档并返回答案
    
    Args:
        query: 用户的问题
        pdf_path: PDF文件路径或目录路径
        
    Returns:
        str: 回答结果
    """
    try:
        qa_chain = setup_qa_chain(pdf_path)
        result = qa_chain({"query": query})
        return result["result"]
    except Exception as e:
        return f"处理请求时出错：{str(e)}"


def main():
    """
    主函数，提供命令行交互界面
    """
    print("欢迎使用文档问答系统！")
    print("输入 'quit' 或 'exit' 退出程序")
    
    while True:
        query = input("\n请输入您的问题: ").strip()
        
        if query.lower() in ['quit', 'exit']:
            print("感谢使用，再见！")
            break
            
        if not query:
            print("问题不能为空，请重新输入！")
            continue
            
        response = query_documents(query)
        print("\n回答:", response)


if __name__ == "__main__":
    main() 