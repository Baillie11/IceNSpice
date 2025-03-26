import sqlite3

conn = sqlite3.connect("challenges.db")
c = conn.cursor()

# Create a new table with updated pairing CHECK constraint including 'All'
c.execute('''
    CREATE TABLE IF NOT EXISTS challenges_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
        orientation TEXT NOT NULL CHECK(orientation IN ('Straight', 'Bi')),
        pairing TEXT NOT NULL CHECK(pairing IN (
            'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female', 'All'
        )),
        challenge_text TEXT NOT NULL
    )
''')

# Copy data from old table
c.execute('''
    INSERT INTO challenges_new (id, intensity, orientation, pairing, challenge_text)
    SELECT id, intensity, orientation, pairing, challenge_text FROM challenges
''')

# Drop old table and rename new one
c.execute('DROP TABLE challenges')
c.execute('ALTER TABLE challenges_new RENAME TO challenges')

conn.commit()
conn.close()

print("✅ Updated pairing field to include 'All'.")