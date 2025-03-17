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
        if name and name not in players:
            players.append(name)
    return render_template("index.html", players=players)

@app.route("/randomize")
def randomize():
    global players
    if players:
        shuffled_players = players[:]
        random.shuffle(shuffled_players)
        return render_template("result.html", players=shuffled_players)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global players
    players = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
