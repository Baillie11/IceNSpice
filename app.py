from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import csv
from io import TextIOWrapper

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
            orientation TEXT NOT NULL CHECK(orientation IN ('All', 'Straight', 'Bi', 'Gay', 'Lesbian')),
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

def get_matching_player(current_player, pairing):
    potential = []
    current_name = current_player['name']
    current_sex = current_player['sex']
    current_orientation = current_player['orientation']
    current_partner = current_player.get('partner')

    for p in players:
        if p['name'] == current_name:
            continue
        if current_partner and p['name'] == current_partner:
            continue

        match = False
        if pairing == "Male to Female" and current_sex == "Male" and p['sex'] == "Female":
            match = True
        elif pairing == "Female to Male" and current_sex == "Female" and p['sex'] == "Male":
            match = True
        elif pairing == "Male to Male" and current_sex == "Male" and p['sex'] == "Male":
            match = True
        elif pairing == "Female to Female" and current_sex == "Female" and p['sex'] == "Female":
            match = True
        elif pairing == "All":
            match = True

        if match:
            if current_orientation == "Straight" and pairing in ["Male to Male", "Female to Female"]:
                continue
            if current_orientation == "Gay" and (pairing not in ["Male to Male"] or p['sex'] != "Male"):
                continue
            if current_orientation == "Lesbian" and (pairing not in ["Female to Female"] or p['sex'] != "Female"):
                continue
            potential.append(p['name'])

    return random.choice(potential) if potential else None

@app.route("/gameplay")
def gameplay():
    global players, current_player_index, current_question_number, current_round
    if not players:
        return redirect(url_for("index"))

    current_player = players[current_player_index]
    current_name = current_player['name']

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT challenge_text, pairing FROM challenges ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        challenge_text, pairing = row
        partner_name = get_matching_player(current_player, pairing)
        challenge_text = challenge_text.replace("USERNAME", current_name)
        challenge_text = challenge_text.replace("PARTNERNAME", partner_name if partner_name else "someone")
    else:
        challenge_text = "No challenges available."

    return render_template("gameplay.html", players=players, challenge=challenge_text,
                           current_player=current_name, current_player_index=current_player_index,
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
                return redirect(url_for("home"))

    return redirect(url_for("gameplay"))

@app.route("/skip_round", methods=["POST"])
def skip_round():
    global current_question_number, current_round
    if current_round < 10:
        current_round += 1
        current_question_number = 1
    else:
        return redirect(url_for("home"))
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

@app.route("/bulk_import", methods=["POST"])
def bulk_import():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    file = request.files.get("file")
    if not file:
        flash("No file selected.", "error")
        return redirect(url_for("admin"))

    try:
        stream = TextIOWrapper(file.stream, encoding="utf-8")
        reader = csv.DictReader(stream)

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        count = 0
        for row in reader:
            text = row["challenge_text"].strip()
            intensity = int(row["intensity"])
            orientation = row["orientation"].strip()
            pairing = row["pairing"].strip()

            if text:
                c.execute("INSERT INTO challenges (challenge_text, intensity, orientation, pairing) VALUES (?, ?, ?, ?)",
                          (text, intensity, orientation, pairing))
                count += 1

        conn.commit()
        conn.close()

        flash(f"Successfully imported {count} challenges.", "success")
    except Exception as e:
        flash(f"Import failed: {str(e)}", "error")

    return redirect(url_for("admin"))


@app.route("/update-challenge/<int:id>", methods=["POST"])
def update_challenge(id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    challenge_text = request.form.get("challenge_text")
    intensity = request.form.get("intensity")
    orientation = request.form.get("orientation")
    pairing = request.form.get("pairing")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        UPDATE challenges
        SET challenge_text = ?, intensity = ?, orientation = ?, pairing = ?
        WHERE id = ?
    """, (challenge_text, intensity, orientation, pairing, id))
    conn.commit()
    conn.close()
    flash("Challenge updated successfully.", "success")
    return redirect(url_for("admin"))

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
