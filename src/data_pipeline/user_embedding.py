import numpy as np
import pandas as pd
import requests

from src.data_pipeline.utils import kmeans


class UserEmbedding:
    def __init__(self):
        self.server_path = "http://localhost:7877/"
        self.url_young = self.server_path + "get_young_info/"
        self.url_elder = self.server_path + "get_elder_info/"

    def embedding(self, k_mean: bool, n_clusters: int):
        try:
            response_y = requests.get(self.url_young)
            result_y = response_y.json()
            df_young = pd.DataFrame(result_y["message"])

            response_e = requests.get(self.url_elder)
            result_e = response_e.json()
            df_elder = pd.DataFrame(result_e["message"])

            df = pd.concat([df_young, df_elder], axis=0)

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
