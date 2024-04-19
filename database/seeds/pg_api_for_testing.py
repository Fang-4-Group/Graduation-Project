import psycopg2
from fastapi import HTTPException


async def access_db():
    try:
        # 連接到PostgreSQL
        conn = psycopg2.connect(
            host="postgres_db",
            port="5432",
            database="postgres",
            user="riceball",
            password="gp12345",
        )
        return conn
    except Exception as e:
        # 如果連接發生錯誤，捕獲異常並處理
        error_msg = "Error connecting to db: " + str(e)
        raise HTTPException(status_code=500, detail=error_msg)  # noqa


# Test Create
async def test_create_fun():
    conn = await access_db()
    try:
        cursor = conn.cursor()
        # 建立測試資料表&資料
        cursor.execute(
            """CREATE TABLE test_table (id serial PRIMARY KEY,
                    name VARCHAR(255), age INTEGER);
                    INSERT INTO test_table (name, age) VALUES ('Alice', 25);
                    INSERT INTO test_table (name, age) VALUES ('Bob', 30);
                    INSERT INTO test_table (name, age) VALUES ('Charlie', 28);
                    """
        )
        conn.commit()
        return {"message": "success to create table"}
    except Exception as e:
        error_msg = "Error selecting data: " + str(e)
        raise HTTPException(status_code=500, detail=error_msg)  # noqa
    finally:
        conn.close()


# Test Select
async def test_select_fun():
    conn = await access_db()
    try:
        cursor = conn.cursor()
        # 執行查詢
        cursor.execute("SELECT * FROM test_table;")
        # 獲取查詢結果
        rows = cursor.fetchall()
        data = [{"id": row[0], "name": row[1], "age": row[2]} for row in rows]
        return {"data": data}

    except Exception as e:
        error_msg = "Error selecting data: " + str(e)
        raise HTTPException(status_code=500, detail=error_msg)  # noqa
    finally:
        conn.close()


# Test Drop
async def test_drop_fun():
    conn = await access_db()
    try:
        cursor = conn.cursor()
        # 刪除table
        cursor.execute("DROP TABLE test_table;")
        conn.commit()
        return {"message": "success to delete table"}
    except Exception as e:
        error_msg = "Error selecting data: " + str(e)
        raise HTTPException(status_code=500, detail=error_msg)  # noqa
    finally:
        conn.close()
