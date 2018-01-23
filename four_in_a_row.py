import sys
HUMAN = "human"
AI = "ai"
NO_IP_INPUT_SIZE = 3
AI_RECURSION_DEPTH = 2
ERROR_ARGUMENTS = "arguments program Illegal"
PORT_NOT_NUM_ERR = "received port is not a number"
MAX_PORT = 65535

from block_win_ai import BlockWinAI
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
    try:
        port = int(port)
    except TypeError:
        raise ValueError(PORT_NOT_NUM_ERR)
    if port > MAX_PORT:
        raise ValueError(ERROR_ARGUMENTS)
    if ip is None:
        color = Gui.PLAYER_ONE_COLOR
        player = Game.PLAYER_ONE
    else:
        color = Gui.PLAYER_TWO_COLOR
        player = Game.PLAYER_TWO

    if is_human == AI:
        ai = BlockWinAI(player)
        is_ai = True
    elif is_human == HUMAN:
        ai = None
        is_ai = False
    else:
        raise ValueError(ERROR_ARGUMENTS)

    gui = Gui(Game.ROWS_NUM, Game.COLUMN_NUM, color, is_ai)
    communicator = Communicator(root=gui._parent, ip=ip, port=port)
    communicator.connect()
    communication_handler = SocketCommunicatorHandler(communicator)

    game_manager = GameManager(gui, communication_handler, Game(),
                               player, ai)
    game_manager.run()


if __name__ == '__main__':
    args = sys.argv
    main(args)