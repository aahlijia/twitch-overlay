import json
import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SETLIST_PATH = os.path.join(os.path.dirname(__file__), "setlist.json")
RECENTS_PATH = os.path.join(os.path.dirname(__file__), "recents.json")
RECENTS_MAX = 4

# In-memory state — resets when the server restarts
state = {"game": "", "song": "", "visible": False}


def load_setlist():
    with open(SETLIST_PATH, "r") as f:
        return json.load(f)


def save_setlist(data):
    with open(SETLIST_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_recents():
    if not os.path.exists(RECENTS_PATH):
        return []

    with open(RECENTS_PATH, "r") as f:
        return json.load(f)


def save_recents(data):
    with open(RECENTS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def add_recent(game, song):
    """Upsert (game, song) into recents, move-to-front, capped at 4."""
    recents = load_recents()

    recents = [
        entry
        for entry in recents
        if not (
            entry["game"].lower() == game.lower()
            and entry["song"].lower() == song.lower()
        )
    ]

    recents.insert(0, {"game": game, "song": song})
    recents = recents[:RECENTS_MAX]

    save_recents(recents)
    return recents


@app.route("/overlay")
def overlay():
    return send_file("overlay.html")


@app.route("/control")
def control():
    return send_file("control.html")


@app.route("/state")
def get_state():
    return jsonify(state)


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()

    if "game" in data:
        state["game"] = data["game"]

    if "song" in data:
        state["song"] = data["song"]

    if "visible" in data:
        state["visible"] = data["visible"]

    recents = load_recents()
    if state["visible"] and state["game"]:
        recents = add_recent(state["game"], state["song"])

    return jsonify({"ok": True, "state": state, "recents": recents})


@app.route("/setlist")
def get_setlist():
    return jsonify(load_setlist())


@app.route("/recents")
def get_recents():
    return jsonify(load_recents())


@app.route("/setlist/add-song", methods=["POST"])
def add_song():
    """Add a song to an existing game entry, or create a new game entry."""
    data = request.get_json()
    game = data.get("game", "").strip()
    song = data.get("song", "").strip()

    if not game or not song:
        return jsonify(
            {"ok": False, "error": "game and song are required"}
        ), 400

    setlist = load_setlist()

    for entry in setlist:
        if entry["game"].lower() == game.lower():
            if song not in entry["songs"]:
                entry["songs"].append(song)

            save_setlist(setlist)

            return jsonify({"ok": True, "setlist": setlist})

    # Game not found — create a new entry
    setlist.append({"game": game, "songs": [song]})
    save_setlist(setlist)

    return jsonify({"ok": True, "setlist": setlist})


if __name__ == "__main__":
    print("Now Playing server running.")
    print("  OBS browser source → http://localhost:5000/overlay")
    print("  Control panel      → http://localhost:5000/control")
    print("  (or use your local IP for phone access)")
    app.run(host="0.0.0.0", port=5000, debug=False)
