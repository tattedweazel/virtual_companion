


class MultiModalPrompt():

    def __init__(self, background=None, context=None, recent_exchanges=None, user_label=None, user_input=None, ai_label=None) -> None:
        self.background = background
        self.context = context
        self.recent_exchanges = recent_exchanges
        self.user_label = user_label
        self.user_input = user_input
        self.ai_label = ai_label

    
    def output(self):
        preamble = "This is the template boilerplate"
        background = "Background Information:\n" + self.background
        context = "Context:\n" + self.context
        recent_exchanges = "Recent Exchanges:\n" + self.recent_exchanges
        return f"{preamble}\n\n{background}\n\n{context}\n\n{recent_exchanges}\n{self.user_input}\n{self.ai_label}:"