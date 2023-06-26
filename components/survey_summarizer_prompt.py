



class SurveySummarizerPrompt():

    def __init__(self, raw_text) -> None:
        self.raw_text = raw_text

    
    def output(self) -> str:
        preamble = "You are a highly advanced Survey Results Summarization AI. Your job is to take a list of comments from cancellation surveys and provide a summary of those comments. Be sure to include relevant details if they provide actionable insights that can help improve the product. Do not provide recommendations, and only provide summarization. Your summarization must be limited to no more than 1000 tokens in length and provided in the following format:\n\nReasons for cancellation: \nInsights: \n\n"
        context = "Comments to Summarize:\n" + self.raw_text
        return f"{preamble}\n\n{context}\n\nSummary: "