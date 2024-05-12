import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()


class PosgresqClient:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.database = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")

    @asynccontextmanager
    async def access_db(self):
        conn = None
        try:
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            yield conn
        except Exception as e:
            raise Exception(f"Error when accessing db: {str(e)}")
        finally:
            if conn:
                await conn.close()

    async def get_young_info(self) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "PEOPLE" AS PEO
                        JOIN "PREFERENCE" AS PRE ON PEO."People_ID" = PRE."People_ID"
                    WHERE
                        PEO."Role" = 0;
                    """  # noqa
                )
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_elder_info(self) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "PEOPLE" AS PEO
                    WHERE
                        PEO."Role" = 1;
                    """  # noqa
                )
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_preference_house_place(self, preference_id) -> dict:
        async with self.access_db() as conn:
            try:
                if not isinstance(preference_id, int):
                    raise ValueError("preference_id need to be integer")
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "PREFERENCE_HOUSE_PLACE" AS PRE_PLA
                    WHERE
                        PRE_PLA."Preference_ID" = $1
                    """,
                    preference_id,
                )
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_district_geocoding(self, city, district):
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "DISTRICT_LOCATIONS" AS DIS
                    WHERE
                        DIS."City" = $1
                        AND DIS."District" = $2
                    """,
                    city,
                    district,
                )
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_house_info(self) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "HOUSE"
                    """
                )
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_sleep_time(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Sleep_Time" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id
                )
                return {"sleep_time": data}
            except Exception as e:
                return {"error": f"Error retrieving sleep time: {str(e)}"}

    async def get_drink_or_smoke(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Drink_or_Smoke"
                    FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id
                )
                return {"drink_or_smoke": data}
            except Exception as e:
                return {"error":
                        f"Error retrieving drink or smoke habit: {str(e)}"}

    async def get_clean_habit(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Clean" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id
                )
                return {"clean_habit": data}
            except Exception as e:
                return {"error": f"Error retrieving clean habit: {str(e)}"}

    async def get_mbti(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Mbti" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id
                )
                return {"mbti": data}
            except Exception as e:
                return {"error": f"Error retrieving MBTI: {str(e)}"}

    async def get_characters(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT "Character" FROM "PEOPLE_CHARACTER"
                    WHERE "People_ID" = $1;
                    """,
                    people_id
                )
                characters = [row["Character"] for row in data]
                return {"characters": characters}
            except Exception as e:
                return {"error": f"Error retrieving characters: {str(e)}"}

    async def get_interests(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        "Shopping", "Movie", "Travel", "Music", "Read",
                        "Game", "PE", "Science", "Food"
                    FROM
                        "PEOPLE"
                    WHERE
                        "People_ID" = $1;
                    """,
                    people_id
                )
                interests = {key: value for key,
                             value in data[0].items() if value == 1}
                return {"interests": interests}
            except Exception as e:
                return {"error": f"Error retrieving interests: {str(e)}"}

    async def update_sleep_time(
            self, people_id: int, new_sleep_time: int) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Sleep_Time" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_sleep_time, people_id
                )
                return {"message": "Sleep time updated successfully"}
            except Exception as e:
                return {"error": f"Error updating sleep time: {str(e)}"}

    async def update_drink_or_smoke(
            self, people_id: int, new_drink_or_smoke: int) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Drink_or_Smoke" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_drink_or_smoke, people_id
                )
                return {"message": "Drink or smoke habit updated successfully"}
            except Exception as e:
                return {"error":
                        f"Error updating drink or smoke habit: {str(e)}"}

    async def update_clean_habit(self, people_id: int, new_clean: int) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Clean" = $1 WHERE "People_ID" = $2;
                    """,
                    new_clean, people_id
                )
                return {"message": "Clean habit updated successfully"}
            except Exception as e:
                return {"error": f"Error updating clean habit: {str(e)}"}

    async def update_mbti(self, people_id: int, new_mbti: str) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Mbti" = $1 WHERE "People_ID" = $2;
                    """,
                    new_mbti, people_id
                )
                return {"message": "MBTI updated successfully"}
            except Exception as e:
                return {"error": f"Error updating MBTI: {str(e)}"}

    async def add_preference_house_furniture(
            self, preference_id: int, new_furniture: list) -> dict:
        async with self.access_db() as conn:
            try:
                for furniture in new_furniture:
                    await conn.execute(
                        """
                        INSERT INTO "PREFERENCE_HOUSE_FURNITURE" (
                            "Preference_ID", "Preference_House_Furniture")
                        VALUES ($1, $2);
                        """,
                        preference_id, furniture
                    )
                return {"message": "Preference house furniture added success"}
            except Exception as e:
                return {"error":
                        f"Error adding preference house furniture: {str(e)}"}

    async def add_preference_house_place(
            self, preference_id: int, new_place: list) -> dict:
        async with self.access_db() as conn:
            try:
                for place in new_place:
                    await conn.execute(
                        """
                        INSERT INTO "PREFERENCE_HOUSE_PLACE"
                        ("Preference_ID", "Preference_House_Place")
                        VALUES ($1, $2);
                        """,
                        preference_id, place
                    )
                return {"message": "Preference house place added successfully"}
            except Exception as e:
                return {"error":
                        f"Error adding preference house place: {str(e)}"}

    async def update_integer_field(
            self, column_name: str, people_id: int, new_value: int) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    f"""
                    UPDATE "PEOPLE" SET "{column_name}" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_value, people_id
                )
                return {"message": f"{column_name} updated successfully"}
            except Exception as e:
                return {"error": f"Error updating {column_name}: {str(e)}"}
