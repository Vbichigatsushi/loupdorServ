import requests

class GameClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.role = None
        self.player_name = None 
        self.game_started = False 

    def set_name(self, name):
        """Définit le nom du joueur."""
        self.player_name = name

    def set_role(self, role):
        if self.game_started:
            print("Erreur : Vous ne pouvez pas changer de rôle après le début de la partie.")
            return

        roles = ['villageois', 'vif d\'or', 'loup garou']
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return

        response = requests.post(f"{self.server_url}/set_role", json={"role": role, "player_name": self.player_name})
        if response.status_code == 200:
            self.role = role
            print(f"Rôle attribué : {role}")
        else:
            print("Erreur lors de la définition du rôle :", response.text)

    def move(self, direction):
         if not self.game_started:
               print("Erreur : Vous ne pouvez pas vous déplacer avant que la partie commence.")
               return

         valid_directions = {
               'NORTH': 'NORTH', 'NORD': 'NORTH', 'N': 'NORTH',
               'SOUTH': 'SOUTH', 'SUD': 'SOUTH', 'S': 'SOUTH',
               'EAST': 'EAST', 'EST': 'EAST', 'E': 'EAST',
               'WEST': 'WEST', 'OUEST': 'WEST', 'O': 'WEST', 'W': 'WEST'
         }

         direction_upper = direction.upper()
         normalized_direction = valid_directions.get(direction_upper)
         if not normalized_direction:
               print("Erreur : Direction invalide. Choisissez parmi :", list(valid_directions.keys()))
               return

         response = requests.post(f"{self.server_url}/move", json={"direction": normalized_direction, "player_name": self.player_name})
         if response.status_code == 200:
            data = response.json()
            print("Déplacement effectué :", data.get("new_position"))
         else:
            print("Erreur lors du déplacement :", response.text)
    def interact(self, object_name):
        if not self.game_started:
            print("Erreur : Vous ne pouvez pas interagir avant que la partie commence.")
            return

        response = requests.post(f"{self.server_url}/interact", json={"object_name": object_name, "player_name": self.player_name})
        if response.status_code == 200:
            data = response.json()
            print("Résultat de l'interaction :", data.get("result"))
        else:
            print("Erreur lors de l'interaction :", response.text)

    def get_game_state(self):
        response = requests.get(f"{self.server_url}/state", params={"player_name": self.player_name})
        if response.status_code == 200:
            data = response.json()
            self.game_started = data.get("game_started", False)
            print("Carte actuelle :", data.get("map"))
            print("Objets autour :", data.get("nearby_objects"))
            print("Temps restant :", data.get("time_remaining"))
            print("Partie commencée :", self.game_started)
        else:
            print("Erreur lors de la récupération de l'état :", response.text)

    def execute_command(self, command, *args):
        commands = {
            "set_role": lambda: self.set_role(*args),
            "move": lambda: self.move(*args) if args else print("Erreur : Veuillez préciser une direction (nord, sud, est, ouest)."),
            "interact": lambda: self.interact(*args),
            "get_game_state": lambda: self.get_game_state(),
        }

        if command in commands:
            commands[command]()
        else:
            print(f"Erreur : Commande '{command}' non reconnue.")


if __name__ == "__main__":
    server_url = "http://localhost:9999/"  # Adresse du serveur
    client = GameClient(server_url)

    print("Bienvenue dans le jeu !")
    while not client.player_name:
        player_name = input("Entrez votre nom : ").strip()
        if player_name:
            client.set_name(player_name)
        else:
            print("Erreur : Le nom ne peut pas être vide. Veuillez réessayer.")

    print(f"Bienvenue {client.player_name} !")
    print("Commandes disponibles : set_role, move, interact, get_game_state, start_game, quit")

    while True:
        user_input = input("Entrez une commande : ").strip().split()
        command = user_input[0]
        args = user_input[1:]  

        if command == "quit":
            print("Fin du jeu.")
            break
        elif command == "start_game":
            client.game_started = True 
            print("La partie commence !")
        else:
            client.execute_command(command, *args)
