import json
import weaviate
from tools.secret_squirrel import SecretSquirrel


class VectorManager():

    def __init__(self) -> None:
        self._creds = SecretSquirrel().stash
        auth_config = weaviate.AuthApiKey(api_key=self._creds['weaviate_api_key'])
        self._client = weaviate.Client(
            url=self._creds['weaviate_url'],
            auth_client_secret=auth_config,
            additional_headers={
                'X-OpenAI-API-Key': self._creds['open_ai_api_key']
            }
        )
        self._BATCH_SIZE=50
        self._DYNAMIC=False


    def _jdump(self, _in) -> str:
        return json.dumps(_in, indent=4)


    def get_schema(self) -> str:
        return self._jdump(self._client.schema.get())
    

    def clear_schema(self) -> None:
        self._client.schema.delete_all()


    def create_class_obj(self, class_name) -> None:
        self._client.schema.create_class({
            "class": class_name,
            "vectorizer": "text2vec-openai"
        })
        return self._jdump(self._client.schema.get())
    

    def perform_similarity_search(self, input_string, class_name="", fields=[], limit=5) -> str:
        results = self._jdump(self._client.query.get(
                class_name, fields
            ).with_near_text(
                {"concepts": [input_string]}
            ).with_limit(limit).do()
        )
        docs = []
        j_data = json.loads(results)
        for record in j_data['data']['Get'][f"{class_name}"]:
            docs.append(record['content'])
        return docs


    def store(self, class_name, data_objs=[]) -> str:
        with self._client.batch as batch:
            batch.batch_size=self._BATCH_SIZE
            batch.dynamic=self._DYNAMIC
            for data_obj in data_objs:
                batch.add_data_object(
                    data_obj,
                    class_name
                )
        return self._jdump(self._client.query.aggregate(class_name).with_meta_count().do())