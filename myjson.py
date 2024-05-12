import json

class MyJson:
	def __init__(self, maps):
		pass
	@classmethod
	def load_json(cls, path):
		'''
		Loads data from .json file and converts it into python dictionary
		'''
		with open(path, "r", encoding='utf-8') as f:
			data = json.loads(f.read())
			return data

	@classmethod
	def save_json(cls, path, data):
		with open(path, 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=2, ensure_ascii=False)

