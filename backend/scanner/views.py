from django.http import JsonResponse

def task_list(request):
    return JsonResponse({'status': 'ok', 'data': []})