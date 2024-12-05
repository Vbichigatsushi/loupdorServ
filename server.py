from flask import Flask, request, jsonify

app = Flask(__name__)

# État global de la partie
game_state = {
    "game_started": False,
    "players": {},  # Stocke les joueurs avec leurs rôles et positions
    "grid": None,  # Grille NxM
    "turn": 0,  # Compteur de tours
    "max_turns": 10  # Nombre maximum de tours
}

# Routes de gestion de la partie
@app.route('/set_role', methods=['POST'])
def set_role():
    if game_state["game_started"]:
        return jsonify({"error": "La partie a déjà commencé, impossible d'ajouter ou modifier les rôles."}), 400

    data = request.json
    player_id = data.get("player_id")
    role = data.get("role")

    if not player_id or not role:
        return jsonify({"error": "Les champs 'player_id' et 'role' sont requis."}), 400

    if player_id in game_state["players"]:
        return jsonify({"error": f"Le joueur {player_id} existe déjà."}), 400

    # Ajouter le joueur
    game_state["players"][player_id] = {
        "role": role,
        "position": [0, 0]  # Position initiale par défaut
    }

    return jsonify({"message": f"Joueur {player_id} ajouté avec le rôle {role}."}), 200

@app.route('/start_game', methods=['POST'])
def start_game():
    if game_state["game_started"]:
        return jsonify({"error": "La partie est déjà en cours."}), 400

    # Initialiser la grille NxM
    data = request.json
    n = data.get("n", 10)  # Taille par défaut 10x10
    m = data.get("m", 10)

    game_state["grid"] = [[None for _ in range(m)] for _ in range(n)]
    game_state["game_started"] = True

    return jsonify({"message": "La partie a commencé !", "grid_size": (n, m)}), 200

@app.route('/move', methods=['POST'])
def move():
    if not game_state["game_started"]:
        return jsonify({"error": "La partie n'a pas encore commencé."}), 400

    data = request.json
    player_id = data.get("player_id")
    direction = data.get("direction")

    if player_id not in game_state["players"]:
        return jsonify({"error": f"Joueur {player_id} inconnu."}), 400

    if direction not in ["north", "south", "east", "west"]:
        return jsonify({"error": "Direction invalide. Choisissez parmi 'north', 'south', 'east', 'west'."}), 400

    # Récupérer la position actuelle du joueur
    current_position = game_state["players"][player_id]["position"]
    x, y = current_position

    # Mettre à jour la position selon la direction
    if direction == "north":
        x -= 1
    elif direction == "south":
        x += 1
    elif direction == "east":
        y += 1
    elif direction == "west":
        y -= 1

    # Vérifier les limites de la grille
    if 0 <= x < len(game_state["grid"]) and 0 <= y < len(game_state["grid"][0]):
        game_state["players"][player_id]["position"] = [x, y]
        return jsonify({"message": f"Joueur {player_id} déplacé vers {direction}.", "new_position": [x, y]}), 200
    else:
        return jsonify({"error": "Déplacement hors de la grille."}), 400

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({
        "game_started": game_state["game_started"],
        "players": game_state["players"],
        "turn": game_state["turn"],
        "max_turns": game_state["max_turns"]
    }), 200

@app.route('/next_turn', methods=['POST'])
def next_turn():
    if not game_state["game_started"]:
        return jsonify({"error": "La partie n'a pas encore commencé."}), 400

    game_state["turn"] += 1

    if game_state["turn"] >= game_state["max_turns"]:
        game_state["game_started"] = False
        return jsonify({"message": "La partie est terminée !"}), 200

    return jsonify({"message": f"Tour {game_state['turn']} terminé.", "next_turn": game_state["turn"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
