import asyncio
import datetime
import json
import os

# import json
# from bson.json_util import dumps
import pymongo
from dotenv import load_dotenv

load_dotenv()

SAMPLE_DATA_PATH = "database/migrations/data/chatting_samples/sample_2.json"


def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    for group in data:
        for message in group["messages"]:
            time_str = message["Time"]
            message["Time"] = datetime.datetime.strptime(
                time_str, "%Y-%m-%dT%H:%M:%S.%f"
            )
    return data


class MongoDBInitClient:
    def __init__(self):
        self.url = os.getenv("MONGO_DB_URI")
        print(f"Connecting to MongoDB with URI: {self.url}")  # Debug print
        if not self.url:
            raise ValueError("MONGO_DB_URI environment variable is not set.")
        self.db_name = os.getenv("MONGO_DB_NAME", "Graduation-Project")
        self.collection_name = os.getenv(
            "MONGO_DB_COLLECTION", "group-chat-record"
        )  # noqa
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def insert_data(self):
        try:
            sample_data = load_data(SAMPLE_DATA_PATH)
            existing_data = self.collection.find_one(
                {"groupId": sample_data[0]["groupId"]}
            )
            if existing_data:
                return {"message": "Data already exists in the database"}
            else:
                result = await self.collection.insert_many(sample_data)
                return {
                    "message": f"Success to insert data: {result.inserted_ids}"
                }  # noqa
        except Exception as e:
            return {"message": f"Error when inserting data: {str(e)}"}


async def main():
    client = MongoDBInitClient()
    result = await client.insert_data()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
