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
from sklearn.metrics.pairwise import cosine_similarity
from torch import float, long, no_grad, tensor
from torch_geometric.data import Data
from torch_geometric.utils import to_networkx

from database.migrations.pg_CRUD import PosgresqClient
from src.data_pipeline.GAT import GAT
from src.data_pipeline.item_embedding import ItemEmbedding
from src.data_pipeline.user_embedding import UserEmbedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


class EmbeddingModel:
    def __init__(self, target: int, place_dict: dict = None):
        """sumary_line

        Keyword arguments:
        target -- 0: for young; 1: for the elderly
        """
        self.api_url = os.getenv("API_URL")
        self.target = target
        self.USER_ID = []
        self.ITEM_ID = []
        self.epoch_num = 100
        self.place_dict = place_dict

    async def fetch_data(
        self, session, endpoint: str, item_params: dict = None
    ):  # noqa
        if item_params:
            async with session.post(
                f"{self.api_url}/{endpoint}", json=item_params
            ) as response:  # noqa
                return await response.json()
        else:
            async with session.get(f"{self.api_url}/{endpoint}") as response:
                return await response.json()

    async def get_embedding_data(self):
        userEmbeddingClient = UserEmbedding()
        df_user = userEmbeddingClient.embedding(0, 3)
        logger.info(f"user return type: {type(df_user)}")
        itemEmbeddingClient = ItemEmbedding()
        df_house = await itemEmbeddingClient.item_embedding()
        logger.info(f"item return type: {type(df_house)}")
        return df_user, df_house

    def process_data(self, df_user, df_house):
        df_role_0 = df_user[df_user["Role"] == 0]
        df_role_1 = df_user[df_user["Role"] == 1]

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
        client = PosgresqClient()
        interaction = await client.get_whole_interaction(self.target)
        interaction = [dict(record) for record in interaction]
        logger.info(f"interaction type: {type(interaction)}")
        df_interaction = pd.DataFrame(interaction)
        logger.info(f"interaction df columns: {df_interaction.columns}")

        edge_index = []
        edge_weight = []

        weight_dict = {"Viewed": 1, "Grouped": 2, "Selected": 3}

        for _, row in df_interaction.iterrows():
            user_id = row["People_ID"]
            item_id = row["Item_ID"]

            for interaction_type, weight in weight_dict.items():
                if row[interaction_type] > 0:
                    edge_index.append([user_id, item_id])
                    edge_weight.append(weight)

        edge_index = np.array(edge_index).T
        edge_weight = np.array(edge_weight)

        edge_index = tensor(edge_index, dtype=long)
        edge_weight = tensor(edge_weight, dtype=float)

        return edge_index, edge_weight

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

        data = Data(x=x, edge_index=edge_index, edge_attr=edge_weight)

        # 繪製圖形
        G = to_networkx(data, edge_attrs=["edge_attr"])

        num_users = len(user_features_padded)
        num_items = len(item_features_padded)
        user_indices = range(num_users)
        item_indices = range(num_users, num_users + num_items)

        plt.figure(figsize=(10, 8))

        plt.figure(figsize=(8, 6))
        nx.draw(
            G,
            with_labels=True,
            node_size=300,
            node_color="skyblue",
            font_size=16,
            font_weight="bold",
            edge_color="black",
        )
        # 添加標題
        plt.title("Graph Visualization with User and Item Nodes")

        # 保存圖形
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"graph_visualization_{timestamp}.png"
        plt.savefig(f"src/data_pipeline/graph/{filename}", format="png", dpi=300)

        return data, reverse_user_id_map, reverse_item_id_map

    async def train_model(self, data):
        model = GAT(
            num_features=data.x.shape[1],
            hidden_channels=8,
            num_embeding=8,
            heads=1,
        )
        optimizer = optim.Adam(model.parameters(), lr=0.01)

        def train():
            model.train()
            optimizer.zero_grad()
            out = model(data)
            loss = F.mse_loss(out[data.edge_index[0]], out[data.edge_index[1]])
            loss.backward()
            optimizer.step()
            return loss.item()

        for epoch in range(self.epoch_num):
            loss = train()
            if epoch % 20 == 0:
                logger.info(f"Epoch {epoch + 1}, Loss: {loss:.4f}")

        model.eval()
        with no_grad():
            embeddings = model(data)

        logger.info(f"Embedding Shape: {embeddings.shape}")
        logger.info(f"len: {len(data.x)}")
        user_embeddings = embeddings[: len(self.USER_ID)]
        item_embeddings = embeddings[len(self.USER_ID) :]
        logger.info(f"Shape After Embedding")
        logger.info(f"user: {user_embeddings.shape}")
        logger.info(f"item: {item_embeddings.shape}")
        return user_embeddings, item_embeddings

    async def recommend(
        self,
        user_embeddings,
        item_embeddings,
        reverse_user_id_map,
        reverse_item_id_map,
        K=2,
    ):
        similarity_matrix = cosine_similarity(
            user_embeddings.numpy(), item_embeddings.numpy()
        )
        logger.info(f"Similarity Matrix:\n{similarity_matrix}")

        top_k_recommendations = np.argsort(-similarity_matrix, axis=1)[:, :K]

        recommendations = {}
        for user_id, recs in enumerate(top_k_recommendations):
            logger.info(f"user id: {user_id}")
            logger.info(f"Recommand: {recs}")
            original_user = reverse_user_id_map[user_id]
            original_recs = [reverse_item_id_map[item_id] for item_id in recs]
            recommendations[original_user] = original_recs
            logger.info(f"User {original_user}: {original_recs}")

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
