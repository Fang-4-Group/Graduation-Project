import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()


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
                    CREATE TABLE IF NOT EXISTS "PEOPLE" (
                        "People_ID" integer PRIMARY KEY,
                        "Role" integer,
                        "Sleep_Time" integer,
                        "Drink_or_Smoke" integer,
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
                        "House_ID" integer PRIMARY KEY,
                        "People_ID" integer,
                        "Size" float,
                        "Fire" integer,
                        "Negotiate_Price" integer,
                        "Photo" varchar,
                        "Address" varchar,
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

                    CREATE TABLE IF NOT EXISTS "PREFERENCE_HOUSE_FURNITURE" (
                        "Preference_ID" integer,
                        "Preference_House_Furniture" varchar,
                        PRIMARY KEY ("Preference_ID", "Preference_House_Furniture")
                    );

                    CREATE TABLE IF NOT EXISTS "PREFERENCE_HOUSE_PLACE" (
                    "Preference_ID" integer,
                    "Preference_House_Place" varchar,
                    PRIMARY KEY ("Preference_ID", "Preference_House_Place")
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

                    ALTER TABLE "PREFERENCE_HOUSE_FURNITURE" ADD FOREIGN KEY ("Preference_ID") REFERENCES "PREFERENCE" ("Preference_ID");

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
                    INSERT INTO "PEOPLE" ("People_ID", "Role", "Sleep_Time", "Drink_or_Smoke", "Clean", "Mbti", "Shopping", "Movie", "Travel", "Music", "Read", "Game", "PE", "Science", "Food")
                    VALUES
                    (1, 1, 3, 2, 4, 'INTJ', 0, 1, 1, 0, 1, 0, 1, 1, 0),
                    (2, 0, 4, 1, 3, 'INFP', 1, 1, 0, 1, 1, 0, 0, 0, 1),
                    (3, 1, 2, 3, 5, 'ISTJ', 0, 1, 1, 0, 1, 0, 1, 1, 0),
                    (4, 0, 3, 2, 4, 'ENFP', 1, 1, 0, 1, 1, 0, 0, 0, 1),
                    (5, 1, 4, 1, 5, 'ENTP', 0, 1, 1, 0, 1, 0, 1, 1, 0),
                    (6, 0, 2, 3, 4, 'ISFP', 1, 1, 0, 1, 1, 0, 0, 0, 1),
                    (7, 1, 3, 2, 3, 'ESTJ', 0, 1, 1, 0, 1, 0, 1, 1, 0),
                    (8, 0, 4, 1, 5, 'INFJ', 1, 1, 0, 1, 1, 0, 0, 0, 1),
                    (9, 1, 2, 3, 4, 'ENTJ', 0, 1, 1, 0, 1, 0, 1, 1, 0),
                    (10, 0, 3, 2, 3, 'ESFP', 1, 1, 0, 1, 1, 0, 0, 0, 1);

                    INSERT INTO "PEOPLE_CHARACTER" ("People_ID", "Character")
                    VALUES
                    (1, 'Detail-oriented'),
                    (2, 'Empathetic'),
                    (3, 'Organized'),
                    (4, 'Creative'),
                    (5, 'Analytical'),
                    (6, 'Adventurous'),
                    (7, 'Practical'),
                    (8, 'Idealistic'),
                    (9, 'Strategic'),
                    (10, 'Social');

                    INSERT INTO "HOUSE" ("House_ID", "People_ID", "Size", "Fire", "Negotiate_Price", "Photo", "Address", "Floor", "Type")
                    VALUES
                    (1, 1, 120.5, 0, 1, 'house1.jpg', '123 Main St', 2, 'Apartment'),
                    (2, 3, 150.2, 1, 0, 'house2.jpg', '456 Elm St', 1, 'Condo'),
                    (3, 5, 200.0, 0, 1, 'house3.jpg', '789 Oak St', 3, 'House'),
                    (4, 7, 180.3, 1, 0, 'house4.jpg', '101 Pine St', 2, 'Townhouse'),
                    (5, 9, 220.7, 0, 1, 'house5.jpg', '222 Cedar St', 1, 'Apartment');

                    INSERT INTO "HOUSE_FURNITURE" ("House_ID", "Furniture")
                    VALUES
                    (1, 'Sofa'),
                    (1, 'Coffee Table'),
                    (1, 'TV Stand'),
                    (2, 'Bed'),
                    (2, 'Dining Table'),
                    (3, 'Wardrobe'),
                    (3, 'Study Desk'),
                    (4, 'Bookshelf'),
                    (4, 'Computer Desk'),
                    (5, 'Kitchen Island'),
                    (5, 'Armchair');

                    INSERT INTO "HOUSE_TRAFFIC" ("House_ID", "Traffic")
                    VALUES
                    (1, 'MRT'),
                    (2, 'Bus'),
                    (3, 'MRT'),
                    (4, 'Bus'),
                    (5, 'MRT');

                    INSERT INTO "PREFERENCE" ("Preference_ID", "People_ID")
                    VALUES
                    (1, 2),
                    (2, 4),
                    (3, 6),
                    (4, 8),
                    (5, 10);

                    INSERT INTO "PREFERENCE_HOUSE_FURNITURE" ("Preference_ID", "Preference_House_Furniture")
                    VALUES
                    (1, 'Desk'),
                    (2, 'Bed'),
                    (3, 'Sofa'),
                    (4, 'Dining Table'),
                    (5, 'Bookshelf');

                    INSERT INTO "PREFERENCE_HOUSE_PLACE" ("Preference_ID", "Preference_House_Place")
                    VALUES
                    (1, 'Daan District'),
                    (2, 'Zhongzheng District'),
                    (3, 'Xinyi District'),
                    (4, 'Wanhua District'),
                    (5, 'Datong District');
                    """  # noqa
                )
                return {
                    "message": "success to insert data",
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
