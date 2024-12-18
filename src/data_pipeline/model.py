# flake8: noqa
import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import torch.nn.functional as F
import torch.optim as optim
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# from sklearn.metrics.pairwise import cosine_similarity
from torch import float, load, long, no_grad, save, tensor, zeros_like
from torch_geometric.data import Data
from torch_geometric.utils import negative_sampling

from database.migrations.pg_CRUD import PosgresqClient
from src.data_pipeline.GAT import GAT
from src.data_pipeline.item_embedding import ItemEmbedding
from src.data_pipeline.user_embedding import UserEmbedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


class EmbeddingModel:
    def __init__(self, target: int, place_dict: dict = None, train: int = 1):
        """sumary_line

        Keyword arguments:
        target -- 0: for young; 1: for the elderly
        """
        self.target = target
        self.USER_ID = []
        self.ITEM_ID = []
        self.epoch_num = 100
        self.place_dict = place_dict
        self.client = PosgresqClient()
        self.model_train = train

    async def get_embedding_data(self):
        userEmbeddingClient = UserEmbedding()
        df_user = await userEmbeddingClient.embedding(0, 3)
        df_user = pd.DataFrame(df_user)
        logger.info(f"user return type: {type(df_user)}")
        logger.info(f"user return: {df_user}")

        itemEmbeddingClient = ItemEmbedding()
        df_house = await itemEmbeddingClient.item_embedding()
        logger.info(f"item return type: {type(df_house)}")
        logger.info(f"item return: {df_house}")
        return df_user, df_house

    def process_data(self, df_user, df_house):
        df_role_0 = df_user[df_user["Role"] == 0]
        df_role_1 = df_user[df_user["Role"] == 1]

        logger.info(f"df_role_0: {df_role_0}")
        logger.info(f"df_role_1: {df_role_1}")

        young_user_features = df_role_0.iloc[
            :, df_role_0.columns.get_loc("Sleep_Time") :
        ].values
        elder_user_features = df_role_1.iloc[
            :, df_role_1.columns.get_loc("Sleep_Time") :
        ].values

        selected_columns = [
            "Size",
            "Fire",
            "Negotiate_Price",
            "Floor",
            "Type_公寓",
            "Type_大樓",
            "Type_華廈",
        ]
        house_features = df_house[selected_columns].values

        # extract id for id mapping
        if self.target == 0:
            self.USER_ID = df_role_0["People_ID"]
            self.ITEM_ID = df_house["House_ID"]
        elif self.target == 1:
            self.USER_ID = df_role_1["People_ID"]
            self.ITEM_ID = df_role_0["People_ID"]
        else:
            logger.warning("target should be 0 or 1")

        logger.info(f"User Id: {self.USER_ID}")
        logger.info(f"Item Id: {self.ITEM_ID}")

        return young_user_features, elder_user_features, house_features

    async def fetch_and_process_interactiom(self):
        interaction = await self.client.get_whole_interaction(self.target)
        interaction = [dict(record) for record in interaction]
        logger.info(f"interaction: {interaction}")

        df_interaction = pd.DataFrame(interaction)
        logger.info(f"interaction df: {df_interaction}")

        edge_index = []
        edge_weight = []

        weight_dict = {
            "Selected": 3,
            "Grouped": 2,
            "Viewed": 1,
        }

        for _, row in df_interaction.iterrows():
            user_id = row["People_ID"]
            item_id = row["Item_ID"]

            for interaction_type, weight in weight_dict.items():
                if row[interaction_type] > 0:
                    edge_index.append([user_id, item_id])
                    edge_weight.append(weight)
                    break

        edge_index = np.array(edge_index).T
        edge_weight = np.array(edge_weight)

        edge_index = tensor(edge_index, dtype=long)
        edge_weight = tensor(edge_weight, dtype=float)

        logger.info(f"edge index: {edge_index}")

        return edge_index, edge_weight

    def plot_graph(self, edge_index, edge_weight, user_ids, item_ids):

        G = nx.Graph()

        # 添加 user 節點
        for i, user_id in enumerate(user_ids):
            G.add_node(f"u_{user_id}", type="user", color="aquamarine")

        # 添加 item 節點
        for i, item_id in enumerate(item_ids):
            G.add_node(f"i_{item_id}", type="item", color="lightblue")

        # 添加邊（包含權重）
        for i in range(len(edge_weight)):
            source = f"u_{edge_index[0, i]}"
            target = f"i_{edge_index[1, i]}"

            logger.info(f"{source} - {target}")

            # 加入邊並標記權重
            G.add_edge(source, target, weight=int(edge_weight[i]))

        # 設置節點顏色
        node_colors = [G.nodes[node]["color"] for node in G.nodes]

        # 繪製節點和邊
        pos = nx.circular_layout(G)  # 使用spring布局
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )

        # 為邊添加權重標籤
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # 圖片儲存
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        folder_path = "src/data_pipeline/graph"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = f"graph_{timestamp}.png"
        plt.savefig(f"{folder_path}/{filename}", format="png", dpi=300)

    async def build_graph(self, user_features, item_features):
        user_id_map = {u_id: idx for idx, u_id in enumerate(self.USER_ID)}
        item_id_map = {i_id: idx for idx, i_id in enumerate(self.ITEM_ID)}
        reverse_user_id_map = {v: k for k, v in user_id_map.items()}
        reverse_item_id_map = {v: k for k, v in item_id_map.items()}

        logger.info(f"user id map: {user_id_map}")
        logger.info(f"item id map: {item_id_map}")

        # 計算需要填充的列數
        num_padding_columns_user = max(
            0, item_features.shape[1] - user_features.shape[1]
        )
        num_padding_columns_item = max(
            0, user_features.shape[1] - item_features.shape[1]
        )

        # 為較短的特徵矩陣添加填充列
        user_features_padded = np.pad(
            user_features,
            ((0, 0), (0, num_padding_columns_user)),
            mode="constant",
        )
        item_features_padded = np.pad(
            item_features,
            ((0, 0), (0, num_padding_columns_item)),
            mode="constant",
        )

        logger.info("Shape After Padding")
        logger.info(f"user: {user_features_padded.shape}")
        logger.info(f"item: {item_features_padded.shape}")

        x = tensor(np.vstack((user_features_padded, item_features_padded)), dtype=float)

        edge_index, edge_weight = await self.fetch_and_process_interactiom()

        # 畫圖
        self.plot_graph(
            edge_index=edge_index,
            edge_weight=edge_weight,
            user_ids=list(user_id_map.keys()),
            item_ids=list(item_id_map.keys()),
        )

        # 轉換 user ids 和 item ids
        new_edge_index = zeros_like(edge_index)

        # 替換 user ids
        for i, user_id in enumerate(edge_index[0]):
            new_edge_index[0, i] = user_id_map.get(
                user_id.item(), -1
            )  # 如果找不到，預設為 -1

        # 替換 item ids
        for i, item_id in enumerate(edge_index[1]):
            new_edge_index[1, i] = item_id_map.get(
                item_id.item(), -1
            )  # 如果找不到，預設為 -1

        logger.info(f"transformed edge index: {new_edge_index}")

        data = Data(x=x, edge_index=new_edge_index, edge_attr=edge_weight)

        return data, reverse_user_id_map, reverse_item_id_map

    async def train_model(self, data):
        folder_path = "src/data_pipeline/model"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 正樣本邊 (來自圖的邊)
        pos_edge = data.edge_index

        # 負樣本邊 (隨機生成負樣本)
        neg_edge = negative_sampling(
            edge_index=data.edge_index, num_nodes=data.num_nodes
        )

        model = GAT(
            num_features=data.x.shape[1],
            hidden_channels=8,
            num_embeding=8,
            heads=1,
        )
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        def train():
            model.train()
            optimizer.zero_grad()
            loss = model.bpr_loss(data, pos_edge, neg_edge)
            loss.backward()
            optimizer.step()
            return loss.item()

        if self.model_train:
            for epoch in range(self.epoch_num):
                loss = train()
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch + 1}, Loss: {loss:.4f}")
        else:
            logger.info("load model")
            files = os.listdir("src/data_pipeline/model/")
            logger.info(files)
            model.load_state_dict(load("src/data_pipeline/model/" + files[-1]))

        model.eval()
        # model 輸出
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        save(model.state_dict(), f"{folder_path}/{timestamp}.pth")

        with no_grad():
            embeddings = model(data)

        logger.info(f"Embedding Shape: {embeddings.shape}")
        logger.info(f"len: {len(data.x)}")
        user_embeddings = embeddings[: len(self.USER_ID)]
        item_embeddings = embeddings[len(self.USER_ID) :]
        logger.info(f"Shape After Embedding")
        logger.info(f"user: {user_embeddings.shape}")
        logger.info(f"item: {item_embeddings.shape}")

        logger.info(f"Embedding:")
        logger.info(f"user: {user_embeddings}")
        logger.info(f"item: {item_embeddings}")

        return user_embeddings, item_embeddings

    async def recommend(
        self,
        user_embeddings,
        item_embeddings,
        reverse_user_id_map,
        reverse_item_id_map,
        K=3,
    ):
        similarity_matrix = np.dot(user_embeddings.numpy(), item_embeddings.numpy().T)
        logger.info(f"Similarity Matrix:\n{similarity_matrix}")

        # Similarity Matrix 輸出
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        folder_path = "src/data_pipeline/similarity_matrix"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=[
                reverse_user_id_map[user_id]
                for user_id in range(user_embeddings.shape[0])
            ],
            columns=[
                reverse_item_id_map[item_id]
                for item_id in range(item_embeddings.shape[0])
            ],
        )

        # 保存 CSV 文件
        similarity_df.to_csv(f"{folder_path}/{timestamp}.csv")

        top_k_recommendations = np.argsort(-similarity_matrix, axis=1)[:, :K]

        recommendations = {}
        for user_id, recs in enumerate(top_k_recommendations):
            logger.info(f"user id: {user_id}")
            logger.info(f"Recommand: {recs}")
            original_user = reverse_user_id_map[user_id]
            original_recs = [reverse_item_id_map[item_id] for item_id in recs]
            recommendations[original_user] = original_recs
            logger.info(f"User {original_user}: {original_recs}")

            await self.client.add_recommendation(
                self.target, {"People_ID": original_user, "Item_ID": original_recs}
            )

        return JSONResponse(content=recommendations)

    async def run(self):
        user_result, house_result = await self.get_embedding_data()
        young_user_features, elder_user_features, house_features = self.process_data(
            user_result, house_result
        )

        if self.target == 0:
            data, reverse_user_id_map, reverse_item_id_map = await self.build_graph(
                young_user_features, house_features
            )
        else:
            data, reverse_user_id_map, reverse_item_id_map = await self.build_graph(
                elder_user_features, young_user_features
            )

        user_embeddings, item_embeddings = await self.train_model(data)
        return await self.recommend(
            user_embeddings,
            item_embeddings,
            reverse_user_id_map,
            reverse_item_id_map,
        )
