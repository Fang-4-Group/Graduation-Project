import datetime
import os

# import json
# from bson.json_util import dumps
import pymongo
from dotenv import load_dotenv

load_dotenv()


class MongoDBInitClient:
    def __init__(self):
        self.host = os.getenv("MONGO_HOST", "localhost")
        self.port = int(os.getenv("MONGO_PORT", 27017))
        self.db_name = "sample"
        self.collection_name = "sample_chat_record"
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    async def insert_data(self):
        try:
            sample_data = [
                {
                    "groupId": "A1b2c3d4e5f67890abcdef1234567890",
                    "messages": [
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "接下來將先核對雙方基本資料，請屋主按以下格式打出\n身分:(屋主、轉租者、二房東等)\n姓名:\n年齡:\n出生年月:\n聯絡資料電話:\n聯絡資料電郵:\n請租客按以下格式打出\n姓名:\n年齡:\n出生年月:\n聯絡資料電話:\n聯絡資料電郵:",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 30, 25, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "姓名:ABC\n年齡:44\n出生年月:1980/1/09\n聯絡資料電話:0912341234\n聯絡資料電郵:abc@gmail.com",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 30, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "姓名:XYZ\n年齡:20\n出生年月:2004/11/15\n聯絡資料電話:0943214321\n聯絡資料電郵:xyz@gmail.com",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 32, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請屋主確認房屋基本資料，房屋地址:AA路X段Y號Z樓\n房屋坪數:10\n格局:一房一衛",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 35, 25, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "確認",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 40, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "確認",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 45, 50, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": ":請屋主傳送租房時將附帶之家具/設備(沙發/床鋪/熱水壺等)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 40, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "附帶床跟電視還有沙發",
                            "Time": datetime.datetime(
                                2024, 5, 2, 10, 50, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "有沒有書桌跟椅子阿",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 00, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "沒喔，請自行購買",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 1, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": ":請雙方討論看房時間跟方式",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 2, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "哪請問要什麼時候看房呢?XX月YY號ZZZZ點行嗎?",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 3, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "沒問題，是現場看房嗎?",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 4, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "對，我會在樓下等你，再帶你上去",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 5, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": ":請雙方討論房租與繳納週期/方式(房租金額/月繳年繳/現金或是匯款)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 6, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "這邊房租月租1萬5，年繳優惠每月1萬2",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 7, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "年繳優惠能夠每月1萬嗎?",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 8, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "不行，最少1萬3",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 9, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "成交",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 10, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論水電瓦斯費用歸屬",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 11, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "這些都不包含在房租之中喔，要請你自行負擔",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 12, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "成交",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 13, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論修繕/升級費用歸屬(更換水管/燈具等)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 14, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "換水管等修繕費用可以八二分配嗎?我八你二",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 15, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "更換燈具可以對半分然後水管等升級你負擔全部嗎",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 16, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "ok",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 17, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論其他雜項費用(網路/管理等)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 18, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "這邊並沒又配套的網路跟管理員，所以這些費用也要請你自己負擔",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 19, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "了解了",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 20, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論訂金與押金金額，和訂金與押金歸還方式",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 21, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "訂金就三個月房租，押金一個月房租。簽約成功訂金抵掉房租，押金退租時驗屋沒問題全額歸還",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 22, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "那我得先留存現在屋況的照片",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 23, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論保險相關保費(住宅/租屋火險等)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 24, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "我這邊已經保了住宅火險了",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 25, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "沒問題",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 26, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論關於提前解約(退租)之處理方式(上述各類費用歸還與否)",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 27, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "提前解約的話押金一樣按照屋況退還",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 28, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "那已繳的房租，像是月初剛繳完就退租房租能退還嗎",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 29, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "可以，按天數比例還款",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 29, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "請雙方討論各項規定(寵物/開伙等)，如果需要可以提供以下模板\n是否可養寵物\n自行裝修之許可/範圍\n是否可以合租/轉租\n是否可以開伙做飯(電磁爐等)\n是否允許留宿\n租客可否自行換鎖\n其他規定等\n",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 29, 55, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "寵物可以養，自行裝修的話請先都詢問過我。也請不要合租轉組給其他人。剩下的原則上都可以",  # noqa
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 30, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U98765fed43210cba98765fed43210cba",
                            "UserName": "租客",
                            "MsgText": "如果我換鎖的話需要給鑰匙嗎",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 31, 20, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U12345abc67890def12345abc67890def",
                            "UserName": "屋主",
                            "MsgText": "沒關係，不用",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 31, 45, 500000
                            ),  # noqa
                        },
                        {
                            "UserId": "U45678abc67890def12345abc67890def",
                            "UserName": "青銀共居",
                            "MsgText": "接下來輸出以上聊天摘要並請雙方確認\n聊天摘要紀錄",
                            "Time": datetime.datetime(
                                2024, 5, 2, 11, 27, 55, 500000
                            ),  # noqa
                        },
                    ],
                }
            ]  # noqa
            # 檢查資料庫中是否已存在相同的資料
            existing_data = self.collection.find_one(
                {"groupId": sample_data[0]["groupId"]}
            )
            if existing_data:
                return {
                    "message": "Data already exists in the database",
                }
            else:
                # 如果不存在相同的資料，執行插入操作
                result = self.collection.insert_many(sample_data)
                return {
                    "message": f"Success to insert data: {result}",
                }
        except Exception as e:
            return {
                "message": f"Error when inserting data: {str(e)}",
            }
