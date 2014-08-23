#Read and Write Endpoints for Mypanel API

from django.db import connection
from mypanel_app.models import Event
import json
from dateutil import parser

def extract_params(request):
        """
        Utility function to parse out query params from a django request

        """
        # Parse out the request parameters
        request_params = request.GET if request.GET else request.POST

        # Return dictionary with request params
        request_dict = request_params.dict()

        return request_dict


class Import(object):
    """
        Import Class with methods for insert and import Endpoints
        Insert method deals with data that 
        Both methods return either a 0 or a 1
    """

    def __init__(self, req):
        self.request = req

    def insert(self):
        request_dict = extract_params(self.request)

        # Strip the double quotes and format as JSON  || If the data can't be formatted as JSON, return 0
        try: 
            dict_to_json = json.loads(request_dict['data'].replace("'", "\""))
        except ValueError:
            return 0

        # Create an Event Object with the request dictionary
        event_object = Event(name=dict_to_json.get('event'), time=dict_to_json.get('time').replace('T',' ').split('.')[0])
        event_object.save()

        return 1


class Query(object):
    """
        Query Class returns SQL data for a client Query
    """

    def __init__(self, req):
        self.request = req

    def extract_params(self,request):
        """
        Utility function to parse out query params from a django request

        """
        # Parse out the request parameters
        request_params = request.GET if request.GET else request.POST
        print request_params
        # Return dictionary with request params
        request_dict = request_params.dict()
        return request_dict


    def read(self):
        query = None 

        # grab request parameters
        request_dict = self.extract_params(self.request)
        from_date = request_dict.get('from_date')
        to_date = request_dict.get('to_date')
        event = request_dict.get('events')
        
        if from_date and to_date:
            newfrom = parser.parse(from_date)
            newto = parser.parse(to_date)
            print type(newfrom), type(newto)
            query = Event.objects.filter(time__gt=newfrom).filter(time__lt=newto)

        ## Now Query MySQL with date range, events, etc...

        if not query: query  = Event.objects.all()

        ## A specific event query
        
        if event and event.lower() != 'all': 
            q = query.filter(name=event).values()
            return self.format_data(q)

        data = self.format_data(query.values())

        return data

    def format_data(self, event_list):
        """
            Take a list of events and return a formatted list where the values are summed by day
        """
        event_dict = {}

        for val in event_list:
            pass
        return event_list

        """

        events = []
        event_dct = {} 
        for val in event_list:
            if event_dct.get(val['name']):
                event_dct[val['name']]['date']
        """
