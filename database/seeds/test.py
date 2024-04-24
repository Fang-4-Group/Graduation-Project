import psycopg2

# 連接到PostgreSQL
conn = psycopg2.connect(
    host="postgres_db",
    port="5432",
    database="postgres",
    user="riceball",
    password="gp12345",
)

# 創建游標對象
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

# 執行查詢
cursor.execute("SELECT * FROM test_table;")

# 獲取查詢結果
rows = cursor.fetchall()
for row in rows:
    print(row)

# 刪除測試資料表
cursor.execute("DROP TABLE test_table;")

# 關閉游標和連接
cursor.close()
conn.close()
