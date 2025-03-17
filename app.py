from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Store player names
players = []

@app.route("/", methods=["GET", "POST"])
def index():
    global players
    if request.method == "POST":
        name = request.form.get("name").strip()
        if name and name not in players:
            players.append(name)  # Add player to list
    return render_template("index.html", players=players)

@app.route("/randomize")
def randomize():
    global players
    if players:
        shuffled_players = players[:]  # Copy the list
        random.shuffle(shuffled_players)
        return render_template("result.html", players=shuffled_players)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global players
    players = []  # Reset player list
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
