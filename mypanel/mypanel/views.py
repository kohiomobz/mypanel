from django.http import HttpResponse
from django.shortcuts import render_to_response
from api.api import Import, Query
import json
import pdb

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

    ## Adding pdb module for tracing python error
    #pdb.set_trace()

    Q = Query(request)
    response = HttpResponse()
    """
        Event.objects.all().values() returns a list but that list can't be formatted as valid Json
    """
    query_to_json = Q.read()

    print query_to_json, 'json'
    print json.dumps(query_to_json), 'json response'
    
    response['Access-Control-Allow-Origin'] = '*'
    response.write(json.dumps(query_to_json))
    print response, 'response'

    return response
