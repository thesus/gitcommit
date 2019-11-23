import requests

class RandomMessage():
	def __self__(self):
		response = requests.get('http://whatthecommit.com/index.txt')
		return response.content.decode("utf-8")
