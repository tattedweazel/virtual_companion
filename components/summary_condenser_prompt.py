



class SummaryCondenserPrompt():

    def __init__(self, raw_text) -> None:
        self.raw_text = raw_text

    
    def output(self) -> str:
        preamble = "You are a highly advanced Summary Condenser AI. You take in multiple summaries and combine them into one summary while ensuring to keep as much relevant information as possible. Be sure to include specific details if they help provide insight. Your output be a maximum of 1200 tokens and in the format:\n\nWhat Viewers Liked: \nWhat Viewers Disliked:  \nInsights: \n\n"
        context = "Summaries to Condense:\n" + self.raw_text
        return f"{preamble}\n\n{context}\n\nCondensed Summary: "