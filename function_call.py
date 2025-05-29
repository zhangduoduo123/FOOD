from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json

# 初始化ChatOllama模型
llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)

# 定义函数工具
functions = [
    {
        "name": "add",
        "description": "将两个数字相加",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字"
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "subtract",
        "description": "从第一个数字中减去第二个数字",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字"
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字"
                }
            },
            "required": ["a", "b"]
        }
    }
]

# 实现函数调用功能
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def process_function_call(function_call):
    """处理函数调用"""
    try:
        function_name = function_call.get("name")
        arguments = json.loads(function_call.get("arguments", "{}"))
        
        if function_name == "add":
            result = add(arguments["a"], arguments["b"])
            return {"result": result}
        elif function_name == "subtract":
            result = subtract(arguments["a"], arguments["b"])
            return {"result": result}
        else:
            return {"error": f"未知函数: {function_name}"}
    except Exception as e:
        return {"error": str(e)}

# 构建提示模板
template = """你是一个能够进行数学计算的助手。
你可以使用函数来执行加减操作。

用户问题: {question}

请尽量使用函数来回答用户的问题。
"""

prompt = ChatPromptTemplate.from_template(template)

# 使用函数调用
def get_response(question):
    # 准备消息
    messages = prompt.format_messages(question=question)
    
    # 调用模型并指定函数
    response = llm.invoke(
        messages,
        functions=functions,
        function_call="auto"  # 让模型决定是否调用函数
    )
    
    # 检查是否有函数调用
    if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
        function_call = response.additional_kwargs["function_call"]
        function_result = process_function_call(function_call)
        
        # 将函数结果发送回模型进行解释
        follow_up_messages = messages + [
            response,
            {
                "role": "function",
                "name": function_call["name"],
                "content": json.dumps(function_result, ensure_ascii=False)
            }
        ]
        
        final_response = llm.invoke(follow_up_messages)
        return final_response.content
    else:
        # 如果模型没有调用函数，直接返回结果
        return response.content

# 测试代码
if __name__ == "__main__":
    while True:
        question = input("\n请输入您的问题 (输入'退出'结束): ")
        if question.lower() in ['退出', 'exit', 'quit']:
            break
        
        response = get_response(question)
        print(f"\n回答: {response}")
