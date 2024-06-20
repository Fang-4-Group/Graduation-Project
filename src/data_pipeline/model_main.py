import os

import numpy as np
import pandas as pd
import requests
import torch.nn.functional as F
import torch.optim as optim
from dotenv import load_dotenv
from GAT import GAT
from sklearn.metrics.pairwise import cosine_similarity
from torch import float, long, no_grad, tensor
from torch_geometric.data import Data

"""get data

"""
# 加載 .env 文件
print("loading .env and geting API_URL variable")
load_dotenv()

# 使用 host.docker.internal 訪問主機服務
API_URL = os.getenv("API_URL")
print("API URL:", API_URL)

# get data
print("Geting embedding data ...")
user_result = requests.get(f"{API_URL}/user_embedding/").json()
house_result = requests.get(f"{API_URL}/item_embedding/").json()
print("Finins geting embedding data")

# process user data, and extract features
df_user = pd.DataFrame(user_result)

df_role_0 = df_user[df_user["Role"] == 0]
df_role_1 = df_user[df_user["Role"] == 1]

young_user_features = df_role_0.iloc[
    :, df_role_0.columns.get_loc("Sleep_Time") :  # noqa
].values
elder_user_features = df_role_1.iloc[
    :, df_role_1.columns.get_loc("Sleep_Time") :  # noqa
].values


# process house data, and extract features
df_item = pd.DataFrame(house_result)

selected_columns = [
    "Size",
    "Fire",
    "Negotiate_Price",
    "Floor",
    "Type_公寓",
    "Type_大樓",
    "Type_華廈",
]
house_features = df_item[selected_columns].values


""" Construct the user-item interaction graph
user: young_user_features
item: elder_user_features + df_item(暫時先只用 df_item)
"""

# user-item interaction data
# Each row represents an interaction [People_ID, House_ID]
interactions = np.array([[2, 1], [2, 3], [4, 2], [6, 5]])

# User feature matrix
user_features = young_user_features

# Item feature matrix
item_features = house_features


# ID mapping
user_ids = df_role_0["People_ID"]
item_ids = df_item["House_ID"]

# { People_ID: id }
user_id_map = {user_id: idx for idx, user_id in enumerate(user_ids)}

# { House_ID: id }
item_id_map = {item_id: idx for idx, item_id in enumerate(item_ids)}

# { id: People_ID }
reverse_user_id_map = {v: k for k, v in user_id_map.items()}

# { id: House_ID }
reverse_item_id_map = {v: k for k, v in item_id_map.items()}

print(" user id map:", user_id_map)
print("house id map:", item_id_map)


# 將 interactions 中的 user_id 和 item_id 替換為對應的索引
interactions_mapped = np.array(
    [[user_id_map[uid], item_id_map[iid]] for uid, iid in interactions]
)

print("interactions mapped:\n", interactions_mapped)


# 在 item_features 中加入必要數量的全 0 列，使其與 user_features 具有相同的列數
num_padding_columns = user_features.shape[1] - item_features.shape[1]
item_features_padded = np.pad(
    item_features, ((0, 0), (0, num_padding_columns)), mode="constant"
)

# 節點特徵矩陣
x = tensor(np.vstack((user_features, item_features_padded)), dtype=float)

# 建立邊的索引
edge_index = tensor(
    np.array(
        [
            interactions_mapped[:, 0],
            interactions_mapped[:, 1] + len(user_features),
        ]  # noqa
    ),
    dtype=long,
)

# 建立圖數據
data = Data(x=x, edge_index=edge_index)


"""模型建構&訓練

Output:
    - user embedding
    - item embedding
"""

model = GAT(num_features=x.shape[1], hidden_channels=8, num_embeding=8, heads=2)  # noqa
optimizer = optim.Adam(model.parameters(), lr=0.01)


def train():
    model.train()
    optimizer.zero_grad()
    out = model(data)
    # 範例損失函數：可以使用多種方法來定義實際的損失函數
    loss = F.mse_loss(out[data.edge_index[0]], out[data.edge_index[1]])
    loss.backward()
    optimizer.step()
    return loss.item()


for epoch in range(200):
    loss = train()
    if epoch % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss:.4f}")

model.eval()
with no_grad():
    embeddings = model(data)

# 提取用戶嵌入和物品嵌入
user_embeddings = embeddings[: len(user_features)]
item_embeddings = embeddings[len(user_features) :]  # noqa

print("User Embeddings:\n", user_embeddings)
print("Item Embeddings:\n", item_embeddings)
print()

"""Prediction

Output: each user's recommadation
"""


# 計算使用者和物品嵌入之間的餘弦相似度
user_embeddings_np = user_embeddings.numpy()
item_embeddings_np = item_embeddings.numpy()

similarity_matrix = cosine_similarity(user_embeddings_np, item_embeddings_np)
print("Similarity Matrix:\n", similarity_matrix)
print()

# 為每個使用者推薦 Top-K 個物品
K = 2
top_k_recommendations = np.argsort(-similarity_matrix, axis=1)[:, :K]

print("Top-K Recommendations for each user:")

for user_id, recommendations in enumerate(top_k_recommendations):
    original_user = reverse_user_id_map[user_id]

    original_recommendations = [
        reverse_item_id_map[item_id] for item_id in recommendations
    ]

    print(f"User {original_user}: {recommendations}")
