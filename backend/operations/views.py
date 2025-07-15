# operations/views.py
from django.http import JsonResponse

def operation_history(request):
    return JsonResponse({'status': 'ok', 'history': []})