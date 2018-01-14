from communication_protocol import ErrorMessage, UpdateMessage, WinnerMessage

BLOCKED_CELL_ERROR_MSG = "Cell is blocked!"
NOT_YOUR_TURN_ERROR_MSG = "It is not your turn!"


class GameManager(object):
    def __init__(self, gui, communication_manager, game):
        self.gui = gui
        self.communication_manager = communication_manager
        self.game = game

    def run(self):
        self.gui.set_collumn_choice_handler(self.handle_choice)

    def end_game(self, winner):
        self.gui.output_winner(winner)
        # self.communication_manager.send_winner(winner)
        self.gui.shutdown()

    def handle_choice(self, column):
        raise NotImplementedError


class GameServer(GameManager):
    def __init__(self, gui, communication_manager, game):
        super(GameServer, self).__init__(gui, communication_manager, game)
        # we might want a Player object, containing name, ip and other details about the player
        self.player = self.game.PLAYER_ONE

        # self.communication_manager.set_client_choice_handler(self.handle_client_choice)

    def __handle_choice_wrapper(self, column, player):
        if not self.game.get_current_player() == player:
            raise errors.NotYourTurn()

        cell_i, cell_j = self.game.get_column_cell(column)
        if self.game.get_player_at(cell_i, cell_j) is None:
            self.game.make_move(column)
            if self.game.get_winner == self.player:
                self.end_game(winner=self.player)
        else:
            raise errors.BlockedCell()

        self.gui.output_board(self.game.board)
        # self.communication_manager.send_board_state(game)

    def handle_choice(self, column):
        try:
            self.__handle_choice_wrapper(column, self.player)
        except Exception as e:
            self.gui.output_error(str(e))

    def handle_client_choice(self, column):
        try:
            self.__handle_choice_wrapper(column, self.game.PLAYER_TWO)
        except Exception as e:
            self.communication_manager.send_error(str(e))


class GameClient(GameManager):
    def __init__(self, gui, communicator, game):
        super(GameClient, self).__init__(gui=gui, communication_manager=communicator, game=game)
        self.communication_manager.set_server_answer_handler(self.handle_server_response)

    def handle_choice(self, column):
        self.communication_manager.send_choice(column)

    def handle_server_response(self, message):
        if isinstance(message, ErrorMessage):
            self.gui.output_error(message.content)
        if isinstance(message, UpdateMessage):
            self.game.make_move(message.coordinates)
            self.gui.output_board(self.game)
        if isinstance(message, WinnerMessage):
            self.end_game(message.content)
