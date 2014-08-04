#Read and Write Endpoints for Mypanel API

from django.db import connection
from mypanel_app.models import Event
import json

class Import(object):
	"""
		Import Class with methods for insert and import Endpoints

		Insert method deals with data that 

		Both methods return either a 0 or a 1
	"""
	def __init__(self, req):
		self.request = req

	def insert(self):
		# Parse out the request parameters
		request_params = self.request.GET if self.request.GET else self.request.POST

		# Return dictionary with request params
		request_dict = request_params.dict()

		# Strip the double quotes and format as JSON  || If the data can't be formatted as JSON, return 0
		try: 
			dict_to_json = json.loads(request_dict['data'].replace("'", "\""))
		except ValueError:
			return 0

		# Create an Event Object with the request dictionary
		event_object = Event(name=dict_to_json.get('event'), time=dict_to_json.get('time'))
		event_object.save()

		return 1



class Export(object):
	def __init__(self, req):
		self.request = req

	def read(self):
		print self.request
