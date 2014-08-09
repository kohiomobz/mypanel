#Read and Write Endpoints for Mypanel API

from django.db import connection
from mypanel_app.models import Event
import json

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

		# Return dictionary with request params
		request_dict = request_params.dict()

		return request_dict


	def read(self):
		# grab request parameters
		request_dict = self.extract_params(self.request)
		# format as JSON
		#dict_to_json = json.loads(request_dict['data'].replace("'", "\""))

		## Now Query MySQL with date range, events, etc...
		query = Event.objects.all()

		return query
