



class SummaryCondenserPrompt():

    def __init__(self, raw_text) -> None:
        self.raw_text = raw_text

    
    def output(self) -> str:
        preamble = "You are a highly advanced Summary Condenser AI. You take in multiple summaries and combine them into one summary while ensuring to keep as much relevant information as possible. Be sure to include justification for any statements. Your output be a maximum of 1000 tokens and in the format:\nSentiment: [the condensed sentiments]\nEmotion: [the condense emotions]\nInsights: [the condendsed insights]\n\n"
        context = "Summaries to Condense:\n" + self.raw_text
        return f"{preamble}\n\n{context}\n\nCondensed Summary: "