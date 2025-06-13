from django.shortcuts import render
from mysql_llm import query_database
from mcp_client import MCPClient
# Create your views here.
# your_app/views.py
from django.http import JsonResponse
import json
from UserApp.models import UserInfo
from asgiref.sync import sync_to_async
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
                
                # 使用sync_to_async包装同步操作
                uid = await sync_to_async(request.session.get)("user_id")
                user_info = await sync_to_async(UserInfo.objects.filter(uid=uid).first)()
                username = user_info.username if user_info else None
                
                if username:
                    question = f"当前用户是{username}，{question}"
                
                try:
                    async with MCPClient() as client:
                        answer, steps = await client.ask(question)
                except Exception as e:
                    # 如果MCP调用失败，返回错误信息
                    return JsonResponse({
                        'error': f'MCP调用失败: {str(e)}',
                        'details': '请检查数据库连接和MCP工具配置'
                    }, status=500)
                return JsonResponse({'answer': answer, 'steps': steps})
            else:
                return JsonResponse({'error': '未提供问题'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'error': '只支持 POST 请求'}, status=405)