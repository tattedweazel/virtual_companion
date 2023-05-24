from base.exchange import Exchange
from components.chat_gpt_llm import ChatGptLlm as LLM
from components.cli_interface import CliInterface
from components.conversation_history import ConversationHistory
from components.multi_modal_prompt import MultiModalPrompt as MMP
from components.summarizer import Summarizer
from components.vector_manager import VectorManager
from tools.token_counter import TokenCounter


class ComponentConversation():

    def __init__(self) -> None:
        self._interface = CliInterface()
        self._conversation_history = ConversationHistory()
        self._summarizer = Summarizer()
        self._vector_manager = VectorManager()
        self._token_counter = TokenCounter()
        self._history_k = 2
        self._model = 'gpt-3.5-turbo'
        self._companion_name = self._interface.get_companion_name()


    def _exit_check(self, user_input) -> bool:
        if user_input.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
            return True
        return False
    

    def _schema_check(self) -> bool:
        for data_class in self._vector_manager.get_schema()['classes']:
            if self._companion_name == data_class['class']:
                return True
        self._vector_manager.create_class_obj(class_name=self._companion_name)
        return True

    
    def _conversation_loop(self) -> None:
        user_input = self._interface.get_user_input()
        while not self._exit_check(user_input):
            relevant_docs = self._vector_manager.perform_similarity_search(
                input_string=user_input, 
                class_name=self._companion_name,
                fields=['content']
            )
            if relevant_docs:
                background = self._summarizer.get_summary("\n".join(relevant_docs))
            else:
                background = ""
            history = self._conversation_history.summary_export()
            if history:
                context = self._summarizer.get_summary(history)
            else:
                context = ""
            recent_exchanges = self._conversation_history.k_latest(self._history_k)
            prompt_template = MMP(
                                background=background, 
                                context=context, 
                                recent_exchanges=recent_exchanges,
                                user_name=self._interface.get_user_name(),
                                user_input=user_input,
                                ai_name=self._companion_name
            )
            print("********************************************************")
            print(prompt_template.output())
            print("********************************************************")
            print("Token Count:")
            print(self._token_counter.get_token_count(prompt_template.output()))
            print("********************************************************")
            llm = LLM(model=self._model)
            response = llm.query(prompt_template.output())
            exchange = Exchange(user_input = user_input, response=response)
            self._conversation_history.add_exchange(exchange)
            data_obj={"content": self._conversation_history.k_latest(k=1)}
            self._vector_manager.store(
                class_name=self._companion_name, 
                data_objs=[data_obj]
            )
            self._interface.return_response(response)
            user_input = self._interface.get_user_input()
        self._conversation_history.save()


    def start(self) -> None:
        self._schema_check()
        self._conversation_loop()
