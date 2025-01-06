import requests

class GameClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.role = None
        self.name = None 
        self.game_started = False 

    def set_name(self, name):
        self.name = name

    def set_role(self):
        if self.game_started:
            print("Erreur : Vous ne pouvez plus changer de rôle après le début de la partie.")
            return
        role = input("Veuillez en choisir un : ").strip()
        roles = ["villageois", "vif or", "loup garou"]
        role = role.strip()
        if role not in roles:
            print("Erreur : Rôle invalide. Choisissez parmi :", roles)
            return

        response = requests.post(f"{self.server_url}/set_role", json={"role": role, "name": self.name,"order":"inscription"})
        if response.status_code == 200:
            self.role = role
            print(response.text)
        else:
            print("Erreur lors de la définition du rôle :", response.text)

    def move(self, direction):
         if not self.game_started:
               print("Erreur : Vous ne pouvez pas vous déplacer avant que la partie commence.")
               return

         valid_directions = {
               'NORTH': 'N', 'NORD': 'N', 'N': 'N',
               'SOUTH': 'S', 'SUD': 'S', 'S': 'S',
               'EAST': 'E', 'EST': 'E', 'E': 'E',
               'WEST': 'W', 'OUEST': 'W', 'O': 'W', 'W': 'W'
         }

         direction_upper = direction.upper()
         normalized_direction = valid_directions.get(direction_upper)
         if not normalized_direction:
               print("Erreur : Direction invalide. Choisissez parmi :", list(valid_directions.keys()))
               return

         response = requests.post(f"{self.server_url}/move", json={"direction": normalized_direction,"order":"move"})
         if response.status_code == 200:
            data = response.json()
            print("Déplacement effectué :", response.text)
         else:
            print("Erreur lors du déplacement :", response.text)
    def interact(self, object_name):
        if not self.game_started:
            print("Erreur : Vous ne pouvez pas interagir avant que la partie commence.")
            return

        response = requests.post(f"{self.server_url}/interact", json={"object_name": object_name, "name": self.name})
        if response.status_code == 200:
            data = response.json()
            print("Résultat de l'interaction :", data.get("result"))
        else:
            print("Erreur lors de l'interaction :", response.text)

    def get_game_state(self):
        response = requests.get(f"{self.server_url}/state", params={"name": self.name})
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
            "set_role": lambda: self.set_role(),
            "move": lambda: self.move(*args) if args else print("Erreur : Veuillez préciser une direction (nord, sud, est, ouest)."),
            "interact": lambda: self.interact(*args),
            "get_game_state": lambda: self.get_game_state(),
        }

        if command in commands:
            commands[command]()
        else:
            print(f"Erreur : Commande '{command}' non reconnue.")


if __name__ == "__main__":
    server_url = "http://172.25.1.11:9999/"  # Adresse du serveur
    client = GameClient(server_url)

    print("Bienvenue dans le jeu !")
    while not client.name:
        name = input("Entrez votre nom : ").strip()
        if name:
            client.set_name(name)
        else:
            print("Erreur : Le nom ne peut pas être vide. Veuillez réessayer.")
    while client.role == None:
      print("voici les roles presents : villageois, vif or, loup garou")
      client.set_role()

    print(f"Bienvenue {client.name} !")
    print("Commandes disponibles : set_role, move, interact, get_game_state, start_game, quit")

    while True:
      if client.role == None :
         user_input = input(" : ").strip().split()
         command = user_input[0]
         args = user_input[1:]
      else :
         user_input = input("Entrez une commande : ").strip().split()
         command = user_input[0]
         args = user_input[1:] 
         if command == "quit":
            print("Fin du jeu.")
            break
         elif command == "start_game":
            client.game_started = True 
            print("La partie commence !")
         elif command == "help":
            print("Commandes disponibles : set_role, move, interact, get_game_state, start_game, quit")
         else:
            client.execute_command(command, *args)
       
         
