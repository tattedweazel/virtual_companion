from components.chat_gpt_llm import ChatGptLlm as LLM
from components.cli_interface import CliInterface
from components.conversation_history import ConversationHistory
from components.multi_modal_prompt import MultiModalPrompt as MMP
from components.summarizer import Summarizer
from components.vector_manager import VectorManager


class ComponentConversation():

    def __init__(self) -> None:
        self.interface = CliInterface()
        self.conversation_history = ConversationHistory()
        self.summarizer = Summarizer()
        self.vector_manager = VectorManager()
        self.history_k = 2
        self.model = 'gpt-3.5-turbo'
        self.companion_name = 'Mel'

    
    def _summarize_docs(self, docs) -> str:
        return self.summarizer.get_summary(docs)


    def _exit_check(self, user_input) -> bool:
        if user_input.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
            return True
        return False

    
    def _conversation_loop(self) -> None:
        user_label = self.interface.get_user_label()
        user_input = self.interface.get_user_input()
        while not self._exit_check(user_input):
            formatted_input = user_label + user_input
            input_vectors = self.vector_manager.convert_to_vector(user_input)
            relevant_docs = self.vector_manager.perform_similarity_search(input_vectors)
            background = self._summarize_docs(relevant_docs)
            context = self.summarizer.get_summary(self.conversation_history.summary_export())
            recent_exchanges = self.conversation_history.k_latest(self.history_k)
            prompt_template = MMP(
                                background=background, 
                                context=context, 
                                recent_exchanges=recent_exchanges,
                                user_label=self.interface.get_user_name(),
                                user_input=user_input,
                                ai_label=self.companion_name
                                )
            llm = LLM(model=self.model, prompt=prompt_template.output(), name=self.companion_name)
            response = llm.query()
            input_resopnse_vector = self.vector_manager.convert_to_vector( formatted_input + "\n" + response )
            self.vector_manager.store(input_resopnse_vector)
            self.conversation_history.add_exchange(user_input = user_input, response=response)
            self.interface.return_response(response)
            user_input = self.interface.get_user_input()
        self.conversation_history.save()


    def start(self) -> None:
        self._conversation_loop()
