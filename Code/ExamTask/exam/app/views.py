from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,JsonResponse
# Create your views here.


def home(request):
    return render(request,"home.html")