from components.chat_gpt_llm import ChatGptLlm as LLM
from components.summarizer_prompt import SummarizerPrompt as SP


class Summarizer():

    def __init__(self) -> None:
        self._model='gpt-3.5-turbo'


    def get_summary(self, raw_text) -> str:
        prompt_template = SP(raw_text=raw_text)
        llm = LLM(model=self._model)
        return llm.query(prompt=prompt_template.output())