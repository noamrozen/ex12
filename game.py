import random
import numpy as np


class Game(object):
    ##############################
    #       Game configuration   #
    ##############################
    ROWS_NUM = 6
    COLUMN_NUM = 7
    SEQ_FOR_WIN = 4

    ###############################
    #       Data Representation   #
    ###############################
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = -1
    ############################
    #       Messages           #
    ############################
    ILLEGAL_MOVE = "Illegal move"

    def __init__(self):
        # choosing the first player randomly
        self.__current_player = self.PLAYER_ONE
        # initiating the board with "-1"
        self.__board_mtx = np.full((self.ROWS_NUM,self.COLUMN_NUM),self.EMPTY)

        self.__win_sequence = []
        self.__moves_stack = []

    def get_winning_sequence(self):
        return self.__win_sequence

    @staticmethod
    def __get_lowest_empty(board_column):
        if board_column[0] != Game.EMPTY:
            # the column is full
            return None
        for index in range(len(board_column)):
            if board_column[index] != Game.EMPTY:
                return index - 1
        return len(board_column)-1

    def make_move(self, column):
        player = self.get_current_player()
        board_mtx = self.get_board()
        board_column = board_mtx[:, column]
        if self.get_winner():
            raise ValueError("the game is over")
            # raise Exception(self.ILLEGAL_MOVE)
        if column < 0 or column > self.COLUMN_NUM:
            raise ValueError("column %s out of range" % column)
            # raise Exception(self.ILLEGAL_MOVE)

        chosen_cell_index = self.__get_lowest_empty(board_column)
        if chosen_cell_index is None:
            raise ValueError("column is full!")
            # raise Exception(self.ILLEGAL_MOVE)

        self.__board_mtx[chosen_cell_index, column] = player
        if player == self.PLAYER_ONE:
            self.__current_player = self.PLAYER_TWO
        else:
            self.__current_player = self.PLAYER_ONE

        # store moves played at a stack for option of undo
        self.__moves_stack.append((chosen_cell_index, column))

    def unmake_move(self):
        last_move = self.__moves_stack.pop()
        self.__board_mtx[last_move] = self.EMPTY
        self.__switch_players()

    def is_full(self):
        board_bool = (self.__board_mtx != self.EMPTY)
        return board_bool.all()

    def get_player_at(self, row, col):
        return self.get_board()[row,col]

    def get_current_player(self):
        return self.__current_player

    def get_board(self):
        return self.__board_mtx

    def get_winner(self):
        board_mtx = self.get_board()
        winner_row = self._search_row(board_mtx)
        if winner_row is not None:
            return winner_row
        winner_col = self._search_col(board_mtx)
        if winner_col is not None:
            return winner_col
        winner_diag = self._search_diagonal(board_mtx)
        if winner_diag is not None:
            return winner_diag
        flipped_board = np.fliplr(board_mtx)
        winner_rev_diag = self._search_reversed_diagonal(flipped_board)
        if winner_rev_diag is not None:
            return winner_rev_diag
        # check if the board is full
        board_bool = (board_mtx != self.EMPTY)
        if board_bool.all():
            return self.DRAW
        return None

    def _search_row(self, board_mtx):
        for row in board_mtx:
            winner, index_list = self._search_winner(row)
            if winner is not None:
                self.__win_sequence = [(row, i) for i in index_list]
                return winner

    def _search_col(self, board_mtx):
        for column in board_mtx.T:
            winner, index_list = self._search_winner(column)
            if winner is not None:
                self.__win_sequence = [(i, column) for i in index_list]
                return winner

    def _search_diagonal(self, board_mtx):
        for diagonal_index in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            current_diagonal = np.diag(board_mtx, diagonal_index)
            if diagonal_index < 0:
                first_coord = (-1 * diagonal_index, 0)
            elif diagonal_index > 0:
                first_coord = (0, diagonal_index)
            else:
                first_coord = (0, 0)
            winner, index_list = self._search_winner(current_diagonal)
            if winner is not None:
                self.__win_sequence = [(first_coord[0] + 1 * i, first_coord[1] + 1 * i) for i in index_list]
                return winner

    def _search_reversed_diagonal(self, flipped_board):
        for diagonal_index in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            diagonal = np.diag(flipped_board, diagonal_index)
            current_diagonal = list(reversed(diagonal))
            if diagonal_index < 0:
                first_coord = (-1 * diagonal_index, 0)
            elif diagonal_index > 0:
                first_coord = (0, diagonal_index)
            else:
                first_coord = (0, 0)
            winner, index_list = self._search_winner(current_diagonal)
            if winner is not None:
                first_i, first_j = first_coord
                self.__win_sequence = [(first_i + i, self.COLUMN_NUM - first_j - i - 1) for i in index_list]
                return winner

    def _search_winner(self, board_line):
        player_one_seq = []
        player_two_seq = []
        for i in range(len(board_line)):
            if board_line[i] == self.PLAYER_ONE:
                player_one_seq.append(i)
                player_two_seq = []
            elif board_line[i] == self.PLAYER_TWO:
                player_two_seq.append(i)
                player_one_seq = []
            else:
                player_one_seq = []
                player_two_seq = []
            if len(player_one_seq) == self.SEQ_FOR_WIN:
                return self.PLAYER_ONE, player_one_seq
            if len(player_two_seq) == self.SEQ_FOR_WIN:
                return self.PLAYER_TWO, player_two_seq
        return None, None

    def __switch_players(self):
        if self.__current_player == self.PLAYER_ONE:
            self.__current_player = self.PLAYER_TWO
        else:
            self.__current_player = self.PLAYER_ONE








# # # test for exception when there is a winner
# game = Game()
# # # print(game.get_board())
#
# game.make_move(1)
# game.make_move(1)
# game.make_move(1)
# game.make_move(2)
# game.make_move(0)
# game.make_move(0)
# game.make_move(0)
# game.make_move(2)
# game.make_move(2)
# game.make_move(2)

# print(game.get_board())


# # test for exception when there is a winner by diagonal
# game = Game()
# print(game.get_board())
# # game.make_move(1)

# game.make_move(1)
# game.make_move(1)
# game.make_move(2)
# game.make_move(0)
# game.make_move(0)
# game.make_move(2)
# game.make_move(0)
# game.make_move(2)
# game.make_move(2)
# print(game.get_board())

# # tester for exception when game over
# game = Game()
# game.make_move(1)
# game.make_move(1)
# game.make_move(0)
# game.make_move(1)
# game.make_move(0)
# game.make_move(0)
# game.make_move(0)
# game.make_move(2)
# #game.make_move(2)
# # game.make_move(2)
# # game.make_move(3)
# # game.make_move(3)
# # game.make_move(3)
# #game.make_move(1)
# print(game.get_board())


# tester for exception when column full
# game = Game()
# print(game.get_board())
# game.make_move(1)
# game.make_move(1)
# game.make_move(1)
## game.make_move(1)
# print(game.get_board())
#
# arr = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
# print(arr)
# print()
# print(np.fliplr(arr))