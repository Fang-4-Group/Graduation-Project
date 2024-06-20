import numpy as np

from database.migrations.pg_CRUD import PosgresqClient


class Prediction:
    def __init__(self):
        self.client = PosgresqClient()

    async def get_pref_house_lst(self, people_id: int) -> dict:
        role = await self.client.get_role(people_id)
        role = role["Role"]

        if role == 0:  # for young people
            preference_id = await self.client.get_preference_id(people_id)  # noqa
            preference_id = preference_id["Preference_ID"]
            pre_house_place = await self.client.get_preference_house_place(
                preference_id
            )  # noqa
            pre_house_lst = await self.client.get_preferred_houses(
                pre_house_place["message"]
            )  # noqa
            if len(pre_house_lst["data"]) == 0:
                return {"data": "no house fit"}
            else:
                # 隨機選出三個房屋
                house_len = len(pre_house_lst["data"])
                num_samples = min(3, house_len)
                random_indices = np.random.choice(
                    np.arange(house_len), size=num_samples, replace=False
                )  # noqa
                return_obj = [pre_house_lst["data"][i] for i in random_indices]
        else:  # for elder people
            young_people = await self.client.get_young_info(amount=3)
            return_obj = young_people["message"]

        return {"data": return_obj}
