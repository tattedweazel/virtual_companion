import json
from connectors.chat_gpt_connector import ChatGptConnector
from base.conversation import Conversation
from datetime import datetime
from base.message import Message
from components.token_counter import TokenCounter


class SimpleConversation():

    def __init__(self, companion):
        self.companion = companion
        self.conversation = Conversation()
        self.chat_gpt_connector = ChatGptConnector()
        self.stop = False


    def prime_model(self):
        msg = Message('system', self.companion.primer)
        self.conversation.add_message(msg)


    def get_user_prompt(self):
        print("\n")
        prompt =  input("-> ")
        return prompt
    

    def perform_interaction(self, prompt):
        print("\n\n")
        self.conversation.add_message(Message('user', prompt))
        return self.chat_gpt_connector.send_message(self.conversation)
    

    def store_conversation(self):
        with open(f"conversations/{datetime.strftime(datetime.now(),'%Y%m%d_%H_%M_%S')}.json", "w") as outfile:
            counter = TokenCounter()
            token_count = counter.get_token_count(json.dumps(self.conversation.messages))
            self.conversation.add_message(Message('total_tokens', token_count))
            json.dump(self.conversation.messages, outfile, indent=4)

        print("Conversation successfully stored")


    def end_conversation(self):
        msg = f"Goodbye."
        self.companion.say(msg)
        self.conversation.add_message(Message('assistant', msg))
        self.store_conversation()
        exit()


    def initiate_conversation(self):
        prompt = self.get_user_prompt()
        response = self.perform_interaction(prompt)
        self.conversation_loop(response)


    def conversation_loop(self, full_response):
        while not self.stop:
            success, response, error = full_response
            self.conversation.add_message(Message('assistant', response))
            self.companion.say(response)
            prompt = self.get_user_prompt()

            if prompt.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
                self.conversation.add_message(Message('system', 'User has ended the session'))
                self.stop = True
                break

            full_response = self.perform_interaction(prompt)
            success, response, error = full_response

            if not success:
                msg = f"I'm sorry, but I ran into a problem and we must end this conversation. Details: {response} - {error}"
                self.companion.say(msg)
                self.conversation.add_message(Message('assistant', msg))
                self.stop = True
        self.end_conversation()


    def start(self):
        self.prime_model()
        self.initiate_conversation()