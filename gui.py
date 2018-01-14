import tkinter as tk


class Gui(object):
    def set_collumn_choice_handler(self, handler):
        raise NotImplementedError

    def output_winner(self, winner):
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError

    def output_board(self, board):
        raise NotImplementedError

    def not_your_turn_msg(self):
        raise NotImplementedError

    def blocked_cell(self):
        raise NotImplementedError

    def output_error(self):
        raise NotImplementedError


class TkinterGui(Gui):
    def __init__(self):
        super(TkinterGui, self).__init__()
        self.root = tk.Tk()