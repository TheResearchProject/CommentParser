from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def available_databases(request):
    return JsonResponse({'databases': settings.AVAILABLE_DATABASES})

def index(request):
    return render(request, 'index.html')