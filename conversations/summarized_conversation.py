import json
from components.secret_squirrel import SecretSquirrel
from datetime import datetime
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory


class SummarizedConversation():

    def __init__(self, companion):
        self.creds = SecretSquirrel().stash
        self.companion = companion
        self.stop = False
        
        prompt = PromptTemplate(
            input_variables = self.companion.input_variables(),
            template = self.companion.prompt_template()
        )

        self.conversation_chain = LLMChain(
            llm = ChatOpenAI(
                model_name='gpt-3.5-turbo',
                openai_api_key=self.creds['open_ai_api_key'],
                temperature=0.5
            ),
            prompt = prompt,
            memory=ConversationSummaryMemory(
                llm=ChatOpenAI(
                    model_name='gpt-3.5-turbo',
                    openai_api_key=self.creds['open_ai_api_key'],
                    temperature=0.2
                ),
                ai_prefix=self.companion.name,
                human_prefix=self.companion.human_name
            ),
            verbose=True
        )


    def get_user_prompt(self):
        print("\n")
        prompt =  input("-> ")
        print("\n")
        return prompt
    

    def store_conversation(self):
        messages = []
        for message in self.conversation_chain.memory.chat_memory.messages:
            msg_type = str(type(message)).split('.')[-1].split("'>")[0]
            if msg_type == 'HumanMessage':
                sender = self.companion.human_name
            elif msg_type == 'AIMessage':
                sender = self.companion.name
            else:
                sender = 'System'
            messages.append({
                "sender": sender,
                "content": message.content
            })
        with open(f"logs/{datetime.strftime(datetime.now(),'%Y%m%d_%H_%M_%S')}.json", "w") as outfile:
            json.dump(messages, outfile, indent=4)

        print("Conversation successfully stored")


    def end_conversation(self):
        msg = f"Goodbye."
        self.companion.say(msg)
        self.store_conversation()
        exit()


    def advance_conversation(self, prompt):
        response = self.conversation_chain.predict_and_parse(human_input=prompt)
        return response


    def conversation_loop(self):
        while not self.stop:
            prompt = self.get_user_prompt()

            if prompt.lower() in ['stop', 'stop()', 'exit', 'exit()', 'quit', 'quit()', 'end', 'end()']:
                self.stop = True
                break

            response = self.advance_conversation(prompt=prompt)
            self.companion.say(response)

        self.end_conversation()


    def start(self):
        self.conversation_loop()