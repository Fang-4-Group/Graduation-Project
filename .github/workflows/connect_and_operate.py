import os

import pymongo

# Get MongoDB connection information from environment variables
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))  # Convert port to integer
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")

# Connect to MongoDB
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

# Execute MongoDB data operations
# Here you can add any operations you need to perform on MongoDB
# For example: insert data, query data, etc.
result = collection.find()
for document in result:
    print(document)
