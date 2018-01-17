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
    gui = Gui(Game.ROWS_NUM, Game.COLUMN_NUM)
    communicator = Communicator(root=gui._parent, port=port)
    communicator.connect()
    # communicator

    communication_handler = SocketCommunicatorHandler(communicator)
    game_manager = GameManager(gui, communication_handler, Game(), player=Game.PLAYER_ONE)

    while not communicator.is_connected():
        pass
        # message box saying "waiting for connection..."
    # shutdown message box
    game_manager.run()


if __name__ == '__main__':
    main()