from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
