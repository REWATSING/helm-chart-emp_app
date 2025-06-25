# app-code/backend/init_db.py

import pymysql
import time
import os

def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "rootpass"),
        database=os.getenv("DB_NAME", "empdb"),
        cursorclass=pymysql.cursors.DictCursor
    )

for i in range(10):
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100)
                )
            """)
        conn.commit()
        print("✅ Table created successfully.")
        break
    except Exception as e:
        print(f"⏳ Attempt {i+1}: {e}")
        time.sleep(5)

