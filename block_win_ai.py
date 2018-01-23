import numpy as np
from game import Game
from ai import AI


class BlockWinAI(AI):
    SEQ_LEN = 3

    def __init__(self, player):
        self.player = player

    @staticmethod
    def first_turn(game):
        board = game.get_board()
        board_bool = (board != game.EMPTY)
        if board_bool.all():
            return 5, 3

    @staticmethod
    def get_possible_cells(board):
        cell_list = []
        for col in range(len(board[0])):
            row_index = int(Game.get_lowest_empty(board[:, col]))
            cell_list.append((row_index,col))
        return cell_list

    @staticmethod
    def an_optional_cell(game, cells):
        board = game.get_board()
        for cell in cells:
            if cell[0] < 0 or cell[0] > 5 or cell[1] < 0 or cell[1] > 7:
                continue
            if cell[0] == int(game.get_lowest_empty(board[:,cell[1]])):
                return cell

    def placing_for_seq(self, game, seq):
        board = game.get_board()
        almost_seq = list(sorted(seq))
        if almost_seq[0][0] == almost_seq[1][0]:
            # the seq is in the same row
            cell_placing = [(almost_seq[0][0], almost_seq[0][1]-1),
                            (almost_seq[-1][0], almost_seq[-1][1]+1)]
            print(cell_placing, "**")
            return self.an_optional_cell(game, cell_placing)
        elif almost_seq[0][1] == almost_seq[1][1]:
            # the seq is in the same column
            cell_placing = [(almost_seq[0][0]-1,almost_seq[0][1])]
            print(cell_placing)
            return self.an_optional_cell(game, cell_placing)
        else:
            # in the same diagonal
            if almost_seq[0][0] + 1  == almost_seq[1][0]:
                cell_placing = [(almost_seq[0][0]-1, almost_seq[0][1]-1)]
                return self.an_optional_cell(game, cell_placing)
            else:
                cell_placing = [(almost_seq[0][0] + 1, almost_seq[0][1] + 1)]
                return self.an_optional_cell(game, cell_placing)

    def choose_column(self, game):
        possible_columns = np.nonzero(game.get_board()[0] == game.EMPTY)[0]
        column = np.random.choice(possible_columns, 1)[0]
        # first = self.first_turn(game.get_board())
        # if first is not None:
        #     return first
        # column = self.find_blocking_column(game)
        # if column is None:
        #     possible_columns = np.nonzero(game.get_board()[0] == game.EMPTY)[0]
        #     column = np.random.choice(possible_columns, 1)[0]
        return column

    def find_blocking_column(self, game):
        board = game.get_board()
        seq_list = self.get_seq_list(board)
        if seq_list is not None:
            for seq in seq_list:
                placing = self.placing_for_seq(game, seq)
                if placing is not None:
                    choosen_column = placing[1]
                    # call the func to make the moove
                    return choosen_column

    def _search_row(self, board_mtx):
        row_seq= []
        for row in range(self.ROWS_NUM):
            cur_row = board_mtx[row, :]
            index_list = self._search_winner(cur_row)
            if index_list is not None:
                coord_list = []
                for i in index_list:
                    coord_list.append((row, i))
                row_seq.append(coord_list)
        return row_seq

    def _search_col(self, board_mtx):
        col_seq = []
        for col in range(self.COLUMN_NUM):
            cur_col = board_mtx[:, col]
            index_list = self._search_winner(cur_col)
            if index_list is not None:
                coord_list = []
                for i in index_list:
                    coord_list.append((i, col))
                col_seq.append(coord_list)
        return col_seq


    def _search_diag(self, board_mtx):
        diag_seq = []
        for diag in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            cur_diag = np.diag(board_mtx, diag)
            if diag < 0:
                first_coord = (-1 * diag, 0)
            elif diag > 0:
                first_coord = (0, diag)
            else:
                first_coord = (0, 0)
            index_list = self._search_winner(cur_diag)
            if index_list is not None:
                coord_list = []
                for i in index_list:
                    coord = (
                    first_coord[0] + 1 * i, first_coord[1] + 1 * i)
                    coord_list.append(coord)
                diag_seq.append(coord_list)
        return diag_seq

    def _search_rev_diag(self,flipped_board):
        rev_diag_seq = []
        for diag in range(-(self.ROWS_NUM - 1), self.COLUMN_NUM - 1):
            diagonal = np.diag(flipped_board, diag)
            cur_diag = list(reversed(diagonal))
            if diag < 0:
                first_coord = (-1 * diag, 0)
            elif diag > 0:
                first_coord = (0, diag)
            else:
                first_coord = (0, 0)
            index_list = self._search_winner(cur_diag)
            if index_list is not None:
                coord_list = []
                for i in index_list:
                    coord = (first_coord[0] + 1 * i, self.COLUMN_NUM - first_coord[1] - 1 * i - 1)
                    coord_list.append(coord)
                rev_diag_seq.append(coord_list)
        return rev_diag_seq

    def get_seq_list(self, board_mtx):
        seq_list = []
        row_seq = self._search_row(board_mtx)
        if row_seq is not None:
            [seq_list.append(seq) for seq in row_seq ]
        col_seq = self._search_col(board_mtx)
        if col_seq is not None:
            [seq_list.append(seq) for seq in col_seq ]
        diag_seq = self._search_diag(board_mtx)
        if diag_seq is not None:
            [seq_list.append(seq) for seq in diag_seq ]
        flipped_board = np.fliplr(board_mtx)
        rev_diag_seq = self._search_rev_diag(flipped_board)
        if rev_diag_seq is not None:
            [seq_list.append(seq) for seq in rev_diag_seq ]
        # check if the board is full
        print(seq_list)
        return seq_list

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
            if len(player_one_seq) == self.SEQ_LEN:
                return player_one_seq
            if len(player_two_seq) == self.SEQ_LEN:
                return player_two_seq



if __name__ == '__main__':
    ai = BlockWinAI(1)
    game = Game()
    board = game.get_board()

    game.make_move(1)
    game.make_move(1)
    game.make_move(0)
    game.make_move(1)
    game.make_move(0)
    game.make_move(0)
    game.make_move(0)
    game.make_move(0)
    game.make_move(2)
    #game.make_move(2)
    print(board)
    # pos = ai.get_possible_cells(board)
    # print(pos)
    print(ai.blocking_or_winning(board))



