from django.http import HttpResponse
from django.shortcuts import render_to_response
from api.api import Import, Query
import json

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
	
	"""
	    Event.objects.all().values() returns a list but that list can't be formatted as valid Json
	"""
	query_to_json = []
	for val in Q.read():
	    query_to_json.append(val)
	
	response['Access-Control-Allow-Origin'] = '*'
	response.write(json.dumps(query_to_json))
	return response
