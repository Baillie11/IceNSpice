from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
if os.path.exists(".env"):
    load_dotenv()

# Defaults for PythonAnywhere (in case)
if "ADMIN_EMAIL" not in os.environ:
    os.environ["ADMIN_EMAIL"] = "andrew@clickecommerce.com.au"
    os.environ["SMTP_SERVER"] = "smtp.gmail.com"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USERNAME"] = "your_email@gmail.com"
    os.environ["SMTP_PASSWORD"] = "your_app_password"
    os.environ["ADMIN_USERNAME"] = "admin"
    os.environ["ADMIN_PASSWORD"] = "password123"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# Environment Variables
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

required_vars = [ADMIN_EMAIL, SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, ADMIN_USERNAME, ADMIN_PASSWORD]
if not all(required_vars):
    raise ValueError("Missing required environment variables. Check your .env or system environment variables.")

DB_FILE = "challenges.db"
players = []
current_player_index = 0
current_question_number = 1
current_round = 1

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
            orientation TEXT NOT NULL CHECK(orientation IN ('Straight', 'Bi')),
            pairing TEXT NOT NULL CHECK(pairing IN (
                'Male to Female', 'Female to Male', 'Male to Male', 'Female to Female', 'All'
            )),
            challenge_text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/game", methods=["GET", "POST"])
def index():
    global players, current_player_index, current_question_number, current_round
    if request.method == "POST":
        name = request.form.get("name").strip()
        orientation = request.form.get("orientation")
        sex = request.form.get("sex")
        partner = request.form.get("partner") or None
        if name and orientation and sex:
            players.append({
                "name": name,
                "orientation": orientation,
                "sex": sex,
                "partner": partner
            })
    current_player_index = 0
    current_question_number = 1
    current_round = 1
    return render_template("index.html", players=players)

@app.route("/randomize")
def randomize():
    global players
    if players:
        random.shuffle(players)
        return redirect(url_for("gameplay"))
    return redirect(url_for("index"))

@app.route("/gameplay")
def gameplay():
    global players, current_player_index, current_question_number, current_round
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
                           question_number=current_question_number, round_number=current_round)

@app.route("/next_turn", methods=["POST"])
def next_turn():
    global players, current_player_index, current_question_number, current_round
    if players:
        current_player_index = (current_player_index + 1) % len(players)
        current_question_number += 1

        total_questions = len(players) * 2
        if current_question_number > total_questions:
            if current_round < 10:
                current_round += 1
                current_question_number = 1
            else:
                return redirect(url_for("home"))  # Game over after round 10

    return redirect(url_for("gameplay"))

@app.route("/quit")
def quit_game():
    global players, current_player_index, current_question_number, current_round
    players = []
    current_player_index = 0
    current_question_number = 1
    current_round = 1
    return redirect(url_for("home"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if request.method == "POST":
        challenge_text = request.form["challenge_text"].strip()
        intensity = int(request.form["intensity"])
        orientation = request.form["orientation"]
        pairing = request.form["pairing"]
        if challenge_text:
            c.execute("INSERT INTO challenges (intensity, orientation, pairing, challenge_text) VALUES (?, ?, ?, ?)",
                      (intensity, orientation, pairing, challenge_text))
            conn.commit()

    c.execute("SELECT * FROM challenges")
    challenges = c.fetchall()
    conn.close()

    return render_template("admin.html", challenges=challenges)

@app.route("/delete/<int:id>")
def delete_challenge(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM challenges WHERE id = ?", (id,))
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

@app.route("/suggest-challenge", methods=["GET", "POST"])
def suggest_challenge():
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

if __name__ == "__main__":
    app.run(debug=True)
