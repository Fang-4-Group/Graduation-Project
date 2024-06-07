import aiohttp
import numpy as np
import pandas as pd
from fastapi.responses import JSONResponse


class ItemEmbedding:
    def __init__(self):
        self.server_path = "http://localhost:7877/"
        self.url_item = self.server_path + "get_house_info/"

    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def item_embedding(self):
        try:
            async with aiohttp.ClientSession() as session:
                response = await self.fetch_data(session, self.url_item)
                df = pd.DataFrame(response["message"])

                # one-hot encoding
                encoded = pd.get_dummies(df[["Type"]], dtype="int")

                # 合併 one-hot 編碼的列
                df = pd.concat([df, encoded], axis=1)

                # 刪除原始的 Fire, Negotiate_Price, Type 列
                df.drop(columns=["Type"], inplace=True)

                # 替换NaN和Infinity值
                df.replace([np.inf, -np.inf], np.nan, inplace=True)
                df.fillna(0, inplace=True)

                dict_data = df.to_dict(orient="records")
                return JSONResponse(content=dict_data)

        except Exception as e:
            import traceback

            error_message = traceback.format_exc()
            return {
                "message": f"Error when embedding user feature: {str(e)}",
                "details": error_message,
            }
