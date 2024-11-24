import os

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)
mongo_uri = str(os.getenv("MONGO_DB_URI"))

# Initialize the MongoDB client
mongo_uri = str(os.getenv("MONGO_DB_URI"))
client = pymongo.MongoClient(mongo_uri)
db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_DB_COLLECTION")]


def save_group_chat_records_to_db(group_id, message_detail):
    # Convert Pydantic model to dictionary
    msg_detail_dict = message_detail.dict()

    result = collection.update_one(
        {"groupId": group_id},
        {"$push": {"messages": msg_detail_dict}},
        upsert=True,  # noqa
    )
    return result


def get_group_chat_records_by_id(group_id):
    result = collection.find(
        {"groupId": group_id},
        {"messages.UserName": 1, "messages.MsgText": 1, "_id": 0},  # noqa
    )
    return list(result)
