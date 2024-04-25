import json
import os

import pymongo
from bson.json_util import dumps
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class MongoDBClient:
    def __init__(self):
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = int(os.getenv("MONGO_PORT", 27017))
        self.db_name = os.getenv("MONGO_DB", "test")
        self.collection_name = os.getenv(
            "MONGO_COLLECTION", "default_collection"
        )  # noqa
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def test_insert_fun(self):
        try:
            test_data = [{"name": "Mary", "age": 30}]
            result = self.collection.insert_many(test_data)
            return {
                "status": 200,
                "message": f"Inserted {len(result.inserted_ids)} documents",
            }
        except pymongo.errors.WriteError as e:
            raise HTTPException(
                status_code=500, detail=f"Error when inserting data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Other error when inserting data: {str(e)}",
            )

    async def test_select_fun(self):
        try:
            data = [json.loads(dumps(doc)) for doc in self.collection.find()]
            return {"status": 200, "data": data}
        except pymongo.errors.ReadError as e:
            raise HTTPException(
                status_code=500, detail=f"Error when selecting data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Other error when selecting data: {str(e)}",
            )

    async def test_drop_fun(self):
        try:
            if self.collection_name in self.db.list_collection_names():
                self.db.drop_collection(self.collection_name)
                message = "Success to delete collection"
            else:
                message = "Collection does not exist"
            return {"status": 200, "message": message}
        except pymongo.errors.PyMongoError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error when dropping collection: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Other error when dropping collection: {str(e)}",
            )
