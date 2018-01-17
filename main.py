from game_manager import GameManager
from gui import Gui
from communication_protocol import SocketCommunicatorHandler
from communicator import Communicator
from game import Game

SERVER = "server"
CLIENT = "client"


def main():
    roll = SERVER
    ip = "0.0.0.0"
    port = 8000
    gui = Gui()
    communicator = Communicator(root=gui._parent, port=port)
    communicator.connect()
    # communicator

    communication_handler = SocketCommunicatorHandler(communicator)
    game_manager = GameManager(gui, communication_handler, Game(), player=Game.PLAYER_ONE)

    game_manager.run()

if __name__ == '__main__':
    main()