# loupdorServ

## Etapes mises en place

1. Créer le serveur écoute TCP (with .... socket.server) : pour que les joueurs envoient des actions
2. Créer la classe Handler qui sera appelé à chaque connexion client.
3. Dans la classe Handler, accepter deux actions:
   a) inscription du joueur à une partie
   b) déplacment d'un jouer avec son identifiant
4. Qq soit l'action, écrire dans un fichier au format JSON l'action souhaitée avec les paramètres: dossier request/id.json (un par joueur)

Exemples de format JSON:

a) Inscription
(requete envoyée par le client)
{
"pseudo": "player_1"
"role": "wolf"
}

(réponse à renvoyer au client)
{
"status": "OK/KO",
"identifiant": "player_1"
"environment": [
["","","#"]
["","X","#"]
["O","W","#"]
]
}

b) Deplacement

(requête à envoyer)
{
"pseudo": "player_1",
"move": [x,y] ou x et y sont 0 1 ou -1
}

5. Consulter le dossier response et attendre que le fichier <id>.json existe

6. Lire le fichier,

7. supprimer le fichier

8. renvoyer la réponse au format json
