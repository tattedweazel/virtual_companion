


class ChatGptLlm():

    def __init__(self, model=None, prompt=None, name="Virtual Companion") -> None:
        self.model = model
        self.prompt = prompt
        self.name = name


    def query(self) -> str:
        return f"LLM Response to: {self.prompt}"