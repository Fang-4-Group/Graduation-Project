import json
import logging
import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PosgresqlInitClient:
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

    async def create_table(self):
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    DROP SCHEMA public CASCADE;
                    CREATE SCHEMA public;
                    CREATE TABLE IF NOT EXISTS "PEOPLE" (
                        "People_ID" SERIAL PRIMARY KEY,
                        "Line_ID" varchar,
                        "Name" varchar,
                        "Role" integer,
                        "Mail" varchar,
                        "Sleep_Time" integer,
                        "Drink" integer,
                        "Smoke" integer,
                        "Clean" integer,
                        "Mbti" varchar,
                        "Shopping" integer,
                        "Movie" integer,
                        "Travel" integer,
                        "Music" integer,
                        "Read" integer,
                        "Game" integer,
                        "PE" integer,
                        "Science" integer,
                        "Food" integer
                    );

                    CREATE TABLE IF NOT EXISTS "PEOPLE_CHARACTER" (
                        "People_ID" integer,
                        "Character" varchar,
                        PRIMARY KEY ("People_ID", "Character")
                    );

                    CREATE TABLE IF NOT EXISTS "HOUSE" (
                        "House_ID" SERIAL PRIMARY KEY,
                        "People_ID" integer,
                        "Size" float,
                        "Fire" integer,
                        "Negotiate_Price" integer,
                        "Photo" varchar,
                        "City" varchar,
                        "District" varchar,
                        "Street" varchar,
                        "Floor" integer,
                        "Type" varchar
                    );

                    CREATE TABLE IF NOT EXISTS "HOUSE_FURNITURE" (
                        "House_ID" integer,
                        "Furniture" varchar,
                        PRIMARY KEY ("House_ID", "Furniture")
                    );

                    CREATE TABLE IF NOT EXISTS "HOUSE_TRAFFIC" (
                        "House_ID" integer,
                        "Traffic" varchar,
                        PRIMARY KEY ("House_ID", "Traffic")
                    );

                    CREATE TABLE IF NOT EXISTS "PREFERENCE" (
                        "Preference_ID" integer PRIMARY KEY,
                        "People_ID" integer
                    );

                    CREATE TABLE IF NOT EXISTS "PREFERENCE_HOUSE_PLACE" (
                    "Preference_ID" integer,
                    "Preference_House_Place" varchar,
                    PRIMARY KEY ("Preference_ID", "Preference_House_Place")
                    );

                    CREATE TABLE "DISTRICT_LOCATIONS" (
                        "ID" SERIAL PRIMARY KEY,
                        "City" VARCHAR(50),
                        "District" VARCHAR(50),
                        "Longitude" FLOAT,
                        "Latitude" FLOAT
                    );

                    CREATE TABLE IF NOT EXISTS "RECOMMENDATIONS_YOUNG" (
                        "Recommendation_ID" SERIAL PRIMARY KEY,
                        "People_ID" INT,
                        "Item_ID" INT,
                        "Score" FLOAT,
                        "Timestamp" TIMESTAMP,
                        FOREIGN KEY ("People_ID") REFERENCES "PEOPLE" ("People_ID"),
                        FOREIGN KEY ("Item_ID") REFERENCES "HOUSE" ("House_ID")
                    );

                    CREATE TABLE IF NOT EXISTS "RECOMMENDATIONS_ELDERLY" (
                        "Recommendation_ID" SERIAL PRIMARY KEY,
                        "People_ID" INT,
                        "Item_ID" INT,
                        "Score" FLOAT,
                        "Timestamp" TIMESTAMP,
                        FOREIGN KEY ("People_ID") REFERENCES "PEOPLE" ("People_ID"),
                        FOREIGN KEY ("Item_ID") REFERENCES "PEOPLE" ("People_ID")
                    );

                    CREATE TABLE "INTERACTION_YOUNG" (
                        "Interaction_ID_y" SERIAL PRIMARY KEY,
                        "People_ID" INT,
                        "House_Option_1" INT,
                        "House_Option_2" INT,
                        "House_Option_3" INT,
                        "Interaction_Date" TIMESTAMP,
                        FOREIGN KEY ("People_ID") REFERENCES "PEOPLE"("People_ID"),
                        FOREIGN KEY ("House_Option_1") REFERENCES "HOUSE"("House_ID"),
                        FOREIGN KEY ("House_Option_2") REFERENCES "HOUSE"("House_ID"),
                        FOREIGN KEY ("House_Option_3") REFERENCES "HOUSE"("House_ID")
                    );

                    CREATE TABLE "INTERACTION_DETAILS_YOUNG" (
                        "Detail_ID_y" SERIAL PRIMARY KEY,
                        "Interaction_ID_y" INT,
                        "Item_ID" INT,
                        "Viewed"  INT DEFAULT 0,
                        "Grouped" INT DEFAULT 0,
                        "Selected" INT DEFAULT 0,
                        FOREIGN KEY ("Interaction_ID_y") REFERENCES "INTERACTION_YOUNG"("Interaction_ID_y"),
                        FOREIGN KEY ("Item_ID") REFERENCES "HOUSE"("House_ID")
                    );

                    CREATE TABLE "INTERACTION_ELDERLY" (
                        "Interaction_ID_e" SERIAL PRIMARY KEY,
                        "People_ID" INT,
                        "People_Option_1" INT,
                        "People_Option_2" INT,
                        "People_Option_3" INT,
                        "Interaction_Date" TIMESTAMP,
                        FOREIGN KEY ("People_ID") REFERENCES "PEOPLE"("People_ID"),
                        FOREIGN KEY ("People_Option_1") REFERENCES "PEOPLE"("People_ID"),
                        FOREIGN KEY ("People_Option_2") REFERENCES "PEOPLE"("People_ID"),
                        FOREIGN KEY ("People_Option_3") REFERENCES "PEOPLE"("People_ID")
                    );

                    CREATE TABLE "INTERACTION_DETAILS_ELDERLY" (
                        "Detail_ID_e" SERIAL PRIMARY KEY,
                        "Interaction_ID_e" INT,
                        "Item_ID" INT,
                        "Viewed" INT DEFAULT 0,
                        "Grouped" INT DEFAULT 0,
                        "Selected" INT DEFAULT 0,
                        FOREIGN KEY ("Interaction_ID_e") REFERENCES "INTERACTION_ELDERLY"("Interaction_ID_e"),
                        FOREIGN KEY ("Item_ID") REFERENCES "PEOPLE"("People_ID")
                    );
                    """  # noqa
                )
                return {"message": "success to create all tables"}
            except Exception as e:
                return {
                    "status": 500,
                    "message": f"Error when creating table: {str(e)}",
                }

    async def add_fk_setting(self):
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    ALTER TABLE "HOUSE" ADD FOREIGN KEY ("People_ID") REFERENCES "PEOPLE" ("People_ID");

                    ALTER TABLE "PEOPLE_CHARACTER" ADD FOREIGN KEY ("People_ID") REFERENCES "PEOPLE" ("People_ID");

                    ALTER TABLE "PREFERENCE" ADD FOREIGN KEY ("People_ID") REFERENCES "PEOPLE" ("People_ID");

                    ALTER TABLE "PREFERENCE_HOUSE_PLACE" ADD FOREIGN KEY ("Preference_ID") REFERENCES "PREFERENCE" ("Preference_ID");

                    ALTER TABLE "HOUSE_FURNITURE" ADD FOREIGN KEY ("House_ID") REFERENCES "HOUSE" ("House_ID");

                    ALTER TABLE "HOUSE_TRAFFIC" ADD FOREIGN KEY ("House_ID") REFERENCES "HOUSE" ("House_ID");
                    """  # noqa
                )
                return {
                    "message": "success to set FK",
                }
            except Exception as e:
                return {
                    "message": f"Error when setting FK: {str(e)}",
                }

    async def insert_data(self):
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO "PEOPLE" ("Name", "Line_ID", "Role", "Sleep_Time", "Drink", "Smoke", "Clean", "Mbti", "Shopping", "Movie", "Travel", "Music", "Read", "Game", "PE", "Science", "Food", "Mail")
                    VALUES
                    ('AA', 'fake_line_id', 1, 3, 2, 0, 4, 'INTJ', 0, 1, 0, 0, 0, 0, 0, 1, 0, 'sample@.google.com'),
                    ('BB', 'fake_line_id', 0, 4, 1, 3, 3, 'INFP', 1, 1, 0, 1, 1, 0, 0, 0, 1, 'sample@.google.com'),
                    ('CC', 'fake_line_id', 1, 2, 3, 1, 5, 'ISTJ', 0, 1, 1, 0, 0, 0, 1, 0, 0, 'sample@.google.com'),
                    ('DD', 'fake_line_id', 0, 4, 1, 3, 3, 'INFP', 1, 1, 0, 0, 1, 0, 0, 0, 1, 'sample@.google.com'),
                    ('EE', 'fake_line_id', 1, 4, 1, 2, 5, 'ENTP', 0, 1, 1, 0, 1, 0, 1, 1, 0, 'sample@.google.com'),
                    ('FF', 'fake_line_id', 0, 2, 3, 4, 0, 'ESFP', 1, 1, 0, 1, 0, 0, 0, 0, 1, 'sample@.google.com'),
                    ('GG', 'fake_line_id', 1, 3, 2, 2, 3, 'ESTJ', 0, 0, 1, 0, 1, 1, 1, 0, 0, 'sample@.google.com'),
                    ('HH', 'fake_line_id', 0, 4, 1, 2, 5, 'ENFJ', 0, 1, 0, 0, 1, 0, 0, 0, 1, 'sample@.google.com'),
                    ('II', 'fake_line_id', 1, 2, 3, 1, 4, 'ENTJ', 0, 1, 1, 0, 0, 0, 1, 1, 0, 'sample@.google.com'),
                    ('JJ', 'fake_line_id', 0, 2, 3, 4, 0, 'ISFP', 1, 1, 0, 1, 0, 0, 1, 0, 1, 'sample@.google.com');

                    INSERT INTO "PEOPLE_CHARACTER" ("People_ID", "Character")
                    VALUES
                    (1, '細心'),
                    (1, '有條理'),
                    (2, '友善'),
                    (2, '細心'),
                    (2, '有條理'),
                    (3, '有條理'),
                    (4, '活潑'),
                    (4, '善於社交'),
                    (5, '樂觀'),
                    (5, '有條理'),
                    (6, '喜歡冒險'),
                    (6, '活潑'),
                    (7, '務實'),
                    (8, '務實'),
                    (9, '活潑'),
                    (9, '喜歡冒險'),
                    (10, '善於社交'),
                    (10, '友善');

                    INSERT INTO "HOUSE" ("People_ID", "Size", "Fire", "Negotiate_Price", "Photo", "City", "District", "Street", "Floor", "Type")
                    VALUES
                    (1, 12.5, 0, 1, 'house1.jpg', '臺北市', '大安區', '新生南路', 2, '公寓'),
                    (1, 12.5, 0, 1, 'house1.jpg', '臺北市', '大安區', '新生南路', 2, '公寓'),
                    (3, 12.2, 0, 1, 'house2.jpg', '臺北市', '文山區', '木柵路', 2, '公寓'),
                    (3, 13, 0, 1, 'house6.jpg', '臺北市', '文山區', '木柵路', 2, '公寓'),
                    (5, 10, 0, 1, 'house3.jpg', '新北市', '新店區', '北宜路', 3, '華廈'),
                    (5, 12, 0, 1, 'house11.jpg', '新北市', '新店區', '北宜路', 3, '華廈'),
                    (7, 18.3, 1, 0, 'house4.jpg', '臺北市', '北投區', '石牌路', 2, '大樓'),
                    (9, 10, 0, 1, 'house5.jpg', '臺北市', '士林區', '中正路', 3, '華廈'),
                    (5, 8, 0, 1, 'house7.jpg', '新北市', '新店區', '北宜路', 2, '華廈'),
                    (7, 12, 1, 0, 'house8.jpg', '臺北市', '北投區', '石牌路', 2, '大樓'),
                    (9, 10, 0, 1, 'house9.jpg', '臺北市', '士林區', '中正路', 1, '公寓');

                    INSERT INTO "HOUSE_FURNITURE" ("House_ID", "Furniture")
                    VALUES
                    (1, '衣櫃'),
                    (1, '茶几'),
                    (1, '床'),
                    (2, '床'),
                    (2, '書桌'),
                    (3, '書架'),
                    (3, '書桌'),
                    (4, '書架'),
                    (4, '書桌'),
                    (4, '床'),
                    (5, '衣櫃'),
                    (5, '床');

                    INSERT INTO "HOUSE_TRAFFIC" ("House_ID", "Traffic")
                    VALUES
                    (1, '捷運'),
                    (2, '公車'),
                    (3, '捷運'),
                    (4, '公車'),
                    (5, '捷運');

                    INSERT INTO "PREFERENCE" ("Preference_ID", "People_ID")
                    VALUES
                    (1, 2),
                    (2, 4),
                    (3, 6),
                    (4, 8),
                    (5, 10);

                    INSERT INTO "PREFERENCE_HOUSE_PLACE" ("Preference_ID", "Preference_House_Place")
                    VALUES
                    (1, '大安區'),
                    (1, '文山區'),
                    (2, '大安區'),
                    (2, '文山區'),
                    (3, '新店區'),
                    (4, '士林區'),
                    (4, '北投區'),
                    (5, '新店區');

                    INSERT INTO "INTERACTION_YOUNG" ("People_ID", "House_Option_1", "House_Option_2", "House_Option_3", "Interaction_Date")
                    VALUES
                    (2, 2, 3, 4, NOW()),
                    (10, 5, 6, 8, NOW()),
                    (4, 5, 6, 8, NOW());

                    INSERT INTO "INTERACTION_DETAILS_YOUNG" ("Interaction_ID_y", "Item_ID", "Viewed", "Grouped", "Selected")
                    VALUES
                    (1, 2, 1, 1, 0),
                    (1, 3, 1, 0, 0),
                    (1, 4, 1, 1, 1),
                    (2, 5, 1, 0, 0),
                    (2, 6, 1, 1, 1),
                    (2, 8, 0, 0, 0),
                    (3, 2, 0, 0, 0),
                    (3, 3, 1, 0, 0),
                    (3, 4, 1, 1, 1);

                    INSERT INTO "INTERACTION_ELDERLY" ("People_ID", "People_Option_1", "People_Option_2", "People_Option_3", "Interaction_Date")
                    VALUES
                    (1, 2, 4, 10, NOW()),
                    (3, 2, 8, 10, NOW());

                    INSERT INTO "INTERACTION_DETAILS_ELDERLY" ("Interaction_ID_e", "Item_ID", "Viewed", "Grouped", "Selected")
                    VALUES
                    (1, 2, 1, 0, 0),
                    (1, 4, 1, 0, 0),
                    (1, 10, 0, 0, 0),
                    (2, 2, 1, 0, 0),
                    (2, 8, 1, 1, 0),
                    (2, 10, 0, 0, 0);
                    """  # noqa
                )
                return {
                    "message": "success to insert data",
                }
            except Exception as e:
                return {
                    "message": f"Error when inserting data: {str(e)}",
                }

    async def insert_district_data(self):
        async with self.access_db() as conn:
            try:
                json_file_path = [
                    r"database/migrations/data/lat_lon_data/taipei_district_lat_lon.json",
                    r"database/migrations/data/lat_lon_data/newtaipei_district_lat_lon.json",  # noqa
                ]
                for path in json_file_path:
                    with open(path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                    for entry in data["data"]:
                        await conn.execute(
                            """
                            INSERT INTO
                                "DISTRICT_LOCATIONS" ("City", "District", "Longitude", "Latitude")
                            VALUES
                                ($1, $2, $3, $4)
                            """,  # noqa
                            entry["City"],
                            entry["District"],
                            entry["Longitude"],
                            entry["Latitude"],
                        )
                return {
                    "message": "success to insert district data",
                }
            except Exception as e:
                return {
                    "message": f"Error when inserting data: {str(e)}",
                }

    async def select_house_data(self):
        async with self.access_db() as conn:
            try:
                rows = await conn.fetch('SELECT * FROM "HOUSE";')
                data = [
                    {
                        "House_ID": row["House_ID"],
                        "People_ID": row["People_ID"],
                        "Size": row["Size"],
                    }
                    for row in rows
                ]
                return {"message": data}
            except Exception as e:
                return {
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def insert_data_by_sql_file(self):
        async with self.access_db() as conn:
            try:
                directory = "database/migrations/data/sample_data"
                sql_files = [
                    "people.sql",
                    "house.sql",
                    "interaction_young.sql",
                    "other.sql",
                ]
                sql_statements = []
                for filename in sql_files:
                    logger.info(filename)
                    file_path = os.path.join(directory, filename)
                    with open(file_path, "r") as file:
                        sql_statements.append(file.read())

                for script in sql_statements:
                    commands = script.split(";")
                    for command in commands:
                        command = command.strip()
                        if command:
                            await conn.execute(command)
                return {
                    "message": "success to insert data",
                }
            except Exception as e:
                return {
                    "message": f"Error when inserting data by sql: {str(e)}",
                }
