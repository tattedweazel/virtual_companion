from base.message import Message


class Conversation():

	def __init__(self):
		self.messages = []

	def __repr__(self):
		return f"Conversation: {len(self.messages)} messages"


	def add_message(self, message:Message):
		self.messages.append(message.serialize_message())