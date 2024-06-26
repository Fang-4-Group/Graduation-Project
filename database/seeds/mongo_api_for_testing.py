import json
import os

import pymongo
from bson.json_util import dumps
from dotenv import load_dotenv

load_dotenv()


class MongoDBClient:
    def __init__(self):
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = int(os.getenv("MONGO_PORT", 27017))
        self.db_name = os.getenv("MONGO_DB", "test_db")
        self.collection_name = os.getenv("MONGO_COLLECTION", "test_collection")  # noqa
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def test_insert_fun(self):
        try:
            test_data = [{"name": "Mary", "age": 30}]
            result = self.collection.insert_many(test_data)
            return {
                "message": f"Inserted {len(result.inserted_ids)} documents",
            }
        except Exception as e:
            return {
                "message": f"Error when inserting data: {str(e)}",
            }

    async def test_select_fun(self):
        try:
            data = [json.loads(dumps(doc)) for doc in self.collection.find()]
            return {"message": data}
        except Exception as e:
            return {
                "message": f"Error when selecting data: {str(e)}",
            }

    async def test_drop_fun(self):
        try:
            if self.collection_name in self.db.list_collection_names():
                self.db.drop_collection(self.collection_name)
                message = "Success to delete collection"
            else:
                message = "Collection does not exist"
            return {"message": message}
        except Exception as e:
            return {
                "message": f"Error when selecting data: {str(e)}",
            }
