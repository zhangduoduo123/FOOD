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
from mysql_llm import query_database

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

def mcp_vote(mysql_answer: str, llm_answer: str, question: str) -> str:
    """实现多数共识协议投票机制"""
    if not mysql_answer:
        return llm_answer
    
    # 使用LLM比较答案
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
    
    prompt = f"""比较以下两个答案，哪个更准确和完整：
    
    问题: "{question}"
    
    MySQL答案: {mysql_answer}
    LLM答案: {llm_answer}
    
    请选择更准确的答案，回复'mysql'或'llm'。"""
    
    try:
        response = llm.invoke(prompt)
        decision = response.content.lower().strip()
        
        if 'mysql' in decision:
            return mysql_answer
        else:
            return llm_answer
    except Exception as e:
        print(f"投票机制出错: {str(e)}")
        return llm_answer
    return mysql_answer

def chatbot_interface(qa_chain, query, history):
    try:
        # 获取最近三次对话
        recent_conversations = []
        if history and len(history) > 0:
            recent_conversations = history[-3:] if len(history) >= 3 else history
        
        conversation_text = ""
        for i, (question, answer) in enumerate(recent_conversations):
            conversation_text += f"对话 {i+1}:\n问题：{question}\n\n"
        
        # 如果有历史对话，生成摘要
        if conversation_text:
            summary_prompt = f"""请对以下对话内容进行简要总结，保留关键信息：
            {conversation_text}
            当前新问题：{query}
            请基于以上对话内容，理解上下文后回答当前问题。"""
            combined_query = summary_prompt
        else:
            combined_query = query

        # 从MySQL获取结构化知识
        mysql_answer = query_database(query)
        
        # 从LLM获取答案
        llm_answer = qa_chain({"query": combined_query})["result"]
        
        # 使用MCP决定最终答案
        final_answer = mcp_vote(mysql_answer, llm_answer, query)
        return final_answer
    except Exception as e:
        return f"处理请求时出错：{str(e)}"

def main():
    qa_chain = setup_qa_chain("pdfs")  # 默认处理pdfs目录下的所有PDF
    iface = gr.ChatInterface(
        fn=lambda message, history: chatbot_interface(qa_chain, message, history),
        title="智能助手",
        description="基于多文档知识库和MySQL数据库的问答系统"
    )
    iface.launch()

if __name__ == "__main__":
    main()