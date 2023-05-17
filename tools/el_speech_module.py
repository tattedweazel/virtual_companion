import elevenlabs
from tools.secret_squirrel import SecretSquirrel


class ELSpeechModule():

	def __init__(self, el_model_id):
		self.creds = SecretSquirrel().stash
		self.el_model_id = el_model_id
		elevenlabs.set_api_key(self.creds['eleven_labs_api_key'])


	def say(self, statement):
		result = self.handle_generation(statement)
		self.handle_play(result)


	def handle_generation(self, statement):
		return elevenlabs.generate(
			text=statement,
			voice=self.el_model_id,
			model="eleven_monolingual_v1",
			stream=False
		)
	

	def handle_play(self, generatation_result):
		elevenlabs.play(
			audio=generatation_result,
			notebook=False
		)
