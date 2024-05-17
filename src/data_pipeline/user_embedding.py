import numpy as np
import pandas as pd
import requests
from fastapi.responses import JSONResponse
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class UserEmbedding:
    def __init__(self):
        self.server_path = "http://localhost:7877/"
        self.url_young = self.server_path + "get_young_info/"
        self.url_elder = self.server_path + "get_elder_info/"
        # self.url_pre_house = self.server_path + "get_preference_house_place/"
        # self.url_dis_geo = self.server_path + "get_district_geocoding/"

    def embedding(self, k_mean, n_clusters):
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
                features = df.drop(
                    columns=["People_ID", "Preference_ID", "Role"]
                )  # noqa

                # 標準化
                scaler = StandardScaler()
                scaled_features = scaler.fit_transform(features)

                # 使用 K-means 聚類
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                kmeans.fit(scaled_features)

                # 將聚類結果添加到 DataFrame 中
                df["Cluster"] = kmeans.labels_
                df.sort_values(by=["Cluster"], inplace=True)

            # 替换NaN和Infinity值
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.fillna(0, inplace=True)

            dict_data = df.to_dict(orient="records")
            return JSONResponse(content=dict_data)

        except Exception as e:
            return {"message": f"Error when embedding user feature: {str(e)}"}
