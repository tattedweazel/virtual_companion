


class MultiModalPrompt():

    def __init__(self, background=None, context=None, recent_exchanges=None, user_name=None, user_input=None, ai_name=None) -> None:
        self.background = background
        self.context = context
        self.recent_exchanges = recent_exchanges
        self.user_name = user_name
        self.user_input = user_input
        self.ai_name = ai_name

    
    def output(self):
        preamble = f"You are an advanced AI who is pretending to be a human named {self.ai_name}. Below, is a conversation between you and someone named {self.user_name}. Context for the conversation, background information relevant to the conversation, and the most recent exchanges from the conversation are provided below. Please use those items to continue this coversation by providing a response."
        context = "Context:\n" + self.context
        background = "Background Information:\n" + self.background
        recent_exchanges = "Recent Exchanges:\n" + self.recent_exchanges
        return f"{preamble}\n\n{background}\n\n{context}\n\n{recent_exchanges}\n\nInput: {self.user_input}\nResponse:"