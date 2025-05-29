import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from utils.env_info import DEEPSEEK_API_KEY

# 初始化 DeepSeek 大模型客户端
llm = ChatDeepSeek(
    model="deepseek-chat",  # 指定 DeepSeek 的模型名称
    api_key=DEEPSEEK_API_KEY  # 替换为您自己的 DeepSeek API 密钥
)
# llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
 
# 解析并输出结果
def print_optimized_result(agent_response):
    """
    解析代理响应并输出优化后的结果。
    :param agent_response: 代理返回的完整响应
    """
    messages = agent_response.get("messages", [])
    steps = []  # 用于记录计算步骤
    final_answer = None  # 最终答案
 
    for message in messages:
        if hasattr(message, "additional_kwargs") and "tool_calls" in message.additional_kwargs:
            # 提取工具调用信息
            tool_calls = message.additional_kwargs["tool_calls"]
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = tool_call["function"]["arguments"]
                steps.append(f"调用工具: {tool_name}({tool_args})")
        elif message.type == "tool":
            # 提取工具执行结果
            tool_name = message.name
            tool_result = message.content
            steps.append(f"{tool_name} 的结果是: {tool_result}")
        elif message.type == "ai":
            # 提取最终答案
            final_answer = message.content
 
    # 打印优化后的结果
    print("\n计算过程:")
    for step in steps:
        print(f"- {step}")
    if final_answer:
        print(f"\n最终答案: {final_answer}")

class MCPClient:
    """
    统一MCP客户端接口，支持异步上下文和外部调用。
    """
    def __init__(self):
        self.client = None
        self.agent = None
        self._tools_config = {
            "math": {
                "command": "python",
                "args": ["./mcp_tools/math_tool.py"],
                "transport": "stdio",
            },
            "adjust_RNI": {
                "command": "python",
                "args": ["./mcp_tools/adjust_RNI.py"],
                "transport": "stdio",
            },
            "optimize_dumpling": {
                "command": "python",
                "args": ["./mcp_tools/select_best_nutrition/optimize_dumpling.py"],
                "transport": "stdio",
            },
        
            "rag": {
                "command": "python",
                "args": ["./mcp_tools/rag.py"],
                "transport": "stdio",
            },
        
            "neo4j_llm": {
                "command": "python",
                "args": ["./mcp_tools/neo4j_llm.py"],
                "transport": "stdio",
            },
            
            
        }

    async def __aenter__(self):
        self.client = MultiServerMCPClient(self._tools_config)
        await self.client.__aenter__()
        self.agent = create_react_agent(llm, self.client.get_tools())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc, tb)

    async def ask(self, question: str):
        """
        向MCP智能体提问，返回最终答案和步骤。
        :param question: 用户问题
        :return: (final_answer, steps)
        """
        agent_response = await self.agent.ainvoke({"messages": question})
        messages = agent_response.get("messages", [])
        steps = []
        final_answer = None
        for message in messages:
            if hasattr(message, "additional_kwargs") and "tool_calls" in message.additional_kwargs:
                tool_calls = message.additional_kwargs["tool_calls"]
                for tool_call in tool_calls:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]
                    steps.append(f"调用工具: {tool_name}({tool_args})")
            elif message.type == "tool":
                tool_name = message.name
                tool_result = message.content
                steps.append(f"{tool_name} 的结果是: {tool_result}")
            elif message.type == "ai":
                final_answer = message.content
        return final_answer, steps

# 命令行交互入口
async def main():
    async with MCPClient() as mcp_client:
        while True:
            try:
                user_input = input("\n请输入您的问题（或输入 'exit' 退出）：")
                if user_input.lower() == "exit":
                    print("感谢使用！再见！")
                    break
                final_answer, steps = await mcp_client.ask(user_input)
                print("\n计算过程:")
                for step in steps:
                    print(f"- {step}")
                if final_answer:
                    print(f"\n最终答案: {final_answer}")
            except Exception as e:
                print(f"发生错误：{e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())