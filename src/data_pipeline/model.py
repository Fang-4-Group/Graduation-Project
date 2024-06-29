# flake8: noqa
import logging
import os

import aiohttp
import numpy as np
import pandas as pd
import torch.nn.functional as F
import torch.optim as optim
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity
from torch import float, long, no_grad, tensor
from torch_geometric.data import Data

from src.data_pipeline.GAT import GAT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel:
    def __init__(self, target):
        """sumary_line

        Keyword arguments:
        target -- 0: for young; 1: for the elderly
        """

        load_dotenv()
        self.api_url = os.getenv("API_URL")
        self.target = target
        self.USER_ID = []
        self.ITEM_ID = []
        self.epoch_num = 100

    async def fetch_data(self, session, endpoint):
        async with session.get(f"{self.api_url}/{endpoint}") as response:
            return await response.json()

    async def get_embedding_data(self):
        async with aiohttp.ClientSession() as session:
            user_result = await self.fetch_data(session, "user_embedding/")
            house_result = await self.fetch_data(session, "item_embedding/")
            return user_result, house_result

    def process_data(self, user_result, house_result):
        df_user = pd.DataFrame(user_result)
        df_role_0 = df_user[df_user["Role"] == 0]
        df_role_1 = df_user[df_user["Role"] == 1]

        young_user_features = df_role_0.iloc[
            :, df_role_0.columns.get_loc("Sleep_Time") :
        ].values
        elder_user_features = df_role_1.iloc[
            :, df_role_1.columns.get_loc("Sleep_Time") :
        ].values

        df_house = pd.DataFrame(house_result)
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

        return young_user_features, elder_user_features, house_features

    def build_graph(self, user_features, item_features, interactions):
        user_id_map = {u_id: idx for idx, u_id in enumerate(self.USER_ID)}
        item_id_map = {i_id: idx for idx, i_id in enumerate(self.ITEM_ID)}
        reverse_user_id_map = {v: k for k, v in user_id_map.items()}
        reverse_item_id_map = {v: k for k, v in item_id_map.items()}

        interactions_mapped = np.array(
            [[user_id_map[uid], item_id_map[iid]] for uid, iid in interactions]
        )

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

        x = tensor(np.vstack((user_features_padded, item_features_padded)), dtype=float)
        edge_index = tensor(
            np.array(
                [
                    interactions_mapped[:, 0],
                    interactions_mapped[:, 1] + len(user_features_padded),
                ]
            ),
            dtype=long,
        )

        data = Data(x=x, edge_index=edge_index)
        return data, reverse_user_id_map, reverse_item_id_map

    async def train_model(self, data):
        model = GAT(
            num_features=data.x.shape[1],
            hidden_channels=8,
            num_embeding=8,
            heads=2,
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

        user_embeddings = embeddings[: len(data.x) // 2]
        item_embeddings = embeddings[len(data.x) // 2 :]
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

        interactions = np.array([[2, 1], [2, 3], [4, 1], [6, 5]])
        if self.target == 0:
            data, reverse_user_id_map, reverse_item_id_map = self.build_graph(
                young_user_features, house_features, interactions
            )
        else:
            data, reverse_user_id_map, reverse_item_id_map = self.build_graph(
                elder_user_features, young_user_features, interactions
            )

        user_embeddings, item_embeddings = await self.train_model(data)
        return await self.recommend(
            user_embeddings,
            item_embeddings,
            reverse_user_id_map,
            reverse_item_id_map,
        )


# To use the EmbeddingModel class
# you would create an instance
# and call the `run` method in an asynchronous context.
# Example:
# embedding_model = EmbeddingModel()
# asyncio.run(embedding_model.run())
