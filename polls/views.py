from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'polls/index.html')

def about(request):
    return render(request,'polls/about.html')

def news(request):
    return render(request,'polls/news.html')

def privacy(request):
    return render(request,'polls/privacy.html')

def question(request):
    return render(request,'polls/question.html')