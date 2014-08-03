from django.http import HttpResponse
from django.shortcuts import render_to_response
from api.api import Import

def hello(request):
    return HttpResponse("Hello World")

def index(request):
	return render_to_response('index.html', {})

def track(request):
	f = Import(request)
	return HttpResponse(f.insert())