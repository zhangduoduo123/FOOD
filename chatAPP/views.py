from django.shortcuts import render
from mysql_llm import query_database
from mcp_client import MCPClient
# Create your views here.
# your_app/views.py
from django.http import JsonResponse
from UserApp.models import UserInfo
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

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Conservation, Content
from django.utils import timezone
import uuid


def index(request):
    # 检查用户是否已登录（通过 session）
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(uid=10000)
    if user:
        try:
            current_conservation = Conservation.objects.filter(
                uid=user
            ).order_by('-create_time').first()
        except Conservation.DoesNotExist:
            current_conservation = None
    else:
        current_conservation = None
    
    # 如果没有当前对话，创建一个新对话
    if not current_conservation:
        current_conservation = Conservation.objects.create(
            uid=user,
            conservation_title=f"对话 {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            create_time=timezone.now()
        )
    print( 'current_conservation_id:',current_conservation.conservation_id)
    return render(request, 'testqa.html', {
        'current_conservation_id': current_conservation.conservation_id
    })

def get_conversation(request, conversation_id):
    # 获取对话内容
    try:
        conversation = Conservation.objects.get(conservation_id=conversation_id)
        user_id = request.session.get('user_id')
        
        # 检查对话是否属于当前用户
        if conversation.uid != user_id:
            return JsonResponse({'error': '权限不足'}, status=403)
        
        contents = Content.objects.filter(conservation=conversation)
        
        conversation_data = {
            'title': conversation.conservation_title,
            'create_time': conversation.create_time,
            'contents': []
        }
        
        for content in contents:
            conversation_data['contents'].append({
                'question': content.question,
                'answer': content.answer,
                'create_time': content.create_time
            })
            
        return JsonResponse(conversation_data)
    except Conservation.DoesNotExist:
        return JsonResponse({'error': '对话不存在'}, status=404)

def add_message(request):
    print(request.method)
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        question = request.POST.get('question')
        
        # 简单的AI响应模拟（实际应用中应替换为真实AI服务）
        answer = f"AI助手: 收到了您的问题 '{question}'，这是一个模拟回答。"
        
        try:
            conversation = Conservation.objects.get(conservation_id=conversation_id)
            user_id = request.session.get('user_id')
            
            # 检查对话是否属于当前用户
            if conversation.uid != user_id:
                return JsonResponse({'error': '权限不足'}, status=403)
            
        except Conservation.DoesNotExist:
            return JsonResponse({'error': '对话不存在'}, status=404)
        
        content = Content.objects.create(
            conservation=conversation,
            question=question,
            answer=answer
        )
        
        return JsonResponse({
            'content_id': content.content_id,
            'question': content.question,
            'answer': content.answer,
            'create_time': content.create_time
        })
    
    return JsonResponse({'error': '无效请求'}, status=400)

def new_conversation(request):
    # 创建新对话
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(uid=10000)
    
    conversation = Conservation.objects.create(
        uid=user,
        conservation_title=f"对话 {timezone.now().strftime('%Y-%m-%d %H:%M')}",
        create_time=timezone.now()
    )
    
    return JsonResponse({
        'conversation_id': conversation.conservation_id,
        'title': conversation.conservation_title,
        'create_time': conversation.create_time
    })

def clear_conversation(request, conversation_id):
    try:
        conversation = Conservation.objects.get(conservation_id=conversation_id)
        user_id = request.session.get('user_id')
        
        # 检查对话是否属于当前用户
        if conversation.uid != user_id:
            return JsonResponse({'error': '权限不足'}, status=403)
        
        Content.objects.filter(conservation=conversation).delete()
        return JsonResponse({'success': True})
    except Conservation.DoesNotExist:
        return JsonResponse({'error': '对话不存在'}, status=404)