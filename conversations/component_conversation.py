from base.exchange import Exchange
from components.chat_gpt_llm import ChatGptLlm as LLM
from components.cli_interface import CliInterface
from components.conversation_history import ConversationHistory
from components.multi_modal_prompt import MultiModalPrompt as MMP
from components.summarizer import Summarizer
from components.vector_manager import VectorManager
from tools.token_counter import TokenCounter


class ComponentConversation():

    def __init__(self, verbose=False) -> None:
        self._interface = CliInterface()                                # The interface we're communicating through
        self._conversation_history = ConversationHistory()              # List of all Exchange objects, constitutes our history
        self._summarizer = Summarizer()                                 # LLM to support summarization of strings
        self._vector_manager = VectorManager()                          # Manager for our vectorstore
        self._token_counter = TokenCounter()                            # Tool to count number of tokens in a string
        self._history_k = 2                                             # How many recent exchanges to include in the context window
        self._model = 'gpt-3.5-turbo'                                   # The main LLM model handling the conversation
        self._companion_name = self._interface.get_companion_name()     # The name of the companion we'll be working with
        self.verbose = verbose                                          # Determines if the passed prompt template is displayed, along with token count


    def _exit_check(self, user_input) -> bool:
        """ Check our user input for a direct match against any "exit" words and return true if found
        param: user_input   the user input
        return: bool        True if match found
        """
        if user_input.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
            return True
        return False
    

    def _schema_check(self) -> bool:
        """ Ensure a schema is available for the currently chosen companion
        This checks the current schema for an existing class that matches the current companion
        If one is not found, it is created
        return: bool    Always True for now
        """
        for data_class in self._vector_manager.get_schema()['classes']:
            if self._companion_name == data_class['class']:
                return True
        self._vector_manager.create_class_obj(class_name=self._companion_name)
        return True
    

    def _get_relevant_docs(self, user_input) -> str:
        """ Query vector store using similarity search based on user input
        param: user_input   the user input
        return: str         a string containing all relevant documents
        """
        return self._vector_manager.perform_similarity_search(
                input_string=user_input, 
                class_name=self._companion_name,
                fields=['content']
            )
    

    def _get_background(self, relevant_docs) -> str:
        """ Helper method to get our background based on the summary of our relevant docs
        param: relevant_docs    previously retrieved relevant docs string
        return: str             string of summary if relevant docs were passed, empty string if not
        """
        if relevant_docs:
            return self._summarizer.get_summary("\n".join(relevant_docs))
        return ""
    

    def _get_context(self, history) -> str:
        """ Helper method to get our context based on the summary of our conversation history
        param: history      string of conversation history
        return: str         string of summary if history was passed, empty string if not
        """
        if history:
            return self._summarizer.get_summary(history)
        return ""
    

    def _handle_exchange(self, user_input, response) -> None:
        """ Create a new Exchange based on user input and response, then store it in our history and vectorstore
        param: user_input   the user input
        param: response     the response to that input
        return: None
        """
        exchange = self._create_new_exchange(user_input, response)
        self._add_exchange_to_conversation_history(exchange)
        self._add_latest_exchange_to_vectorstore()
    

    def _create_new_exchange(self, user_input, response) -> Exchange:
        """ Create and return a new Exchange object from a given user_input and response
        param: user_input   the user input
        param: response     the response to that input
        return: Exchange    the resulting Exchange object
        """
        return Exchange(user_input = user_input, response=response)


    def _add_exchange_to_conversation_history(self, exchange) -> None:
        """ Adds Exchange object to our conversation history
        param: exchange     Exchange object to be stored
        return: None
        """
        self._conversation_history.add_exchange(exchange)


    def _add_latest_exchange_to_vectorstore(self) -> None:
        """ Add the latest exchenage to the vectorstore
        return: None
        """
        data_obj={"content": self._conversation_history.k_latest(k=1)}
        self._vector_manager.store(
            class_name=self._companion_name, 
            data_objs=[data_obj]
        )


    def _display_verbose(self, prompt_template) -> None:
        print("********************************************************")
        print(prompt_template.output())
        print("********************************************************")
        print("Token Count:")
        print(self._token_counter.get_token_count(prompt_template.output()))
        print("********************************************************")

    
    def _conversation_loop(self) -> None:
        user_input = self._interface.get_user_input()
        # with each loop, check for an input matching an exit word
        while not self._exit_check(user_input):
            # Start by getting our relevant docs, using a similarity search of our vector store based on our user_input
            relevant_docs = self._get_relevant_docs(user_input)
            
            # Now we summarize those docs to get our "background"
            background = self._get_background(relevant_docs)

            # Our "context" of our conversation is based on a summarization of our conversation history so far
            history = self._conversation_history.summary_export()
            context = self._get_context(history)

            # Our "recent exchanges" will literally be our k-latest messages from our conversation history
            recent_exchanges = self._conversation_history.k_latest(self._history_k)
            
            # Now we get our template and pass it the requisites
            prompt_template = MMP(
                background=background, 
                context=context, 
                recent_exchanges=recent_exchanges,
                user_name=self._interface.get_user_name(),
                user_input=user_input,
                ai_name=self._companion_name
            )

            # Moar text for debugging purposes
            if self.verbose:
                self._display_verbose(prompt_template)

            # Instantiate our LLM of choice and pass our prompt template's now filled-in output as our query and get our response
            llm = LLM(model=self._model)
            response = llm.query(prompt_template.output())

            # create a new exchange object representing this query/response exchange, and save it to our history and vectorstore
            self._handle_exchange(user_input, response)

            # return our response to the interface and solicit our next input
            self._interface.return_response(response)
            user_input = self._interface.get_user_input()
        
        # Now that the conversation has ended, let's save it for science.
        self._conversation_history.save()


    def start(self) -> None:
        self._schema_check()
        self._conversation_loop()
