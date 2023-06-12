from components.chat_gpt_llm import ChatGptLlm as LLM
from components.summary_condenser_prompt import SummaryCondenserPrompt as SCP
from tools.token_counter import TokenCounter


class SummaryCondenser():

    def __init__(self) -> None:
        self._model='gpt-3.5-turbo'
        self._token_counter = TokenCounter()


    def get_summary(self, raw_text) -> str:
        prompt_template = SCP(raw_text=raw_text)
        llm = LLM(model=self._model, temperature=0.0)
        response = llm.query(prompt=prompt_template.output())
        return response
