from typing import Union, List
import os
import gradio as gr
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


def chatbot_interface(qa_chain, query, history):
   
    try:
        # 获取上一轮对话
        previous_question = ""
        if history and len(history) > 0:
            previous_question = history[-1][0]  # 获取上一轮的问题
            print(previous_question)
        
        # 组合问题
        combined_query = f"上一轮问题：{previous_question}\n当前问题：{query}" if previous_question else query
        print(combined_query)
        # 执行查询
        result = qa_chain({"query": combined_query})
        return result["result"]
    except Exception as e:
        return f"处理请求时出错：{str(e)}"


def main():
    qa_chain = setup_qa_chain("pdfs")  # 默认处理pdfs目录下的所有PDF
    iface = gr.ChatInterface(
        fn=lambda message, history: chatbot_interface(qa_chain, message, history),
        title="智能助手",
        description="基于多文档知识库的问答系统"
    )
    iface.launch()


if __name__ == "__main__":
    main()