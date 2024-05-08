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

    async def get_preference_furniture(self, preference_id) -> dict:
        async with self.access_db() as conn:
            try:
                if not isinstance(preference_id, int):
                    raise ValueError("preference_id need to be integer")
                data = await conn.fetch(
                    """
                    SELECT
                        *
                    FROM
                        "PREFERENCE_HOUSE_FURNITURE" AS PRE_FUR
                    WHERE
                        PRE_FUR."Preference_ID" = $1
                    """,
                    preference_id,
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