import tiktoken


class TokenCounter():
		
	def __init__(self):
		self.encoding_type = 'gpt2'
		self.tt = tiktoken


	def encode(self, input_string):
		enc = self.tt.get_encoding(self.encoding_type)
		return enc.encode(input_string)


	def get_token_count(self, input_string):
		encoding = self.encode(input_string)
		num_tokens = len(encoding)
		return num_tokens