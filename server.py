# loupdorServ

## Etapes mises en place

import json
import socketserver
import os

# 2. Créer la classe Handler qui sera appelé à chaque connexion client.
# la classe doit hériter de socketserver base request handler

class MyTCPHandler (socketserver.BaseRequestHandler):


# 3. Dans la classe Handler, accepter deux actions:




    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("Received from {}:".format(self.client_address[0]))
        print(self.data)
        
        
      # lire le data qu'on convertie en texte pour traduire en json
      
        request_json = json.loads(self.data.decode('UTF-8'))
        print(request_json)
     
      # si move alors on est dans un deplacement sinon on est dans une inscription

        # a) déplacment d'un jouer avec son identifiant
        if 'move' in request_json or 'role' in request_json :
      # 4. Qq soit l'action, écrire dans un fichier au format JSON l'action souhaitée avec les paramètres: dossier request/id.json (un par joueur)

        # demander le déplacement au moteur du jeu
        # créer le fichier <id>.json
           pseudo = request_json['pseudo']
           f = open(f'requests/{pseudo}.json', 'w', encoding="utf-8")
           # écrire le json dans le fichier id
           f.write(json.dumps(request_json))
             # fermer le fichier
           f.close()
          
          # dessous = meme chose que les trois lignes du dessus
          # with open('requests/id.json', 'w') as f:
          #   f.wirte(request_json)
           self.request.sendall(json.dumps({"status":"Requete prise en compte"}).encode('UTF-8'))
           
        # 5. Consulter le dossier response et attendre que le fichier <id>.json existe
        
       
       
        if 'action' in request_json:
          pseudo = request_json['pseudo']
          action = request_json['action']
          if action == 'get_env':
            # 6. Lire le fichier,
            result_env = {}
            with open(f'responses/{pseudo}.json','r') as f:
              result_env = json.load(f)
            # 7. renvoyer la réponse au format json
            self.request.sendall(json.dumps(result_env).encode('UTF-8'))
              
           # 8. supprimer le fichier
            os.remove(f'responses/{pseudo}.json')
          
        # c) si ni l'un ni l'autre
        if 'action' not in request_json or 'role' not in request_json or 'move' not in request_json :
          self.request.sendall(b"Invalid.")
          


# 1. Créer le serveur écoute TCP (with .... socket.server) : pour que les joueurs envoient des actions

if __name__ == "__main__":
    HOST, PORT = "172.25.1.10", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()



