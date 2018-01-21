# from communication_protocol import ErrorMessage, UpdateMessage, WinnerMessage

BLOCKED_CELL_ERROR_MSG = "Cell is blocked!"
NOT_YOUR_TURN_ERROR_MSG = "It is not your turn!"


class GameManager(object):
    def __init__(self, gui, communication_manager, game, player, ai=None):
        self.gui = gui
        self.communication_manager = communication_manager
        self.game = game

        # we might want a Player object, containing name, ip and other details about the player
        self.player = player
        self.opponent = self.__get_opponent(player)
        self.communication_manager.set_client_choice_handler(self.handle_opponent_choice)
        self.ai = ai

    def __get_opponent(self, player):
        return ({self.game.PLAYER_ONE, self.game.PLAYER_TWO} - {player}).pop()

    def run(self):
        self.gui.set_collumn_choice_handler(self.handle_choice)
        self.gui.run()

    def end_game(self, winner):
        winner_color_mapping = {
            self.game.PLAYER_ONE: self.gui.PLAYER_ONE_COLOR,
            self.game.PLAYER_TWO: self.gui.PLAYER_TWO_COLOR,
        }
        winner_color = winner_color_mapping.get(winner)
        self.gui.show_winning(self.game.get_board(), self.game.get_winning_sequence(), winner_color)
        # self.communication_manager.send_winner(winner)
        self.gui.shutdown()



    def handle_choice(self, column):
        if not self.game.get_current_player() == self.player:
            self.gui.output_error(NOT_YOUR_TURN_ERROR_MSG)
            return

        try:
            self.game.make_move(column)
            self.communication_manager.send_choice(column)
            self.gui.output_board(self.game.get_board())
            winner = self.game.get_winner()
            # self.__switch_players()
            if winner is not None:
                self.end_game(winner)

        except ValueError as e:
            self.gui.output_error(str(e))

        # self.communication_manager.send_board_state(game)

    def handle_opponent_choice(self, column):
        self.game.make_move(column)
        self.gui.output_board(self.game.get_board())
        winner = self.game.get_winner()
        if winner is not None:
            self.end_game(winner)

        if self.ai is not None:
            self.ai.find_legal_move(self.game, self.gui.press_column)


