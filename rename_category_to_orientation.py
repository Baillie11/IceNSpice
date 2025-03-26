import sqlite3

conn = sqlite3.connect("challenges.db")
c = conn.cursor()

# Create a new table with 'orientation' instead of 'category'
c.execute('''
    CREATE TABLE IF NOT EXISTS challenges_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
        orientation TEXT NOT NULL CHECK(orientation IN ('Straight', 'Bi')),
        pairing TEXT NOT NULL CHECK(pairing IN (
            'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female'
        )),
        challenge_text TEXT NOT NULL
    )
''')

# Copy data, renaming the column from 'category' to 'orientation'
c.execute('''
    INSERT INTO challenges_new (id, intensity, orientation, pairing, challenge_text)
    SELECT id, intensity, category, pairing, challenge_text FROM challenges
''')

# Replace old table with the new one
c.execute('DROP TABLE challenges')
c.execute('ALTER TABLE challenges_new RENAME TO challenges')

conn.commit()
conn.close()

print("✅ Renamed 'category' to 'orientation' successfully.")