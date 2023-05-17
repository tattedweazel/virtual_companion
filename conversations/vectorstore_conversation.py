from base.cli_conversation import CliConversation
from connectors.weaviate_connector import WeaviateConnector
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Weaviate


class VectorstoreConversation(CliConversation):

    def __init__(self, companion, first_time = False, clear_store=False):
        super().__init__(companion)
        self.first_time = first_time
        self.clear_store = clear_store
        
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
