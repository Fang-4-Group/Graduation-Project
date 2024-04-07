from pymongo import MongoClient

# MongoDB 連接資訊
host = "mongodb"  # 如果 MongoDB 在本地運行
port = 27017  # 默認 MongoDB 端口

# 連接 MongoDB
client = MongoClient(host, port)

# 列出所有數據庫
databases = client.list_database_names()
print("所有數據庫：")
for db in databases:
    print(db)
