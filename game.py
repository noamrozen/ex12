import random
import numpy as np


class Game:

    ROWS_NUM = 6
    COLUMN_NUM = 7
    SEQ_FOR_WIN = 3
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    EMPTY = -1
    ILLEGAL_MOVE = "Illegal move"

    def __init__(self):
        # choosing the first player randomly
        # self.__current_player = random.choice([self.PLAYER_ONE,self.PLAYER_TWO])
        self.__current_player = self.PLAYER_ONE
        # initiating the board with "None"
        self.__board_mtx = np.full((self.ROWS_NUM,self.COLUMN_NUM),self.EMPTY)


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

    def search_winner(self, list):
        player_one_counter = 0
        player_two_counter = 0
        for i in range(len(list)):
            if list[i] == self.PLAYER_ONE:
                player_one_counter += 1
                player_two_counter = 0
            if list[i] == self.PLAYER_TWO:
                player_two_counter += 1
                player_one_counter = 0
            if player_one_counter == self.SEQ_FOR_WIN:
                return str(self.PLAYER_ONE)
            if player_two_counter == self.SEQ_FOR_WIN:
                return str(self.PLAYER_TWO)
        return None

    def get_winner(self):
        board_mtx = self.get_board()
        for row in range(self.ROWS_NUM):
            cur_row = board_mtx[row, :]
            if self.search_winner(cur_row):
                return self.search_winner(cur_row)
        for col in range(self.COLUMN_NUM):
            cur_col = board_mtx[:, col]
            if self.search_winner(cur_col):
                return self.search_winner(cur_col)
        for diag in range(-(self.ROWS_NUM-1), self.COLUMN_NUM-1):
            cur_diag = np.diag(board_mtx, diag)
            if self.search_winner(cur_diag):
                return self.search_winner(cur_diag)
        fliped_board = np.fliplr(board_mtx)
        for diag in range(-(self.ROWS_NUM-1), self.COLUMN_NUM-1):
            cur_diag = np.diag(fliped_board, diag)
            if self.search_winner(cur_diag):
                return self.search_winner(cur_diag)
        board_bool = (board_mtx != self.EMPTY)
        if board_bool.all():
            return self.DRAW
        return None


    def get_player_at(self, row, col):
        return self.get_board()[row,col]

    def get_current_player(self):
        return self.__current_player

    def get_board(self):
        return self.__board_mtx






if __name__ == '__main__':
    # test for exception when there is a winner
    game = Game()
    # print(game.get_board())

    game.make_move(1)
    game.make_move(1)
    game.make_move(1)
    game.make_move(2)
    game.make_move(0)
    game.make_move(0)
    game.make_move(0)
    game.make_move(2)
    game.make_move(2)

    print(game.get_board())


    # # test for exception when there is a winner by diagonal
    # game = Game()
    # # print(game.get_board())
    # game.make_move(1)
    # game.make_move(1)
    # game.make_move(1)
    # game.make_move(2)
    # game.make_move(0)
    # game.make_move(0)
    # game.make_move(2)
    # game.make_move(0)
    # #game.make_move(2)
    # print(game.get_board())


    ## tester for exception when game over
    # game = Game()
    # print(game.get_board())
    # game.make_move(1)
    # game.make_move(1)
    # game.make_move(1)
    # game.make_move(0)
    # game.make_move(0)
    # game.make_move(0)
    # game.make_move(2)
    # game.make_move(2)
    # game.make_move(2)
    # game.make_move(3)
    # game.make_move(3)
    # game.make_move(3)
    ##game.make_move(1)
    # print(game.get_board())


    # tester for exception when column full
    # game = Game()
    # print(game.get_board())
    # game.make_move(1)
    # game.make_move(1)
    # game.make_move(1)
    ## game.make_move(1)
    # print(game.get_board())