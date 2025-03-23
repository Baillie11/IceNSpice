from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Manually force environment variables to load in PythonAnywhere
if "ADMIN_EMAIL" not in os.environ:
    print("⚠️ Environment variables not found. Attempting to load from WSGI...")
    os.environ["ADMIN_EMAIL"] = "andrew@clickecommerce.com.au"
    os.environ["SMTP_SERVER"] = "smtp.gmail.com"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USERNAME"] = "your_email@gmail.com"
    os.environ["SMTP_PASSWORD"] = "your_16_character_app_password"
    os.environ["ADMIN_USERNAME"] = "admin"
    os.environ["ADMIN_PASSWORD"] = "password123"

# Load .env file only for local development
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# Retrieve credentials from environment variables
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Check if all required environment variables are set
missing_vars = [var for var in ["ADMIN_EMAIL", "SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD", "ADMIN_USERNAME", "ADMIN_PASSWORD"] if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. Check your .env file or system environment variables.")

DB_FILE = "challenges.db"

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
current_player_index = 0
current_question_number = 1

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/game", methods=["GET", "POST"])
def index():
    global players, current_player_index, current_question_number

    if request.method == "POST":
        name = request.form.get("name").strip()
        orientation = request.form.get("orientation")

        if name and orientation:
            players.append({"name": name, "orientation": orientation})

    current_player_index = 0
    current_question_number = 1

    return render_template("index.html", players=players)

@app.route("/randomize")
def randomize():
    global players
    if players:
        random.shuffle(players)
        return redirect(url_for("gameplay"))  # 🔁 go to gameplay page instead of result.html
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    global players, current_player_index, current_question_number
    players = []
    current_player_index = 0
    current_question_number = 1
    return redirect(url_for("index"))

@app.route("/gameplay")
def gameplay():
    global players, current_player_index, current_question_number

    if not players:
        return redirect(url_for("index"))

    current_player = players[current_player_index]["name"]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT challenge_text FROM challenges ORDER BY RANDOM() LIMIT 1")
    challenge = c.fetchone()
    conn.close()

    challenge_text = challenge[0] if challenge else "No challenges available."
    challenge_text = challenge_text.replace("USERNAME", current_player)

    return render_template("gameplay.html", players=players, challenge=challenge_text, 
                           current_player=current_player, current_player_index=current_player_index,
                           question_number=current_question_number)

@app.route("/next_turn")
def next_turn():
    global players, current_player_index, current_question_number

    if players:
        current_player_index = (current_player_index + 1) % len(players)
        current_question_number += 1

    return redirect(url_for("gameplay"))

@app.route("/quit")
def quit_game():
    global players, current_player_index, current_question_number
    players = []
    current_player_index = 0
    current_question_number = 1
    return redirect(url_for("index"))

# ------------------- Challenge Suggestion Page -------------------

@app.route("/suggest-challenge", methods=["GET", "POST"])
def suggest_challenge():
    """Handles challenge suggestions from users."""
    if request.method == "POST":
        challenge_idea = request.form.get("challenge_idea")

        if challenge_idea:
            subject = "New Challenge Suggestion for Ice n Spice"
            message = f"New challenge idea submitted:\n\n{challenge_idea}"
            send_email(ADMIN_EMAIL, subject, message)

            flash("Your challenge suggestion has been submitted!", "success")
            return redirect(url_for("suggest_challenge"))

    return render_template("suggest_challenge.html")

def send_email(to_email, subject, message):
    """Function to send emails via SMTP"""
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending email:", e)

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
    """Admin login page."""
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
