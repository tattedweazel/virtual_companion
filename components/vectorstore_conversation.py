import json
from tools.secret_squirrel import SecretSquirrel
from connectors.weaviate_connector import WeaviateConnector
from datetime import datetime
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Weaviate


class VectorstoreConversation():

    def __init__(self, companion, first_time = False, clear_store=False):
        self.creds = SecretSquirrel().stash
        self.companion = companion
        self.first_time = first_time
        self.clear_store = clear_store
        self.stop = False
        self.message_log = []
        
        prompt = PromptTemplate(
            input_variables = self.companion.input_variables(),
            template = self.companion.prompt_template()
        )

        client = WeaviateConnector().get_client()
        
        if self.clear_store:
            client.schema.delete_all()
        
        client.schema.get()
        
        if self.first_time:
            schema = {
                "classes": [
                    {
                        "class": "MelParagraph",
                        "description": "A written paragraph",
                        "vectorizer": "text2vec-openai",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "model": "ada",
                                "modelVersion": "002",
                                "type": "text"
                            }
                        },
                        "properties": [
                            {
                                "dataType": ["text"],
                                "description": "The content of the paragraph",
                                "moduleConfig": {
                                    "text2vec-openai": {
                                        "skip": False,
                                        "vectorizePropertyName": False
                                    }
                                },
                                "name": "content",
                            },
                        ],
                    },
                ]
            }

            client.schema.create(schema)
        vectorstore = Weaviate(client, "MelParagraph", "content")
        retriever = vectorstore.as_retriever(search_kwargs=dict(k=8))
        memory = VectorStoreRetrieverMemory(retriever=retriever)
        self.conversation_chain = LLMChain(
            llm = ChatOpenAI(
                model_name='gpt-3.5-turbo',
                openai_api_key=self.creds['open_ai_api_key'],
                temperature=0.6
            ),
            prompt = prompt,
            memory=memory,
            verbose=True
        )


    def get_user_prompt(self):
        print("\n")
        prompt =  input("-> ")
        print("\n")
        return prompt
    

    def store_conversation(self):
        with open(f"conversations/{datetime.strftime(datetime.now(),'%Y%m%d_%H_%M_%S')}.json", "w") as outfile:
            json.dump(self.message_log, outfile, indent=4)

        print("Conversation successfully stored")


    def end_conversation(self):
        msg = f"Goodbye."
        self.companion.say(msg)
        self.store_conversation()
        exit()


    def advance_conversation(self, prompt):
        self.message_log.append({
            "sender": self.companion.human_name,
            "content": prompt
        })
        response = self.conversation_chain.predict_and_parse(human_input=prompt)
        self.message_log.append({
            "sender": self.companion.name,
            "content": response
        })
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