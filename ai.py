import numpy as np


class AI(object):
    def find_legal_move(self, game, func, timeout=None):
        if game.is_full():
            raise ValueError("No possible AI moves")
        column = self.choose_column(game)
        func(column)

    def choose_column(self, game):
        raise NotImplementedError


class RandomAI(AI):
    def choose_column(self, game):
        possible_columns = np.nonzero(game.get_board()[0] == game.EMPTY)[0]
        return np.random.choice(possible_columns, 1)[0]

