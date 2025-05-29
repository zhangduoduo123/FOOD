from django.shortcuts import render
from mysql_llm import query_database
from mcp_client import MCPClient
# Create your views here.
# your_app/views.py
from django.http import JsonResponse
import json

async def get_answer(request):
    if request.method == 'POST':
        try:
            # 获取前端传来的问题
            data = json.loads(request.body)
            question = data.get('question')
            if question:
                # 这里可以添加实际的问题处理逻辑，例如调用大模型接口
                # 目前先简单模拟返回一个固定答案
                # answer = query_database(question)
                async with MCPClient() as client:
                    answer, steps = await client.ask(question)
                return JsonResponse({'answer': answer, 'steps': steps})
            else:
                return JsonResponse({'error': '未提供问题'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'error': '只支持 POST 请求'}, status=405)