import sqlite3

DB_FILE = "challenges.db"

def update_schema():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Rename old table
    c.execute("ALTER TABLE challenges RENAME TO challenges_old")

    # Create new table with updated orientation options
    c.execute('''
        CREATE TABLE challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
            orientation TEXT NOT NULL CHECK(orientation IN ('All', 'Straight', 'Bi', 'Gay', 'Lesbian')),
            pairing TEXT NOT NULL CHECK(pairing IN (
                'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female', 'All'
            )),
            challenge_text TEXT NOT NULL
        )
    ''')

    # Copy data from old table into new table
    c.execute('''
        INSERT INTO challenges (id, intensity, orientation, pairing, challenge_text)
        SELECT id, intensity, orientation, pairing, challenge_text FROM challenges_old
    ''')

    # Drop old table
    c.execute("DROP TABLE challenges_old")

    conn.commit()
    conn.close()
    print("Schema updated successfully.")

if __name__ == "__main__":
    update_schema()
