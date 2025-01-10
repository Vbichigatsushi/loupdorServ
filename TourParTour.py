from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, LoggingEventHandler,FileSystemEventHandler
import json
import protos.interface_pb2_grpc as interface2
import protos.interface_pb2 as interface
import concurrent.futures as futures
import grpc
from sqlalchemy import text,create_engine,select,insert,update
from sqlalchemy.orm import Session
import random
from ORM import Player,Game

#region variable globale
gridWidth=20
gridHeight=20
timeForRound=int
maxPlayer=int
game=False
players={}
game_id=2
engine = create_engine("sqlite:///test.db", echo=True)
alive=True
session = Session(engine)
round_en_cours = 0
timer = 0
#endregion

#region récupération data pour tcp
class truc(FileSystemEventHandler):
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:

        with open('truc.json','r') as fichier:
                data = json.load(fichier)

        return super().on_created(event)


def machin():
    path = "./player_actions"
    event_handler = truc()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
#endregion

#region récupération data pour http
class LoupdorService(interface2.LoupdorServiceServicer):
    def CreateMap(self, request, context):
        gridWidth=request.width
        gridHeight=request.height
        return interface.MapSizeReply(message=f"Carte de taille {request.width},{request.height} créé !")
    
    def TimerForTour(self, request, context):
        timeForRound=request.timeSecond
        return interface.SecondForTimerReply(message=f"Timer défini à {request.timeSecond}s.")
    
    def NbMaxPlayer(self, request, context):
        maxPlayer=request.nbPlayers
        return interface.NbplayerReply(message=f"Nombre de joueur maximum défini à {request.nbPlayers}.")
    
    def StartGame(self, request, context):
        game = True if request.isStarting else False
        print(request.isStarting,game)
        return interface.StartGameReply(message=f"Partie démarrée.")
    
    def Inscrption(self, request, context):
        if request.ip not in players :
            hauteur=random.randint(0,gridHeight)
            largeur=random.randint(0,gridWidth)
            set_player(str(request.name),str(request.role),str(request.ip),int(hauteur),int(largeur),game_id)
        else :
            update_player(str(request.name),str(request.role),str(request.ip),game_id,players[request.ip][2])
        players[request.ip]=[request.role,request.name,alive]
        print(players)
        return interface.InscriptionReply(message=request.role)
    
    def Move(self, request, context):
        return interface.MoveReply(message=deplacement(request.direction,request.ip,game_id))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    interface2.add_LoupdorServiceServicer_to_server(LoupdorService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()
#endregion

#region communication ORM BDD
#use session (session.execute(select(colonne)))
def set_player(paName,paRole,paIp,paHauteur,paLargeur,paGame_id,paAlive=True):
    stmt = (
        insert(Player)
        .values(
            name = paName,
            role = paRole,
            alive = paAlive,
            ip = paIp,
            hauteur = paHauteur,
            largeur = paLargeur,
            game_id = paGame_id
        )
    )
    session.execute(stmt)
    session.commit()
    
def update_player(paName,paRole,paIp,paGame_id,paAlive=True):
    update_stmt = (
        update(Player)
        .where(Player.ip == paIp)
        .where(Player.game_id == paGame_id)
        .values(
            name = paName,
            role = paRole,
            alive=paAlive
        )
    )
    session.execute(update_stmt)
    session.commit()

def update_player_place(paHauteur,paLargeur,paIp,paGame_id,paAlive=True):
    update_stmt = (
        update(Player)
        .where(Player.ip == paIp)
        .where(Player.game_id == paGame_id)
        .values(
            hauteur=paHauteur,
            largeur=paLargeur,
            alive=paAlive
        )
    )
    session.execute(update_stmt)
    session.commit()

def get_player_place(paIp,paIdgame):
    stmt = (select(
                Player.role,
                Player.alive,
                Player.hauteur,
                Player.largeur,
                Player.game_id)
            .where(Player.ip == paIp)
            .where(Player.game_id == paIdgame)
            .order_by(Player.game_id.desc())
            .limit(1))
    result = session.execute(stmt).first()
    return result

def get_game_state(paIdgame):
    stmt = (select(Game.statut)
            .where(Game.id == paIdgame))
    return session.execute(stmt)

def set_game(paMaxPlayer,paNbTour,paHauteur,paLargeur,paTimerTour,paStatut):
    stmt = (
        insert(Game)
        .values(
            max_player = paMaxPlayer,
            nb_tours = paNbTour,
            hauteur = paHauteur,
            largeur = paLargeur,
            temps_par_tour = paTimerTour,
            statut = paStatut,
        )
    )
    session.execute(stmt)
    print(session.commit())  

def get_somethings_here(paX: int, paY: int, paIdgame: int) -> bool:
    stmt = (
        select(Player.role)
        .where(Player.game_id == paIdgame)
        .where(Player.largeur == paX)
        .where(Player.hauteur == paY)
        .where(Player.alive == True)
    )
    result = session.execute(stmt).fetchall()
    if len(result) >= 1 :
        return True
    return False

#endregion
#region moteur
def deplacement(paDirection,paIp,paIdgame):
    # round_en_cours+=1
    # wait_player()
    infos = get_player_place(paIp,paIdgame)
    x=infos.largeur
    y=infos.hauteur
    role=infos.role
    if role=="vif or":
        match paDirection:
            case "N":
                move=[x+0,y+2]
                pass
            case "S":
                move=[x+0,y-2]
                pass
            case "E":
                move=[x+2,y+0]
                pass
            case "W":
                move=[x-2,y+0]
                pass
            case _:
                pass
    else :
        match paDirection:
            case "N":
                move=[x+0,y+1]
                pass
            case "S":
                move=[x+0,y-1]
                pass
            case "E":
                move=[x+1,y+0]
                pass
            case "W":
                move=[x-1,y+0]
                pass
            case _:
                pass
    if move_possible(move[0],move[1]):
        update_player_place(move[1],move[0],paIp,paIdgame)
    show_grid(move[0],move[1],role)
    return str(move)

def move_possible(paX, paY):
    if 0 < paX < gridWidth and 0 < paY < gridHeight:
        return True
    return False


def wait_player():
    while round_en_cours < len(players) or timer < timeForRound:
        break

def show_grid(paX,paY,paRole):
    vision = []
    compteur1=0
    compteur2=0
    if paRole == "vif or":
        startx = paX-2
        endx = paX+2
        starty = paY-2
        endy = paY+2
    else :
        startx = paX-1
        endx = paX+1
        starty = paY-1
        endy = paY+1

    for i in range(startx,endx+1):
        vision.append([])
        for y in range(starty,endy+1):
            if 0 <= i > gridWidth or 0 <= y > gridHeight :
                vision[compteur1].append(["#"])
            elif i == paX and y ==paY:
                vision[compteur1].append(["S"])
            elif get_somethings_here(i,y,game_id):
                vision[compteur1].append(["E"])
            else :
                vision[compteur1].append([" "])
            compteur2+=1
        compteur1+=1
    print(vision)
#endregion


if __name__=="__main__":
    deplacement("E","172.17.0.2","2")
    # get_somethings_here(5,18,2)
    # serve()