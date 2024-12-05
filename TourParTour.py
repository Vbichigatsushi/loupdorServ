from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, LoggingEventHandler,FileSystemEventHandler
import json
import protos.interface_pb2_grpc as interface2
import protos.interface_pb2 as interface
import concurrent.futures as futures
import grpc

#region variable globale
player=dict
grille=[]
timertour=int
start=False
nbtour=int
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
        return interface.MapSizeReply(message=f"Carte de taille {request.width},{request.height} créé !")
    def TimerForTour(self, request, context):
        return interface.SecondForTimerReply(message=f"Timer défini à {request.timeSecond}s.")
    def NbMaxPlayer(self, request, context):
        return interface.NbplayerReply(message=f"Nombre de joueur maximum défini à {request.nbPlayers}.")
    def StartGame(self, request, context):
        return interface.StartGameReply(message=f"Partie démarée.")
    def Inscrption(self, request, context):
        return interface.InscriptionReply(message=f"Joueur inscrit au role de {request.role}")
    def Move(self, request, context):
        return interface.MoveReply(message=f"Mouvement au {request.direction} pris en compte")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    interface2.add_LoupdorServiceServicer_to_server(LoupdorService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()
#endregion


if __name__=="__main__":
    # machin()
    serve()