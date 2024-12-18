import logging
import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    async def get_young_info(self, amount: int = None) -> dict:
        async with self.access_db() as conn:
            try:
                query = """
                        SELECT
                            PEO."People_ID" AS "People_ID",
                            PEO.*
                        FROM
                            "PEOPLE" AS PEO
                            LEFT JOIN "PREFERENCE" AS PRE ON PEO."People_ID" = PRE."People_ID"
                        WHERE
                            PEO."Role" = 0
                        """  # noqa
                if amount is not None:
                    query += f"""
                    ORDER BY RANDOM()
                    LIMIT {amount}
                    """
                logger.info(f"query: {query}")
                data = await conn.fetch(query)
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
                place_list = [row["Preference_House_Place"] for row in data]
                return {"message": place_list}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_role(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        "Role"
                    FROM
                        "PEOPLE"
                    WHERE
                        "People_ID" = $1;
                    """,
                    people_id,
                )
                return data[0]
            except Exception as e:
                return {"error": f"Error getting role: {str(e)}"}

    async def get_preference_id(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT
                        "Preference_ID"
                    FROM
                        "PREFERENCE"
                    WHERE
                        "People_ID" = $1;
                    """,
                    people_id,
                )
                return data[0]
            except Exception as e:
                return {"error": f"Error getting preferenceid: {str(e)}"}

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

    async def get_house_info(
        self, city: str = None, district: str = None
    ) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                query = """
                    SELECT
                        *
                    FROM
                        "HOUSE"
                """
                conditions = []
                params = []

                if city:
                    conditions.append('"City" = $1')
                    params.append(city)
                if district:
                    conditions.append('"District" = $2')
                    params.append(district)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                logger.info("Query: %s", query)
                data = await conn.fetch(query, *params)
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_single_house(self, id: int = None) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                query = """
                    SELECT
                        *
                    FROM
                        "HOUSE" AS h
                    WHERE
                        h."House_ID" = $1
                """

                data = await conn.fetch(query, id)
                return data
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def get_name(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Name" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"name": data}
            except Exception as e:
                return {"error": f"Error retrieving name: {str(e)}"}

    async def get_preferred_houses(self, pre_house_place_lst: list) -> dict:
        async with self.access_db() as conn:
            try:
                # 執行 SQL 查詢
                data = []
                for dis in pre_house_place_lst:
                    sub_data = await conn.fetch(
                        """
                        SELECT *
                        FROM "HOUSE"
                        WHERE "District" = $1;
                        """,
                        dis,
                    )
                    data.extend(sub_data)
                return {
                    "data": data,
                }
            except Exception as e:
                return {
                    "message": f"Error when selecting pre_house: {str(e)}",
                }

    async def get_sleep_time(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Sleep_Time" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"sleep_time": data}
            except Exception as e:
                return {"error": f"Error retrieving sleep time: {str(e)}"}

    async def get_drink(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Drink"
                    FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"drink": data}
            except Exception as e:
                return {"error": f"Error retrieving drink habit: {str(e)}"}

    async def get_smoke(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Smoke"
                    FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"smoke": data}
            except Exception as e:
                return {"error": f"Error retrieving smoke habit: {str(e)}"}

    async def get_clean_habit(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Clean" FROM "PEOPLE" WHERE "People_ID" = $1;
                    """,
                    people_id,
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
                    people_id,
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
                    people_id,
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
                    people_id,
                )
                interests = [
                    key for key, value in data[0].items() if value == 1
                ]  # noqa
                return {"interests": interests}
            except Exception as e:
                return {"error": f"Error retrieving interests: {str(e)}"}

    async def get_size(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Size" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"size": data}
            except Exception as e:
                return {"error": f"Error retrieving size: {str(e)}"}

    async def get_fire(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Fire" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"fire": data}
            except Exception as e:
                return {"error": f"Error retrieving fire: {str(e)}"}

    async def get_negotiate(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Negotiate_Price"
                    FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"negotiate_price": data}
            except Exception as e:
                return {"error": f"Error retrieving negotiate price: {str(e)}"}

    async def get_city(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "City" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"city": data}
            except Exception as e:
                return {"error": f"Error retrieving city: {str(e)}"}

    async def get_district(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "District" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"district": data}
            except Exception as e:
                return {"error": f"Error retrieving district: {str(e)}"}

    async def get_street(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Street" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"street": data}
            except Exception as e:
                return {"error": f"Error retrieving street: {str(e)}"}

    async def get_floor(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Floor" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"floor": data}
            except Exception as e:
                return {"error": f"Error retrieving floor: {str(e)}"}

    async def get_house_type(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetchval(
                    """
                    SELECT "Type" FROM "HOUSE" WHERE "People_ID" = $1;
                    """,
                    people_id,
                )
                return {"type": data}
            except Exception as e:
                return {"error": f"Error retrieving house type: {str(e)}"}

    async def get_house_furniture(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT "Furniture" FROM "HOUSE_FURNITURE"
                    WHERE "House_ID" = (
                        SELECT "House_ID" FROM "HOUSE"
                        WHERE "People_ID" = $1
                        LIMIT 1
                    );
                     """,
                    people_id,
                )
                furniture = [row["Furniture"] for row in data]
                return {"furniture": furniture}
            except Exception as e:
                return {"error": f"Error retrieving house furniture: {str(e)}"}

    async def get_house_traffic(self, people_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT "Traffic" FROM "HOUSE_TRAFFIC"
                    WHERE "House_ID" = (
                    SELECT "House_ID" FROM "HOUSE"
                    WHERE "People_ID" = $1
                    LIMIT 1
                    );
                    """,
                    people_id,
                )
                traffic = [row["Traffic"] for row in data]
                return {"traffic": traffic}
            except Exception as e:
                return {"error": f"Error retrieving house traffic: {str(e)}"}

    async def get_elder_info_by_house_id(self, house_id: int) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    SELECT * FROM "PEOPLE"
                    WHERE "People_ID" = (
                        SELECT "People_ID" FROM "HOUSE"
                        WHERE "House_ID" = $1
                    );
                    """,
                    house_id,
                )
                return data
            except Exception as e:
                return {"error": f"Error retrieving elder info: {str(e)}"}

    async def update_sleep_time(
        self, people_id: int, new_sleep_time: int
    ) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Sleep_Time" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_sleep_time,
                    people_id,
                )
                return {"message": "Sleep time updated successfully"}
            except Exception as e:
                return {"error": f"Error updating sleep time: {str(e)}"}

    async def update_drink_or_smoke(
        self, people_id: int, new_drink_or_smoke: int
    ) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Drink_or_Smoke" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_drink_or_smoke,
                    people_id,
                )
                return {"message": "Drink or smoke habit updated successfully"}
            except Exception as e:
                return {
                    "error": f"Error updating drink or smoke habit: {str(e)}",
                }

    async def update_clean_habit(self, people_id: int, new_clean: int) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    UPDATE "PEOPLE" SET "Clean" = $1 WHERE "People_ID" = $2;
                    """,
                    new_clean,
                    people_id,
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
                    new_mbti,
                    people_id,
                )
                return {"message": "MBTI updated successfully"}
            except Exception as e:
                return {"error": f"Error updating MBTI: {str(e)}"}

    async def add_preference_house_place(
        self, preference_id: int, new_place: list
    ) -> dict:
        async with self.access_db() as conn:
            try:
                for place in new_place:
                    await conn.execute(
                        """
                        INSERT INTO "PREFERENCE_HOUSE_PLACE"
                        ("Preference_ID", "Preference_House_Place")
                        VALUES ($1, $2);
                        """,
                        preference_id,
                        place,
                    )
                return {"message": "Preference house place added successfully"}
            except Exception as e:
                return {
                    "error": f"Error adding preference house place: {str(e)}",
                }

    async def update_integer_field(
        self, column_name: str, people_id: int, new_value: int
    ) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    f"""
                    UPDATE "PEOPLE" SET "{column_name}" = $1
                    WHERE "People_ID" = $2;
                    """,
                    new_value,
                    people_id,
                )
                return {"message": f"{column_name} updated successfully"}
            except Exception as e:
                return {"error": f"Error updating {column_name}: {str(e)}"}

    async def post_user_basic_info(self, user_data: dict) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    INSERT INTO "PEOPLE"
                    ("Name", "Role", "Sleep_Time", "Drink",
                    "Smoke", "Clean", "Mbti", "Shopping", "Movie", "Travel",
                    "Music", "Read", "Game", "PE", "Science", "Food")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                    $13, $14, $15, $16)
                    RETURNING "People_ID"
                    """,
                    user_data["Name"],
                    user_data["Role"],
                    user_data["Sleep_Time"],
                    user_data["Drink"],
                    user_data["Smoke"],
                    user_data["Clean"],
                    user_data["Mbti"],
                    user_data["Shopping"],
                    user_data["Movie"],
                    user_data["Travel"],
                    user_data["Music"],
                    user_data["Read"],
                    user_data["Game"],
                    user_data["PE"],
                    user_data["Science"],
                    user_data["Food"],
                )
                return {
                    "message": "Data inserted successfully",
                    "People_ID": data[0]["People_ID"],
                }
            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def post_house_info(self, house_data: dict) -> dict:
        async with self.access_db() as conn:
            try:
                data = await conn.fetch(
                    """
                    INSERT INTO "HOUSE"
                    ("People_ID", "Size", "Fire", "Negotiate_Price",
                    "City", "District", "Street", "Floor", "Type")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    RETURNING "House_ID"
                    """,
                    house_data["People_ID"],
                    house_data["Size"],
                    house_data["Fire"],
                    house_data["Negotiate_Price"],
                    house_data["City"],
                    house_data["District"],
                    house_data["Street"],
                    house_data["Floor"],
                    house_data["Type"],
                )
                return {
                    "message": "Data inserted successfully",
                    "House_ID": data[0]["House_ID"],
                }
            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def post_house_furniture_info(self, house_furn_data: dict) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                house_id = house_furn_data["House_ID"]
                furniture_list = house_furn_data["Furniture"]
                values = ", ".join(
                    [f"({house_id}, '{furn}')" for furn in furniture_list]
                )  # noqa
                await conn.execute(
                    """
                    INSERT INTO "HOUSE_FURNITURE" ("House_ID", "Furniture")
                    VALUES
                    """
                    + values
                )
                return {
                    "message": "Data inserted successfully",
                }
            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def post_house_traffic_info(self, house_traffic_data: dict) -> dict:  # noqa
        async with self.access_db() as conn:
            try:
                house_id = house_traffic_data["House_ID"]
                values = ", ".join(
                    [
                        f"({house_id}, '{furn}')"
                        for furn in house_traffic_data["Traffic"]
                    ]
                )  # noqa
                await conn.execute(
                    """
                    INSERT INTO "HOUSE_TRAFFIC" ("House_ID", "Traffic")
                    VALUES
                    """
                    + values
                )
                return {
                    "message": "Data inserted successfully",
                }
            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    # Update profile info
    async def update_user_info(self, user_update_data: dict):
        async with self.access_db() as conn:
            try:
                user_id = user_update_data["People_ID"]
                data = user_update_data["data"]
                set_clauses = ", ".join(
                    [f'"{key}" = ${i+2}' for i, key in enumerate(data.keys())]
                )  # noqa

                query = f"""
                UPDATE "PEOPLE"
                SET {set_clauses}
                WHERE "People_ID" = $1
                RETURNING "People_ID"
                """
                values = list(data.values())

                await conn.fetch(query, user_id, *values)

                return {
                    "message": "Data updated successfully",
                }
            except Exception as e:
                return {"message": f"Error when updating data: {str(e)}"}

    async def update_house_info(self, house_update_data: dict):
        async with self.access_db() as conn:
            transaction = conn.transaction()
            await transaction.start()
            try:
                house_id = house_update_data["House_ID"]
                basic = house_update_data["Basic"]
                furniture = house_update_data.get("Furniture", None)
                traffic = house_update_data.get("Traffic", None)

                basic_keys = list(basic.keys())
                basic_values = list(basic.values())

                basic_set_clauses = ", ".join(
                    [f'"{key}" = ${i+2}' for i, key in enumerate(basic_keys)]
                )
                update_query = f"""
                    UPDATE "HOUSE"
                    SET {basic_set_clauses}
                    WHERE "House_ID" = $1
                    RETURNING "House_ID";
                """
                await conn.execute(update_query, house_id, *basic_values)

                # Update `HOUSE FURNITURE` table
                if furniture is not None:
                    await conn.execute(
                        """
                        DELETE FROM "HOUSE_FURNITURE"
                        WHERE "House_ID" = $1
                        """,
                        house_id,
                    )

                    for fur in list(furniture):
                        await conn.execute(
                            """
                            INSERT INTO "HOUSE_FURNITURE" ("House_ID", "Furniture")
                            VALUES ($1, $2)
                            """,
                            house_id,
                            fur,
                        )

                # Update `HOUSE TRAFFIC` table
                if traffic is not None:
                    await conn.execute(
                        """
                        DELETE FROM "HOUSE_TRAFFIC"
                        WHERE "House_ID" = $1
                        """,
                        house_id,
                    )

                    for traff in list(traffic):
                        await conn.execute(
                            """
                            INSERT INTO "HOUSE_TRAFFIC" ("House_ID", "Traffic")
                            VALUES ($1, $2)
                            """,
                            house_id,
                            traff,
                        )

                await transaction.commit()
                return {
                    "message": "Data updated successfully",
                }
            except Exception as e:
                await transaction.rollback()
                return {"message": f"Error when updating data: {str(e)}"}

    # Recommadation
    async def add_recommendation(self, role: int, recommendation_info: dict):
        async with self.access_db() as conn:
            try:
                people_id = recommendation_info["People_ID"]
                item_Ids = recommendation_info["Item_ID"]
                sql = "INSERT INTO "
                if role == 0:
                    sql += '"RECOMMENDATIONS_YOUNG"'
                elif role == 1:
                    sql += '"RECOMMENDATIONS_ELDERLY"'
                else:
                    return {
                        "message": "Please use valid role number, 0 for young and 1 for elderly"  # noqa
                    }

                sql += """ ("People_ID", "Item_ID", "Timestamp")
                        VALUES ($1, $2, CURRENT_TIMESTAMP)
                        """

                for item_id in item_Ids:
                    await conn.execute(
                        sql,
                        people_id,
                        item_id,
                    )

                return {
                    "message": f"People id {people_id}'s recommendation inserted successfully",  # noqa
                }

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def get_recommendation(self, role: int, id: int):
        async with self.access_db() as conn:
            try:
                sql = "SELECT * FROM "
                if role == 0:
                    sql += '"RECOMMENDATIONS_YOUNG"'
                elif role == 1:
                    sql += '"RECOMMENDATIONS_ELDERLY"'
                else:
                    return {
                        "message": "Please use valid role number, 0 for young and 1 for elderly"  # noqa
                    }

                sql += """
                    WHERE "People_ID" = $1
                    ORDER BY "Timestamp" DESC
                    LIMIT 3;
                    """

                data = await conn.fetch(
                    sql,
                    id,
                )

                output = []
                for record in data:
                    record = dict(record)
                    item = await self.get_single_house(int(record["Item_ID"]))
                    item = dict(item[0])
                    item["URL"] = (
                        f"https://form.fang5-group.tw/showotherold?People_ID={item['People_ID']}"
                    )
                    output.append(item)

                return output

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def add_interaction(self, role: int, interaction_info: dict):
        async with self.access_db() as conn:
            try:
                sql = "INSERT INTO "
                if role == 0:
                    sql += """"INTERACTION_YOUNG"
                        ("People_ID", "House_Option_1", "House_Option_2", "House_Option_3", "Interaction_Date")
                        VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
                        RETURNING "Interaction_ID_y"
                        """  # noqa
                    key = "Interaction_ID_y"
                elif role == 1:
                    sql += """"INTERACTION_ELDERLY"
                        ("People_ID", "People_Option_1", "People_Option_2", "People_Option_3", "Interaction_Date")
                        VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP)
                        RETURNING "Interaction_ID_e"
                        """  # noqa
                    key = "Interaction_ID_e"
                else:
                    return {"message": "Please input valid role"}

                data = await conn.fetch(
                    sql,
                    interaction_info["People_ID"],
                    interaction_info["Options"][0],
                    interaction_info["Options"][1],
                    interaction_info["Options"][2],
                )
                return {
                    "message": "Data inserted successfully",
                    "Interaction_ID": data[0][key],
                }

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def add_interaction_detail(self, role: int, detail_info: dict):
        async with self.access_db() as conn:
            try:
                if role == 0:
                    sql = """INSERT INTO "INTERACTION_DETAILS_YOUNG"
                            ("Interaction_ID_y", "Item_ID")
                            VALUES ($1, $2)
                            """  # noqa
                    role = "Young"
                elif role == 1:
                    sql = """INSERT INTO "INTERACTION_DETAILS_ELDERLY"
                            ("Interaction_ID_e", "Item_ID")
                            VALUES ($1, $2)
                            """  # noqa
                    role = "Elderly"
                else:
                    return {"message": "Please input valid role"}
                for option_id in detail_info["Options"]:
                    await conn.execute(
                        sql, detail_info["Interaction_ID"], option_id
                    )  # noqa

                return {
                    "role": role,
                    "message": f"Initial detail for Interaction ID {detail_info['Interaction_ID']} inserted successfully",  # noqa
                }

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def update_field(self, role: int, detail_id: int, field: str):
        valid_fields = ["Viewed", "Grouped", "Selected"]
        if field not in valid_fields:
            return {"message": "Invalid field name"}
        async with self.access_db() as conn:
            try:
                if role == 0:
                    sql = f"""
                        UPDATE "INTERACTION_DETAILS_YOUNG"
                        SET "{field}" = 1
                        WHERE "Detail_ID_y" = $1
                        """
                elif role == 1:
                    sql = f"""
                        UPDATE ""INTERACTION_DETAILS_ELDERLY""
                        SET "{field}" = 1
                        WHERE "Detail_ID_e" = $1
                        """
                else:
                    return {"message": "Please input valid role number"}

                await conn.execute(
                    sql,
                    detail_id,
                )
                return {"message": "Update Successfully"}
            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def get_interaction(self, role: int, detail_id: int):
        async with self.access_db() as conn:
            try:
                if role == 0:
                    sql = """SELECT * FROM "INTERACTION_DETAILS_YOUNG"
                        WHERE "Detail_ID_y" = $1
                        """
                elif role == 1:
                    sql = """SELECT * FROM "INTERACTION_DETAILS_ELDERLY"
                        WHERE "Detail_ID_e" = $1
                        """
                else:
                    return {
                        "message": "Please use valid role number, 0 for young and 1 for elderly"  # noqa
                    }

                data = await conn.fetch(
                    sql,
                    detail_id,
                )

                return data

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}

    async def get_whole_interaction(self, role: int):
        async with self.access_db() as conn:
            try:
                if role == 0:
                    sql = """
                        SELECT
                            inte_y."People_ID", detail_y.*
                        FROM
                            "INTERACTION_DETAILS_YOUNG" AS detail_y
                            LEFT JOIN "INTERACTION_YOUNG" AS inte_y
                            ON detail_y."Interaction_ID_y" = inte_y."Interaction_ID_y"
                        """
                elif role == 1:
                    sql = """
                        SELECT
                            inte_e."People_ID" , detail_e.*
                        FROM
                            "INTERACTION_DETAILS_ELDERLY" AS detail_e
                            LEFT JOIN "INTERACTION_ELDERLY" AS inte_e
                            ON detail_e."Interaction_ID_e" = inte_e."Interaction_ID_e"
                        """
                else:
                    return {
                        "message": "Please use valid role number, 0 for young and 1 for elderly"  # noqa
                    }

                data = await conn.fetch(sql)

                return data

            except Exception as e:
                return {"message": f"Error when inserting data: {str(e)}"}
