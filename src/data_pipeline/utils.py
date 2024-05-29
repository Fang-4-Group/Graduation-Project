import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def kmeans(df: pd.DataFrame, n_clusters: int):
    features = df.drop(columns=["People_ID", "Preference_ID", "Role"])  # noqa

    # 標準化
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # 使用 K-means 聚類
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(scaled_features)

    # 將聚類結果添加到 DataFrame 中
    df["Cluster"] = kmeans.labels_
    df.sort_values(by=["Cluster"], inplace=True)
    return df
