from game_manager import  GameServer
from gui import Gui
from communication_protocol import ClientCommunicationHandler, ServerCommunicationHandler
from communicator import Communicator
from game import Game

SERVER = "server"
CLIENT = "client"


def main():
    roll = SERVER
    ip = "127.0.0.1"
    port = 8000
    gui = Gui()
    communicator = Communicator(root=gui._parent, ip=ip, port=port)

    if roll == SERVER:
        communication_handler = ServerCommunicationHandler(communicator)
        game_manager = GameServer(gui, communication_handler, Game())
    else:
        communication_handler = ClientCommunicationHandler(communicator)
        game_manager = GameClient(gui, communication_handler)

    game_manager.run()

if __name__ == '__main__':
    main()