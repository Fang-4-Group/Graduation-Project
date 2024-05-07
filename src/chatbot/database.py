import os

import pymongo
from dotenv import load_dotenv

load_dotenv()
mongo_uri = str(os.getenv("MONGO_URI"))

# Initialize the MongoDB client
client = pymongo.MongoClient(mongo_uri)
db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_COLLECTION")]


# Insert new message to group message records
async def add_message_to_group(group_id, message_detail):
    # Convert Pydantic model to dictionary
    msg_detail_dict = message_detail.model_dump()

    result = await collection.update_one(
        {"groupId": group_id},
        {"$push": {"messages": msg_detail_dict}},
        upsert=True,
    )
    return result


# Query all messages from a specific group
async def select_all_group_msg(group_id: str):
    cursor = collection.find({"groupId": group_id})
    result = []
    for msg in cursor:
        result.append(msg)
    return result
