import MySQLdb
import sys

print("Testing connection to MySQL server at 127.0.0.1:3306...")
try:
    # Try connecting to the server without a specific database
    db = MySQLdb.connect(
        host="127.0.0.1",
        user="root",
        passwd="",
        port=3306
    )
    print("SUCCESS: Connected to MySQL server!")
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [d[0] for d in cursor.fetchall()]
    print("Available databases:", databases)
    if 'medikit' in databases:
        print("Database 'medikit' exists.")
    else:
        print("Database 'medikit' DOES NOT exist. You may need to create it.")
    db.close()
except Exception as e:
    print(f"FAILED: Could not connect to MySQL server. Error: {e}")
