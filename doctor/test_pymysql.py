import pymysql
import sys

print("Testing connection to MySQL server using PyMySQL...")
try:
    db = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        port=3306,
        connect_timeout=5
    )
    print("SUCCESS: Connected to MySQL server using PyMySQL!")
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [d[0] for d in cursor.fetchall()]
    print("Available databases:", databases)
    db.close()
except Exception as e:
    print(f"FAILED: Could not connect to MySQL server using PyMySQL. Error: {e}")
