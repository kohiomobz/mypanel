#Read and Write Endpoints for Mypanel API

from django.db import connection
from mypanel_app.models import Event
import json
from dateutil import parser
from datetime import datetime, timedelta, date
from collections import defaultdict
import pdb

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
        # Parse out the request parametersZ
        request_params = request.GET if request.GET else request.POST
        # Return dictionary with request params
        request_dict = request_params.dict()
        return request_dict


    def read(self):
        query = None

        # Grab Request Parameters

        request_dict = self.extract_params(self.request)
        from_date = request_dict.get('from_date')
        to_date = request_dict.get('to_date')
        event = request_dict.get('events')
        date_range = None

        if from_date and to_date:
            new_from = parser.parse(from_date)
            new_to = parser.parse(to_date)
            
            ## Now Query MySQL with date range, events, etc...
            query = Event.objects.filter(time__gt=new_from).filter(time__lt=new_to)
            date_range = self.set_date_range(from_date,to_date)

        if not query: query  = Event.objects.all()

        ## A specific event query

        if event and event.lower() != 'all': 
            q = query.filter(name=event).values()

            return self.format_data(q, date_range)
    
        data = self.format_data(query.values(), date_range)

        return {'data':data, 'values':date_range}

    def set_date_range(self, from_date, to_date):
        """ 
            If date range is greater than 30 days, use months instead if its greater than 365 days, use years
            If date range is smaller than 30 days, use a 30 day date range from the start of the from_date

        """
        #[int(from_date.split('-')[0])] + 
        start = [int(x) for x in from_date.split('-')]
        end = [int(x) for x in to_date.split('-')]

        datetime_start = date(start[0], start[1], start[2])
        datetime_end = date(end[0], end[1], end[2])

        diff = datetime_end - datetime_start
        
        # The number of days between your start date and end date
        number_of_days = diff.days
        date_list = []

        if number_of_days > 31:
            pass ## return months
        else:
            for val in range(number_of_days):
                new_date = datetime_start + timedelta(val)
                date_list.append(new_date.isoformat())

        return date_list

    def format_data(self, event_list, date_range):
        """
            Take a list of events and return a formatted list where the values are summed by day
            also remove all unicode values to avoid json errors
        """

        event_dict = defaultdict(list)
        values = []
        
        if not date_range or len(date_range) < 31:
            values = [0 for x in range(30)]


        for val in event_list:
            print val
            if not event_dict.get(val['name']):
                event_dict[val['name']] = values
                print date_range
                index = date_range.index(val['time'])
                print date_range
                event_dict[val['name']][index] +=1

            else:
                ## find the range element
                index = date_range[val['time']]
                event_dict[val['name']][index] += 1
        print event_dict
        return event_dict

        """



        """
