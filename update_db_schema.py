import sqlite3

# Connect to the existing database
conn = sqlite3.connect("challenges.db")
c = conn.cursor()

# Create new table with 'pairing' field
c.execute('''
    CREATE TABLE IF NOT EXISTS challenges_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
        category TEXT NOT NULL CHECK(category IN ('Straight', 'Bi')),
        pairing TEXT NOT NULL CHECK(pairing IN (
            'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female'
        )),
        challenge_text TEXT NOT NULL
    )
''')

# Copy data from old table into new table with a default pairing
c.execute('''
    INSERT INTO challenges_new (id, intensity, category, pairing, challenge_text)
    SELECT id, intensity, category, 'Male to Female', challenge_text FROM challenges
''')

# Drop old table and rename new one
c.execute('DROP TABLE challenges')
c.execute('ALTER TABLE challenges_new RENAME TO challenges')

conn.commit()
conn.close()

print("✅ Database schema updated successfully.")
