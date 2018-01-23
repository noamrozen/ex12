BLOCKED_CELL_ERROR_MSG = "Cell is blocked!"
NOT_YOUR_TURN_ERROR_MSG = "It is not your turn!"


class GameManager(object):
    def __init__(self, gui, communication_manager, game, player, ai=None):
        # game elements handlers
        self.gui = gui
        self.communication_manager = communication_manager
        self.game = game
        self.ai = ai

        # managing attributes
        self.player = player
        self.opponent = self.__get_opponent(player)

    def __get_opponent(self, player):
        return ({self.game.PLAYER_ONE, self.game.PLAYER_TWO} - {player}).pop()

    def run(self):
        self.communication_manager.set_client_choice_handler(self.handle_opponent_choice)
        self.gui.set_column_choice_handler(self.handle_choice)
        if self.ai and self.game.get_current_player() == self.player:
            self.run_ai()
        self.gui.run()

    def end_game(self, winner):
        winner_color_mapping = {
            self.game.PLAYER_ONE: self.gui.PLAYER_ONE_COLOR,
            self.game.PLAYER_TWO: self.gui.PLAYER_TWO_COLOR,
        }
        winner_color = winner_color_mapping.get(winner)
        self.gui.show_winning(self.game.get_board(), self.game.get_winning_sequence(), winner_color)
        for column in range(self.game.COLUMN_NUM):
            self.gui.disable_button(column)

    def handle_choice(self, column):
        if not self.game.get_current_player() == self.player:
            self.gui.output_error(NOT_YOUR_TURN_ERROR_MSG)
            return

        try:
            self.game.make_move(column)
            self.communication_manager.send_choice(column)
            self.gui.output_board(self.game.get_board())
            winner = self.game.get_winner()
            if winner is not None:
                self.end_game(winner)

        except ValueError as e:
            self.gui.output_error(str(e))

    def handle_opponent_choice(self, column):
        self.game.make_move(column)
        self.gui.output_board(self.game.get_board())
        winner = self.game.get_winner()
        if winner is not None:
            self.end_game(winner)
            return

        if self.ai is not None:
            self.run_ai()

    def run_ai(self):
        def ai_press_column(column):
            self.gui.enable_button(column)
            self.gui.press_column(column)
            self.gui.disable_button(column)
        self.ai.find_legal_move(self.game, ai_press_column)




