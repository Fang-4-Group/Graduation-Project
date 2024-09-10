import logging

import aiohttp
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ItemEmbedding:
    def __init__(self):
        self.server_path = "http://localhost:7877/"
        self.url_item = self.server_path + "get_house_info/"

    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def item_embedding(self, place_lst: list = None) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                all_data = []
                if place_lst:
                    for place in place_lst:
                        city, district = place
                        # 構建 URL，添加查詢參數
                        params = []
                        if city:
                            params.append(f"city={city}")
                        if district:
                            params.append(f"district={district}")

                        url = self.url_item
                        if params:
                            url += "?" + "&".join(params)

                        response = await self.fetch_data(session, url)
                        all_data.extend(response["message"])
                else:
                    response = await self.fetch_data(session, self.url_item)
                    all_data.extend(response["message"])

                df = pd.DataFrame(all_data)

                # one-hot encoding
                encoded = pd.get_dummies(df[["Type"]], dtype="int")

                # 確保所有可能的列都存在
                all_types = ["Type_公寓", "Type_大樓", "Type_華廈"]
                for t in all_types:
                    if t not in encoded.columns:
                        encoded[t] = 0

                # 按照原來的順序排列列
                encoded = encoded[all_types]

                # 合併 one-hot 編碼的列
                df = pd.concat([df, encoded], axis=1)

                # 刪除原始的 Fire, Negotiate_Price, Type 列
                df.drop(columns=["Type"], inplace=True)

                # 替换NaN和Infinity值
                df.replace([np.inf, -np.inf], np.nan, inplace=True)
                df.fillna(0, inplace=True)

                return df

        except Exception as e:
            import traceback

            error_message = traceback.format_exc()
            return {
                "message": f"Error when embedding user feature: {str(e)}",
                "details": error_message,
            }
