from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from knowledgeApp.doc_process import rag
import time




def knowledge(request):
    print("request.method:", request.method)
    print("进入 knowledge 视图")
    if request.method == 'POST':
        try:
            print("收到 POST 请求")
            data = json.loads(request.body)
            print("请求体数据：", data)
            question = data.get('question', '')
            print("问题内容：", question)
            if not question:
                print("未输入问题")
                return JsonResponse({'answer': '请输入问题'}, status=400)
            start_time = time.time()
            #rag = RAGSystem()
            result = rag.query_documents(question)
            print("RAG 查询结果：", result)
            end_time = time.time()
            cost_time = end_time - start_time
            if result.get('status') == 'success':
                answer = result.get('answer', '未找到答案')
            else:
                answer = result.get('message', '查询失败')
            print("最终返回：", {'answer': answer, 'cost_time': cost_time})
            return JsonResponse({'answer': answer, 'cost_time': cost_time})
        except Exception as e:
            print("异常：", e)
            return JsonResponse({'answer': f'服务异常: {str(e)}'}, status=500)
    print("非POST请求，渲染页面")
    return render(request, 'knowledge.html')
# Create your views here.
# def knowledge(request):
#      if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             question = data.get('question', '')
#             if not question:
#                 return JsonResponse({'answer': '请输入问题'}, status=400)
#             # 记录开始时间
#             start_time = time.time()
#             # 调用RAG查询
#             result = rag.query_documents(question)
#             print(result)
#             # 记录结束时间
#             end_time = time.time()
#             cost_time = end_time - start_time
#             if result.get('status') == 'success':
#                 answer = result.get('answer', '未找到答案')
                
#             else:
#                 answer = result.get('message', '查询失败')
#             return JsonResponse({'answer': answer, 'cost_time': cost_time})
#         except Exception as e:
#             return JsonResponse({'answer': f'服务异常: {str(e)}'}, status=500)
#      return render(request, 'knowledge.html')

# @csrf_exempt
# def get_answer(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             question = data.get('question', '')
#             if not question:
#                 return JsonResponse({'answer': '请输入问题'}, status=400)
#             # 调用RAG查询
#             result = rag.query_documents(question)
#             if result.get('status') == 'success':
#                 answer = result.get('answer', '未找到答案')
#             else:
#                 answer = result.get('message', '查询失败')
#             return JsonResponse({'answer': answer})
#         except Exception as e:
#             return JsonResponse({'answer': f'服务异常: {str(e)}'}, status=500)
#     return JsonResponse({'answer': '仅支持POST请求'}, status=405)