from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a strong secret key

DB_FILE = "challenges.db"

# Admin credentials (change as needed)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

def init_db():
    """Creates the challenges table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Drop the old table if it exists (only do this if you're okay with resetting data)
    c.execute("DROP TABLE IF EXISTS challenges")
    
    c.execute('''CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
                    category TEXT NOT NULL CHECK(category IN ('Straight', 'Bi')),
                    challenge_text TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

players = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/game", methods=["GET", "POST"])
def index():
    global players
    if request.method == "POST":
        name = request.form.get("name").strip()
        orientation = request.form.get("orientation")

        if name and orientation:
            # Store player as a dictionary
            players.append({"name": name, "orientation": orientation})

    return render_template("index.html", players=players)

@app.route("/randomize")
def randomize():
    global players
    if players:
        shuffled_players = players[:]  # Copy list to shuffle
        random.shuffle(shuffled_players)
        return render_template("result.html", players=shuffled_players)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global players
    players = []  # Clear player list
    return redirect(url_for("index"))

@app.route("/gameplay")
def gameplay():
    global players
    shuffled_players = players[:]  # Copy list to shuffle
    random.shuffle(shuffled_players)

    # Example: Retrieve a random challenge for round 1, intensity 1
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT challenge_text FROM challenges WHERE round_number = 1 AND intensity = 1 ORDER BY RANDOM() LIMIT 1")
    challenge = c.fetchone()
    conn.close()

    challenge_text = challenge[0] if challenge else "No challenges available."

    return render_template("gameplay.html", players=shuffled_players, challenge=challenge_text)

# ------------------- Admin Panel -------------------

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin_logged_in" not in session:
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if request.method == "POST":
        challenge_text = request.form["challenge_text"].strip()
        intensity = int(request.form["intensity"])
        category = request.form["category"]

        if challenge_text:
            c.execute("INSERT INTO challenges (intensity, category, challenge_text) VALUES (?, ?, ?)", 
                      (intensity, category, challenge_text))
            conn.commit()

    c.execute("SELECT * FROM challenges ORDER BY intensity")
    challenges = c.fetchall()
    conn.close()

    return render_template("admin.html", challenges=challenges)


@app.route("/admin/delete/<int:id>")
def delete_challenge(id):
    if "admin_logged_in" not in session:
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM challenges WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
    
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True)
