import tkinter as tk
from communicator import Communicator
import numpy as np
from tkinter import messagebox
from gui_config import *


#resizeable

class Gui:
    PLAYER_ONE = 0
    PLAYER_ONE_COLOR = "indian red1"
    PLAYER_TWO_COLOR = "lightgoldenrod1"
    PLAYER_TWO = 1

    def __init__(self,row_num, col_num):
        # super(TkinterGui, self).__init__()
        self._parent = tk.Tk()
        self.num_row = row_num
        self.num_col = col_num
        self.__place_widgets()



    def __place_widgets(self):
        ## create config for MN

        self._title = tk.Canvas(self._parent, width=CAN_W, height=CAN_H,
                                bg=TITLE_BG)
        self._title.pack(side=TITLE_SIDE)
        self._title.create_text(WIN_W / 2, TITLE_H / 2, text= TEXT_TITLE,
                        fill=TEXT_FILL, font=(FONT, FINT_SIZE, BOLD_FONT))
        self._columns_list = []
        self._upper_frame = tk.Canvas(self._parent, width=FRAME_W,
                height=FRAME_H, highlightbackground=U_FRAME, bd=FRAME_BD,
                                    highlightthickness=TK,bg=BG_COLOR)
        self._upper_frame.pack()
        for col in reversed(list(range(self.num_col))):
            button = tk.Button(self._upper_frame, command=lambda c=col:
            self.__set_collumn_choice_handler(c))
            button.configure(width=BT_W, activebackground=TITLE_BG,
                             bg=BG_COLOR, borderwidth=TK)
            button.pack(side=BUTTONS_SIDE,  fill=FILL_BOTH)
        for col in range(self.num_col):
            self._columns_list.append(tk.Canvas(self._parent, width=COL_W,
                    height=COL_H,highlightbackground=BG_COLOR,
                    bd=FRAME_BD,highlightthickness=FRAME_BD, bg=BG_COLOR))
            self._columns_list[-1].pack(side=COLUMNS_SIDE)
            for row in range(self.num_row):
                self._columns_list[-1].create_oval(INIT_X0, INIT_X0+row *
                        OVAL_WIDTH, INIT_X1, INIT_Y1+row*OVAL_WIDTH,
                        width=0, fill=TITLE_BG)

    def __set_collumn_choice_handler(self, column):
        self.__game_handler(column)
        # self._communicator.send_message(column)

    def set_collumn_choice_handler(self, handler):
        self.__game_handler = handler

    def show_winning(self, board, list_coord, winner):
        self.output_board(board)
        if winner == self.PLAYER_ONE:
            winner_color = self.PLAYER_ONE_COLOR
        elif winner == self.PLAYER_TWO:
            winner_color = self.PLAYER_TWO_COLOR
        else:
            self.output_draw()
            return
        for coord in list_coord:
            self._columns_list[coord[1]].create_oval(INIT_X0, INIT_X0
                + coord[0] * OVAL_WIDTH, INIT_X1, INIT_Y1 +
                coord[0] * OVAL_WIDTH, width=WIN_WIDTH, fill=winner_color)
            self._columns_list[coord[1]].pack()
        self._output_winner(winner)

    @staticmethod
    def output_draw():
        messagebox.showinfo(DREW_TITLE, DREW_TEXT)

    def _output_winner(self, winner):
        messagebox.showinfo(WINNER_TITLE, WINNER_TEXT % winner)
        self.shutdown()

    def shutdown(self):
        self._parent.destroy()

    def output_board(self, board):
        for col in range(board.shape[1]):
            cur_col = board[:, col]
            for row in range(len(cur_col)):
                if cur_col[row] == self.PLAYER_ONE:
                    color = self.PLAYER_ONE_COLOR
                elif cur_col[row] == self.PLAYER_TWO:
                    color = self.PLAYER_TWO_COLOR
                else:
                    continue
                self._columns_list[col].create_oval(INIT_X0, INIT_X0+row *
                                                    OVAL_WIDTH,
                INIT_X1, INIT_Y1+row*OVAL_WIDTH, width=0, fill=color)

    def output_error(self, error_text):
         messagebox.showinfo(ERROR_TITLE, error_text)

    def run(self):
        self._parent.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    # Finds out the IP, to be used cross-platform without special issues.
    # # (on local machine, could also use "localhost" or "127.0.0.1")
    port = 8000
    server = True
    if server:
        self = Gui(root, port)
        root.title(SERVER)
    root.mainloop()
