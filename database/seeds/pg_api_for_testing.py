import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()


class DatabaseClient:
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

    async def test_create_fun(self) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY,
                        name VARCHAR(255), age INTEGER);
                    INSERT INTO test_table (name, age) VALUES ('Alice', 25);
                    INSERT INTO test_table (name, age) VALUES ('Bob', 30);
                    INSERT INTO test_table (name, age) VALUES ('Charlie', 28);
                    """  # noqa
                )
                return {"status": 200, "message": "success to create table"}
            except Exception as e:
                return {
                    "status": 500,
                    "message": f"Error when creating table: {str(e)}",
                }

    async def test_select_fun(self) -> dict:
        async with self.access_db() as conn:
            try:
                rows = await conn.fetch("SELECT * FROM test_table;")
                data = [
                    {"id": row["id"], "name": row["name"], "age": row["age"]}
                    for row in rows
                ]
                return {"status": 200, "message": data}
            except Exception as e:
                return {
                    "status": 500,
                    "message": f"Error when selecting data: {str(e)}",
                }

    async def test_drop_fun(self) -> dict:
        async with self.access_db() as conn:
            try:
                await conn.execute("DROP TABLE IF EXISTS test_table;")
                return {"status": 200, "message": "success to drop table"}
            except Exception as e:
                return {
                    "status": 500,
                    "message": f"Error when dropping table: {str(e)}",
                }
