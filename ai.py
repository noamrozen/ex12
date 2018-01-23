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


# if __name__ == '__main__':
#     ai = MinMaxAi(1)
#     game = Game()
#     board = game.get_board()
#
#     game.make_move(1)
#     game.make_move(1)
#     game.make_move(0)
#     game.make_move(1)
#     game.make_move(0)
#     game.make_move(0)
#     game.make_move(0)
#     game.make_move(0)
#     game.make_move(2)
#     #game.make_move(2)
#     print(board)
#     # pos = ai.get_possible_cells(board)
#     # print(pos)
#     print(ai.blocking_or_winning(board))
#
#
#
