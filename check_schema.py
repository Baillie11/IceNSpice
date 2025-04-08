import sqlite3

DB_FILE = "challenges.db"

def show_table_info():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("PRAGMA table_info(challenges)")
    columns = c.fetchall()
    print("Current schema for 'challenges' table:")
    for col in columns:
        print(f"{col[1]} - {col[2]}")
    conn.close()

if __name__ == "__main__":
    show_table_info()
