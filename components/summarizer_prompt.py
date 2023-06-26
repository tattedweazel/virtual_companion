


class SummarizerPrompt():

    def __init__(self, raw_text) -> None:
        self.raw_text = raw_text

    
    def output(self) -> str:
        preamble = "You are a highly advanced Summarization AI. You take in a string of text and return a high-quality summary that is succinct but captures the overall meaning, intent, and context of the information passed to you. Be sure to maintain specific details if they are relevant. Your output will be used to make decisions on the course of the content, so be sure to provide actionable information in your summary. Your summarization must be limited to no more than 900 tokens in length."
        context = "Text to Summarize:\n" + self.raw_text
        return f"{preamble}\n\n{context}\n\nSummary: "