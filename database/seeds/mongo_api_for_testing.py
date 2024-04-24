# from fastapi import APIRouter, HTTPException
import json

import pymongo
from bson.json_util import dumps

# MongoDB连接信息
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
MONGO_DB = "test_db"
MONGO_COLLECTION = "test_collection"

# MongoDB连接实例
client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


async def test_insert_fun():
    try:
        # 插入测试数据
        test_data = [
            {"name": "Mary", "age": 30},
        ]
        result = collection.insert_many(test_data)
        return {
            "status": 200,
            "message": f"Inserted {len(result.inserted_ids)} documents",
        }
    except pymongo.error.WriteError as e:
        return {
            "status": 500,
            "message": f"Error when inserting data: {str(e)}",
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f"Other error when inserting data: {str(e)}",
        }


async def test_select_fun():
    try:
        # 查詢數據
        data = [json.loads(dumps(doc)) for doc in collection.find()]
        # return data
        return {"status": 200, "data": data}
    except pymongo.error.ReadError as e:
        return {
            "status": 500,
            "message": f"Error when selecting data: {str(e)}",
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f"Other error when selecting data: {str(e)}",
        }


async def test_drop_fun():
    try:
        if MONGO_COLLECTION in db.list_collection_names():
            db.drop_collection(MONGO_COLLECTION)
            message = "Success to delete collection"
        else:
            message = "Collection does not exist"
        return {"status": 200, "message": message}
    except pymongo.errors.PyMongoError as e:
        return {
            "status": 500,
            "message": f"Error when dropping collection: {str(e)}",
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f"Other error when dropping collection: {str(e)}",
        }
