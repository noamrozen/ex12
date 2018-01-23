import numpy as np
import collections
from ai import AI


class MinMaxAi(AI):
    def __init__(self, player, recursion_depth = 3):
        self.player = player
        self.recursion_depth = recursion_depth

    def choose_column(self, game):
        board = game.get_board()
        occupied_columns = board[-1] != game.EMPTY
        not_full_columns = board[0] == game.EMPTY
        # possible_cells = np.nonzero(np.logical_and(occupied_columns, not_full_columns))[0]
        # possible_cells = set(possible_cells)
        # for cell in list(possible_cells):
        #     possible_cells |= {cell - 1, cell + 1}
        possible_cells = set(np.nonzero(not_full_columns)[0])
        if not possible_cells:
            possible_cells = {np.random.randint(0, game.COLUMN_NUM)}
        possible_cell_score_counter = collections.Counter()
        for possible_cell in possible_cells:
            game.make_move(possible_cell)
            possible_cell_score = min_max_ai_recursion(
                game=game,
                player_turn=self.player,
                ai_player=self.player,
                ai_opponent_player=({game.PLAYER_ONE, game.PLAYER_TWO} - {self.player}).pop(),
                possible_cells=possible_cells - {possible_cell},
                recursion_depth=self.recursion_depth
            )
            possible_cell_score_counter[possible_cell] = possible_cell_score
            game.unmake_move()
        return possible_cell_score_counter.most_common(1)[0][0]


def score_row_by_player(row, ai_player, ai_opponent):
    row_counter = np.zeros(len(row))
    row_counter[row == ai_player] = 1
    row_counter[row == ai_opponent] = -1
    while len(row_counter) > 1:
        n = len(row_counter)
        i = np.arange(n)
        new_length = int(np.floor(len(row_counter) / 2))
        last_cell = row_counter[-1]
        row_counter = row_counter[i % 2 == 0][:new_length] + row_counter[i % 2 == 1][:new_length]
        if new_length * 2 < n:
            row_counter = np.append(row_counter, last_cell)
    return row_counter[0]


def score_row(row, ai_player, ai_opponent):
    return score_row_by_player(row, ai_player, ai_opponent) - score_row_by_player(row, ai_opponent, ai_player)


def min_max_score(board, ai_player, ai_opponent):
    score = 0
    board = np.array(board)
    for row in board:
        score += score_row(row, ai_player, ai_opponent)
    for column in board.T:
        score += score_row(column, ai_player, ai_opponent)
    for diag_offset in range(board.shape[0] - 1):
        score += score_row(board.diagonal(diag_offset), ai_player, ai_opponent)
        score += score_row(board.diagonal(-diag_offset), ai_player, ai_opponent)
    for diag_offset in range(board.shape[1] - 1):
        score += score_row(board.T.diagonal(diag_offset), ai_player, ai_opponent)
        score += score_row(board.T.diagonal(-diag_offset), ai_player, ai_opponent)
    return score


def update_possible_cells(column, game, possible_cells):
    board = game.get_board()
    full_columns = board[0] != game.EMPTY
    possible_cells = possible_cells - set(np.nonzero(full_columns)[0])
    # if column not in possible_cells:
    #     if column < game.COLUMN_NUM - 1:
    #         possible_cells = possible_cells | {column + 1}
    #     if column > 0:
    #         possible_cells = possible_cells | {column - 1}
    return possible_cells


def min_max_ai_recursion(game, player_turn, ai_player, ai_opponent_player, possible_cells, recursion_depth):
    winner = game.get_winner()
    if winner == ai_player:
        return HIGH_SCORE - recursion_depth
    if winner == ai_opponent_player:
        return LOW_SCORE
    if recursion_depth == 0 or len(possible_cells) == 0:
        return min_max_score(game.get_board(), ai_player, ai_opponent_player)

    max_score = -np.inf
    for column in possible_cells:
        try:
            game.make_move(column)
        except ValueError:
            continue
        next_player = ai_player
        if player_turn == ai_player:
            next_player = ai_opponent_player
        score = min_max_ai_recursion(
            game=game,
            player_turn=next_player,
            ai_player=ai_player,
            ai_opponent_player=ai_opponent_player,
            possible_cells=update_possible_cells(column, game, possible_cells),
            recursion_depth=recursion_depth - 1
        )
        if score == LOW_SCORE:
            game.unmake_move()
            return score
        # move_score += score
        if score > max_score:
            max_score = score
        game.unmake_move()

    return max_score

# from game import Game
# game = Game()
#
# game.make_move(5)
# ai = MinMaxAi(game.PLAYER_TWO, recursion_depth=2)
# ai.find_legal_move(game, print)
