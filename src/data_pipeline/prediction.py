import numpy as np

from database.migrations.pg_CRUD import PosgresqClient


class Prediction:
    def __init__(self):
        self.client = PosgresqClient()

    async def get_pre_house_lst(self, people_id: int) -> dict:
        preference_id = await self.client.get_preference_id(people_id)  # noqa
        preference_id = preference_id["Preference_ID"]
        pre_house_place = await self.client.get_preference_house_place(
            preference_id
        )  # noqa
        pre_house_lst = await self.client.get_pre_house_info(
            pre_house_place["message"]
        )  # noqa

        if len(pre_house_lst["data"]) < 3:
            random_int = np.random.randint(0, len(pre_house_lst["data"]))
            return_obj = pre_house_lst["data"][random_int]
        else:
            return_obj = {"message": "wait for rs"}
            # ToDo: recommadation system

        return {
            "data": return_obj,
        }
