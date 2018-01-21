import random
import numpy as np


class Game(object):

    ROWS_NUM = 6
    COLUMN_NUM = 7
    SEQ_FOR_WIN = 4
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = -1
    ILLEGAL_MOVE = "Illegal move"

    def __init__(self):
        # choosing the first player randomly
        self.__current_player = self.PLAYER_ONE
        # initiating the board with "-1"
        self.__board_mtx = np.full((self.ROWS_NUM,self.COLUMN_NUM),self.EMPTY)
        self.__win_seq = []
        self.__moves_stack = []

    def get_winning_sequence(self):
        return self.__win_seq

    @staticmethod
    def __get_lowest_empty(board_column):
        if board_column[0] != Game.EMPTY:
            # the column is full
            return False
        for index in range(len(board_column)):
            if board_column[index] != Game.EMPTY:
                return str(index - 1)
        return str(len(board_column)-1)

    def make_move(self, column):
        player = self.get_current_player()
        board_mtx = self.get_board()
        board_column = board_mtx[:, column]
        if self.get_winner():
            raise ValueError("the game is over")
            # raise Exception(self.ILLEGAL_MOVE)
        if not self.__get_lowest_empty(board_column):
            raise ValueError("column is full!")
            # raise Exception(self.ILLEGAL_MOVE)
        if column < 0 or column > self.COLUMN_NUM:
            raise ValueError("column %s out of range" % column)
            # raise Exception(self.ILLEGAL_MOVE)
        else:
            index = int(self.__get_lowest_empty(board_column))
            self.__board_mtx[index, column] = player
            if player == self.PLAYER_ONE:
                self.__current_player = self.PLAYER_TWO
            else:
                self.__current_player = self.PLAYER_ONE

            self.__moves_stack.append((index, column))

    def _search_winner(self, list):
        player_one_seq = []
        player_two_seq = []
        for i in range(len(list)):
            if list[i] == self.PLAYER_ONE:
                player_one_seq.append(i)
                player_two_seq = []
            elif list[i] == self.PLAYER_TWO:
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

    def unmake_move(self):
        last_move = self.__moves_stack.pop()
        self.__board_mtx[last_move] = self.EMPTY
        self.__switch_players()


    def _search_row(self, board_mtx):
        for row in range(self.ROWS_NUM):
            cur_row = board_mtx[row, :]
            winner, index_list = self._search_winner(cur_row)
            if winner is not None:
                coord_list = []
                for i in index_list:
                    coord_list.append((row, i))
                self.__win_seq = coord_list
                return winner

    def _search_col(self, board_mtx):
        for col in range(self.COLUMN_NUM):
            cur_col = board_mtx[:, col]
            winner, index_list = self._search_winner(cur_col)
            if winner is not None:
                coord_list = []
                for i in index_list:
                    coord_list.append((i, col))
                self.__win_seq = coord_list
                return winner

    def _search_diag(self, board_mtx):
        for diag in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            cur_diag = np.diag(board_mtx, diag)
            if diag < 0:
                first_coord = (-1 * diag, 0)
            elif diag > 0:
                first_coord = (0, diag)
            else:
                first_coord = (0, 0)
            winner, index_list = self._search_winner(cur_diag)
            if winner is not None:
                coord_list = []
                for i in index_list:
                    coord = (
                    first_coord[0] + 1 * i, first_coord[1] + 1 * i)
                    coord_list.append(coord)
                self.__win_seq = coord_list
                return winner

    def _search_rev_diag(self,flipped_board):
        for diag in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            diagonal = np.diag(flipped_board, diag)
            cur_diag = list(reversed(diagonal))
            if diag < 0:
                first_coord = (-1 * diag, 0)
            elif diag > 0:
                first_coord = (0, diag)
            else:
                first_coord = (0, 0)
            winner, index_list = self._search_winner(cur_diag)
            if winner is not None:
                coord_list = []
                for i in index_list:
                    coord = (first_coord[0] + 1 * i, self.COLUMN_NUM - first_coord[1] - 1 * i - 1)
                    coord_list.append(coord)
                self.__win_seq = coord_list
                return winner

    def get_winner(self):
        board_mtx = self.get_board()
        winner_row = self._search_row(board_mtx)
        if winner_row is not None:
            return winner_row
        winner_col = self._search_col(board_mtx)
        if winner_col is not None:
            return winner_col
        winner_diag = self._search_diag(board_mtx)
        if winner_diag is not None:
            return winner_diag
        flipped_board = np.fliplr(board_mtx)
        winner_rev_diag = self._search_rev_diag(flipped_board)
        if winner_rev_diag is not None:
            return winner_rev_diag
        # check if the board is full
        board_bool = (board_mtx != self.EMPTY)
        if board_bool.all():
            return self.DRAW
        return None

    def is_full(self):
        board_bool = (self.__board_mtx != self.EMPTY)
        return board_bool.all()


    def get_player_at(self, row, col):
        return self.get_board()[row,col]

    def get_current_player(self):
        return self.__current_player

    def get_board(self):
        return self.__board_mtx










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