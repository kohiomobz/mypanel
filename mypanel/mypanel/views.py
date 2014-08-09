from django.http import HttpResponse
from django.shortcuts import render_to_response
from api.api import Import, Query

def hello(request):
	return HttpResponse(1)

def index(request):
	return render_to_response('index.html', {})

def track(request):
	f = Import(request)

	# Adding Access Control header to prevent CORS Errors
	response = HttpResponse()
	response.write(f.insert())
	response['Access-Control-Allow-Origin'] = '*'
	return response

def query(request):
	Q = Query(request)
	response = HttpResponse()
	response['Access-Control-Allow-Origin'] = '*'
	response['data'] = Q.read()
	print response['data']

	return response
