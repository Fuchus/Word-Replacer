import requests
import argparse

"""
This module is a library for a typical API application
There are different variables to set 
"""

class API(object):
	params = {}
	def __init__(self, url, api_key, **params):
		"""
		Init function of the API class
		Args:
			url (str): URL for the API to call
			xrequest (bool): Switch if x-request is needed
			api_key (str): API-key as a string
			**params (dict): More parameters for the class to parse in the URL
		Returns:
			API.object: Instance of the API class
		"""

		parser = argparse.ArgumentParser(description='API library that works with requests')
		parser.add_argument('text', nargs='*')
		args = parser.parse_args()

		self.__url = url
		self.__xrequest = xrequest
		self.__api_key = api_key
		self.__params = params

	def find_error(self, request):
		"""
		Find-error function that is used to check the json return dict for any error messages

		Args:
			request (request instance): Instance of the request class

		Returns:
			bool: True for success, False otherwise
		"""
		return 'message' or 'error' in request

	def getr(self):
		"""
		Get request function to build a URL and instantiate a request object with a json result set

		Returns:
			dict: content of the json-page decoded with the requests.object.json() function
		"""
		if self.__params:
			for key, value in self.params.iteritems():
				self.url += '?' + key + '=' + value
		if self.__api_key:
			xrequest = {'x-api-key': self.__api_key}
			r = requests.get(self.url, headers=xrequest, allow_redirects=False)
			r.raise_for_status()
			if r.status_code == 303: raise requests.exceptions.HTTPError
			else: return r.json()
		else:
			r = requests.get(self.url)# ,allow_redirects=False)
			self.find_status(r, 500)
			r.raise_for_status()
			#if r.status_code == 303: raise requests.exceptions.HTTPError
			return r.json()

	def find_status(self, request, status):
		"""
		Find status function that checks for a certain status in the requests.object.status_code int and raise a ValueError accordingly
		Args:
			request (requests object): Requests object
			status (int): Desired status to raise an exception for
		Raises:
			ValueError
		"""
		if request.status_code == status:
			raise ValueError
