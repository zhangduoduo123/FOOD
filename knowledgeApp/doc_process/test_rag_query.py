
import time
from knowledgeApp.doc_process import rag

def main():
    while True:
        question = input("请输入你的问题（输入q退出）：")
        if question.strip().lower() == 'q':
            print("已退出问答。"); break
        start_time = time.time()
        result = rag.query_documents(question)
        end_time = time.time()
        if result.get('status') == 'success':
            print("答案：", result.get('answer', '未找到答案'))
        else:
            print("查询失败：", result.get('message', ''))
        print(f"问答耗时：{end_time - start_time:.2f} 秒\n")

if __name__ == "__main__":
    main() 