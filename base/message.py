


class Message():
	
	def __init__(self, role, message):
		self.role = role
		self.content = message


	def __repr__(self):
		return f"{self.role}: {self.content}"

	def serialize_message(obj):
		if isinstance(obj, Message):
			return {"role": obj.role, "content": obj.content}
		return obj.__dict__