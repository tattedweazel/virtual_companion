import json


class SecretSquirrel():

	def __init__(self, file_location=''):

		self.source_file = file_location + "secrets.json"
		self.stash = self.load_secrets_file()


	def load_secrets_file(self):
		stash = []
		with open(self.source_file, 'r') as raw_stash:
			return json.load(raw_stash)