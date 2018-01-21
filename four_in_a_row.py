import sys
HUMAN = "human"
AI = "ai"
NO_IP_INPUT_SIZE = 3
AI_RECURSION_DEPTH = 2
ERROR_ARGUMENTS = "arguments program Illegal"
MAX_PORT = 65535

from ai import MinMaxAi
from gui import Gui
from game import Game
from communicator import Communicator
from communication_protocol import SocketCommunicatorHandler
from game_manager import GameManager

def main(args):
    ip = None
    if len(args) == NO_IP_INPUT_SIZE:
        script, is_human, port = args
    elif len(args) == NO_IP_INPUT_SIZE + 1:
        script, is_human, port, ip = args
    else:
        raise ValueError(ERROR_ARGUMENTS)
    if port > MAX_PORT:
        raise ValueError(ERROR_ARGUMENTS)
    if ip is None:
        color = Gui.PLAYER_ONE_COLOR
        player = Game.PLAYER_ONE
    else:
        color = Gui.PLAYER_TWO_COLOR
        player = Game.PLAYER_TWO
    gui = Gui(Game.ROWS_NUM, Game.COLUMN_NUM, color)
    communicator = Communicator(root=gui._parent, ip=ip, port=port)
    communicator.connect()
    communication_handler = SocketCommunicatorHandler(communicator)
    if is_human == AI:
        ai = MinMaxAi(player, AI_RECURSION_DEPTH)
    elif is_human == HUMAN:
        ai = None
    else:
        raise ValueError(ERROR_ARGUMENTS)
    game_manager = GameManager(gui, communication_handler, Game(),
                               player, ai)
    game_manager.run()


if __name__ == '__main__':
    args = sys.argv
    main(args)