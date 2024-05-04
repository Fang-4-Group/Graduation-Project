import datetime
import os

# import json
# from bson.json_util import dumps
import pymongo
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class MongoDBInitClient:
    def __init__(self):
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = int(os.getenv("MONGO_PORT", 27017))
        self.db_name = "mongodb"
        self.collection_name = "chat_record"
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def insert_data(self):
        try:
            sample_data = [
                {
                    "_id": "6631da356b73409ff06bfd1b",
                    "groupId": "A1b2c3d4e5f67890abcdef1234567890",
                    "messages": [
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "張大志",
                            "MsgText": "你好",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 30, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "王子軒",
                            "MsgText": "hello",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 32, 20, 500000
                            ),  # noqa
                        },
                    ],
                },
                {  # noqa
                    "_id": "6631da356b73409ff06bfd1c",
                    "groupId": "B1c2d3e4f5g67890hijklmnopqrstuvwx",
                    "messages": [
                        {
                            "UserId": "U13579ace24680ace13579ace24680ace",
                            "UserName": "Cathy",
                            "MsgText": "請問房間可以開火嗎?",
                            "Time": datetime.datetime(
                                2024, 5, 3, 9, 0, 15, 250000
                            ),  # noqa
                        },
                        {
                            "UserId": "U02468bdf13579bdf02468bdf13579bdf",
                            "UserName": "林惠芬",
                            "MsgText": "可以的，但要注意一點",
                            "Time": datetime.datetime(
                                2024, 5, 3, 9, 1, 5, 250000
                            ),  # noqa
                        },
                    ],
                },
            ]  # noqa
            result = self.collection.insert_many(sample_data)
            return {
                "status": 200,
                "message": f"Inserted {len(result.inserted_ids)} documents",
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Other error when inserting data: {str(e)}",
            )

    async def get_data_by_group_id(self, group_id):
        try:
            query = {"groupId": group_id}
            document = self.collection.find_one(query)
            if document:
                return {
                    "status": 200,
                    "data": document,
                }
            else:
                return {
                    "status": 404,
                    "message": "Document not found",
                }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Other error when getting data: {str(e)}",
            )
