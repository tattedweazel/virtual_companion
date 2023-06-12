



class CommentSummarizerPrompt():

    def __init__(self, raw_text) -> None:
        self.raw_text = raw_text

    
    def output(self):
        preamble = "You are a highly advanced YouTube Comment Summarization AI. You take in a string of comments and return a high-quality summary that is succinct but captures the overall sentiment, emotion, and actionable insights from the comments passed to you. Your summarization must be limited to no more than 1000 tokens in length and provided in the following format:\n\nSentiment: positive or negative, and reaons why\nEmotion: a summary of the emotions expressed by viewers, with relevant examples\nInsights: a summary of insights that could be helpful to improve the video that were provided by viewers\n\n"
        context = "Comments to Summarize:\n" + self.raw_text
        return f"{preamble}\n\n{context}\n\nSummary: "