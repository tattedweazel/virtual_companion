import json
from components.comment_summarizer import CommentSummarizer
from components.summary_condenser import SummaryCondenser
from tools.token_counter import TokenCounter



class CommentAnalyzer():

    def __init__(self, source_file) -> None:
        self._raw_comments = self._load_comments(source_file)
        self._flagged_comments = []
        self._batches = []
        self._summaries = []
        self._final_summary = ""
        self._token_counter = TokenCounter()
        self._summarizer = CommentSummarizer()
        self._summary_condeser = SummaryCondenser()
        self.BATCH_TOKEN_LIMIT = 2000


    def _load_comments(self, load_from) -> list:
        comments = []
        with open(load_from, 'r') as f:
            comments = json.loads(f.read())
        return comments
    

    def _get_projected_token_count(self, part, total) -> int:
        return self._token_counter.get_token_count(part) + self._token_counter.get_token_count(total)
    

    def _create_batches(self) -> None:
        batches = []
        batch = ""
        for entry in self._raw_comments:
            # First, make sure the comment itself doesn't bust our token limit - if it does, flag it and move on
            if self._get_projected_token_count(entry['comment'], "") > self.BATCH_TOKEN_LIMIT:
                self._flagged_comments.append({"comment": entry['comment'], "reason": "over token limit"})
                continue
            # Now, let's make sure that adding this comment to our batch doesn't bust the token limit
            if self._get_projected_token_count(entry['comment'], batch) > self.BATCH_TOKEN_LIMIT:
                # If it does, let's add the current batch to the batches list, create a new batch, and add this comment to it
                batches.append(batch)
                batch = f"comment: {entry['comment']}" + "\n"
            else:
                # If it does not, just add it to the current batch
                batch += f"comment: {entry['comment']}" + "\n"
        batches.append(batch)
        self.batches = batches


    def _create_batch_summaries(self) -> None:
        for batch in self.batches:
            self._summaries.append(self._summarizer.get_summary(batch))


    def _combine_summaries(self) -> None:
        running_summary = ""
        for summary in self._summaries:
            if running_summary == "":
                running_summary += summary + "\n\n"
                continue
            running_summary += summary + "\n\n"
            running_summary = self._summary_condeser.get_summary(running_summary) + "\n"
        self._final_summary = running_summary

    

    def start(self) -> None:
        self._create_batches()
        self._create_batch_summaries()
        self._combine_summaries()
