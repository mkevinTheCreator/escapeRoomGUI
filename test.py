import sqlite3
CONFIG = {
    "database_path": "G:/zigpy_db/zigbee.db",  
}
conn = sqlite3.connect(CONFIG["database_path"])
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

for table, in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cursor.fetchone()[0]} rows")

conn.close()
