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
current_player_index = 0  # Track which player's turn it is

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
        random.shuffle(players)
        return render_template("result.html", players=players)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global players, current_player_index
    players = []  # Clear player list
    current_player_index = 0  # Reset turn order
    return redirect(url_for("index"))

@app.route("/gameplay")
def gameplay():
    global players, current_player_index

    if not players:
        return redirect(url_for("index"))

    # Get the current player's name
    current_player = players[current_player_index]["name"]

    # Fetch a random challenge
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT challenge_text FROM challenges ORDER BY RANDOM() LIMIT 1")
    challenge = c.fetchone()
    conn.close()

    challenge_text = challenge[0] if challenge else "No challenges available."

    # Replace USERNAME with the current player's name
    challenge_text = challenge_text.replace("USERNAME", current_player)

    return render_template("gameplay.html", players=players, challenge=challenge_text, current_player=current_player)

@app.route("/next_turn")
def next_turn():
    global players, current_player_index

    if players:
        # Move to the next player (loop back if at the end)
        current_player_index = (current_player_index + 1) % len(players)

    return redirect(url_for("gameplay"))

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
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
