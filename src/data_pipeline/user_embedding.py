import pandas as pd
import requests
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# from sklearn.metrics.pairwise import cosine_similarity


class UserEmbedding:
    def __init__(self):
        self.server_path = "http://localhost:7877/"
        self.url_young = self.server_path + "get_young_info/"
        self.url_elder = self.server_path + "get_elder_info/"
        self.url_pre_house = self.server_path + "get_preference_house_place/"
        self.url_dis_geo = self.server_path + "get_district_geocoding/"

    # def get_young_df(self):
    #     response_y = requests.get(self.url_young)
    #     if response_y.status_code == 200:
    #         result_y = response_y.json()
    #         # df_young = pd.DataFrame(result_y["message"])
    #         return {"data": result_y}
    #     else:
    #         return {"Error:", response_y.status_code}

    # def get_elder_df(self):
    #     response_e = requests.get(self.url_elder)
    #     if response_e.status_code == 200:
    #         result_e = response_e.json()
    #         # df_elder = pd.DataFrame(result_e["message"])
    #         return {"data": result_e}
    #     else:
    #         return {"Error:", response_e.status_code}

    def embedding(self, k_mean=1, n_clusters=3):
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

            # df_young 合併
            df = pd.concat([df, mbti_encoded], axis=1)

            # 删除原始的Mbti列和拆分後的四列
            df.drop(columns=["Mbti", "M1", "M2", "M3", "M4"], inplace=True)
        except Exception as e:
            return {"message": f"Error when embedding user feature: {str(e)}"}

        if k_mean:
            features = df.drop(columns=["People_ID", "Preference_ID", "Role"])

            # 標準化
            scaler = StandardScaler()
            scaled_features = scaler.fit_transform(features)

            # 計算距離矩陣
            # cos_sim_matrix = cosine_similarity(scaled_features)

            # 使用K-means
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(scaled_features)

            # 将聚类结果添加到DataFrame中
            df["Cluster"] = kmeans.labels_
            df.to_dict(orient="records")
            json_data = df.to_dict(orient="records")
            return {"data": json_data}
        else:
            json_data = df.to_dict(orient="records")
            return {"data": json_data}

    def pre_data_process(self):
        # pre_data = {}
        # for index, row in self.df_young.iterrows():
        # pre_id = row["Preference_ID"]
        pre_id = 1
        return {"message": f"{self.url_pre_fun}{pre_id}"}
        response_house = requests.get(f"{self.url_pre_house}{pre_id}")

        if response_house.status_code == 200:
            return {"fun": response_fun.json(), "house": response_house.json()}  # noqa
        else:
            return {"message": "Something wrong when access preference data"}
