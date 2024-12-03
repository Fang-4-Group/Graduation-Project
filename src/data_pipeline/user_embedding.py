import logging

import numpy as np
import pandas as pd

from database.migrations.pg_CRUD import PosgresqClient
from src.data_pipeline.utils import kmeans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserEmbedding:
    def __init__(self):
        self.server_path = "https://fang5-group.tw/"
        self.url_young = self.server_path + "get_young_info/"
        self.url_elder = self.server_path + "get_elder_info/"

    async def embedding(self, k_mean: bool, n_clusters: int):
        try:
            client = PosgresqClient()
            result_y = await client.get_young_info()
            record_dicts = [dict(record) for record in result_y["message"]]
            df_young = pd.DataFrame(record_dicts)

            logger.info(f"young info column: {df_young.columns}")
            logger.info(f"young info: {df_young}")

            result_e = await client.get_elder_info()
            logger.info(result_e)
            record_key_y = list(dict(result_e["message"][0]).keys())
            logger.info(record_key_y)
            df_elder = pd.DataFrame(result_e["message"], columns=record_key_y)

            logger.info(f"elder info column: {df_elder.columns}")
            logger.info(f"elder info: {df_elder}")

            df = pd.concat([df_young, df_elder], axis=0)

            logger.info(f"Check: {df[df.Role == 0]}")

            df["M1"] = df["Mbti"].str[0]
            df["M2"] = df["Mbti"].str[1]
            df["M3"] = df["Mbti"].str[2]
            df["M4"] = df["Mbti"].str[3]

            # one-hot encoding
            mbti_encoded = pd.get_dummies(
                df[["M1", "M2", "M3", "M4"]], dtype="int"
            )  # noqa

            # 合併 one-hot 編碼的列
            df = pd.concat([df, mbti_encoded], axis=1)

            # 刪除原始的 Mbti 列和拆分後的四列
            df.drop(columns=["Mbti", "M1", "M2", "M3", "M4"], inplace=True)

            if k_mean:
                df = kmeans(df, n_clusters)

            # 替换NaN和Infinity值
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.fillna(0, inplace=True)
            return df

        except Exception as e:
            return {"message": f"Error when embedding user feature: {str(e)}"}
