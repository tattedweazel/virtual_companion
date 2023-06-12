from components.chat_gpt_llm import ChatGptLlm as LLM
from components.comment_summarizer_prompt import CommentSummarizerPrompt as CSP


class CommentSummarizer():

    def __init__(self) -> None:
        self._model='gpt-3.5-turbo'


    def get_summary(self, raw_text) -> str:
        prompt_template = CSP(raw_text=raw_text)
        llm = LLM(model=self._model, temperature=0.1)
        return llm.query(prompt=prompt_template.output())