import tkinter as tk
from communicator import Communicator
import numpy as np
from tkinter import messagebox
from gui_config import *




#resizeable


class Gui:
    num_col = 7
    num_row = 6
    PLAYER_ONE = 0
    PLAYER_ONE_COLOR = "indian red1"
    PLAYER_TWO_COLOR = "lightgoldenrod1"
    PLAYER_TWO = 1


    def __init__(self,row_num, col_num):
        # super(TkinterGui, self).__init__()
        self._parent = tk.Tk()
        # self._canvas = tk.Canvas(self._parent,width = 2000, height = 2000, bg = "white")
        # self._canvas.pack()
        # self.__communicator = Communicator(parent, port, ip)
        # self.__communicator.connect()
        # self.__communicator.bind_action_to_message(self.__handle_message)
        self.__place_widgets()
        self.num_row = row_num
        self.num_col = col_num



    def __place_widgets(self):
        ## create config for MN

        self._title = tk.Canvas(self._parent, width = CAN_W, height = CAN_H,bg = TITLE_BG)
        self._title.pack(side = "top")
        self._title.create_text(WIN_W / 2,TITLE_H / 2,text= TEXT_TITLE, fill=TEXT_FILL ,font=(FONT, FINT_SIZE,BOLD_FONT))
        self._columns_list = []
        self._upper_frame = tk.Canvas(self._parent, width=FRAME_W, height=FRAME_H,
          highlightbackground= U_FRAME ,bd=FRAME_BD,highlightthickness=TK, bg=BG_COLOR)
        self._upper_frame.pack()
        for col in reversed(list(range(self.num_col))):
            button = tk.Button(self._upper_frame, command =lambda c=col: self.__set_collumn_choice_handler(c))
            button.configure(width=BT_W, activebackground=TITLE_BG, bg = BG_COLOR, borderwidth=TK)
            button.pack(side="right",  fill =FILL_BOTH)
        for col in range(self.num_col):
            self._columns_list.append(tk.Canvas(self._parent, width=COL_W, height=COL_H,
             highlightbackground=BG_COLOR ,bd=FRAME_BD,highlightthickness=FRAME_BD, bg=BG_COLOR))
            self._columns_list[-1].pack(side = "left")
            for row in range(self.num_row):
                self._columns_list[-1].create_oval(INIT_X0, INIT_X0+row*OVAL_WIDTH,
                INIT_X1, INIT_Y1+row*OVAL_WIDTH, width=0, fill=TITLE_BG)

    def __set_collumn_choice_handler(self, column):
        self.__game_handler(column)
        # self._communicator.send_message(column)


    def set_collumn_choice_handler(self, handler):
        self.__game_handler = handler


    def show_winning(self, board, list_coord, winner):
        self.output_board(board)
        if winner == self.PLAYER_ONE:
            winner_color = self.PLAYER_ONE_COLOR
        else:
            winner_color = self.PLAYER_TWO_COLOR
        for coord in list_coord:
            self._columns_list[coord[1]].create_oval(INIT_X0, INIT_X0
                + coord[0] * OVAL_WIDTH, INIT_X1, INIT_Y1 +
                coord[0] * OVAL_WIDTH, width=WIN_WIDTH ,fill=winner_color)
        self._columns_list[coord[1]].pack()
        self._output_winner(winner)


    def _output_winner(self, winner):
        messagebox.showinfo("We Have A winner!",
                            "and the winner is....   %s" % winner)
        self._shutdown()


    def _shutdown(self):
        self._parent.destroy()

    def output_board(self, board):
        for col in range(board.shape[1]):
            cur_col = board[:,col]
            for row in range(len(cur_col)):
                if cur_col[row] == self.PLAYER_ONE:
                    color = gui.PLAYER_ONE_COLOR
                else:
                    color = gui.PLAYER_TWO_COLOR
                self._columns_list[col].create_oval(INIT_X0, INIT_X0+row*OVAL_WIDTH,
                INIT_X1, INIT_Y1+row*OVAL_WIDTH, width=0, fill=color)


    def output_error(self, error_text):
         messagebox.showinfo("ERROR!", error_text)


if __name__ == "__main__":
    root = tk.Tk()
    # Finds out the IP, to be used cross-platform without special issues.
    # # (on local machine, could also use "localhost" or "127.0.0.1")
    port = 8000
    server = True
    if server:
        gui = Gui(root, port)
        root.title("Server")
        arr = np.array([[1,0,1,0,1,0,1]])
        gui.output_board(arr)
        gui.show_winning(arr, [[0,0],[1,1],[2,2],[3,3]], 1)
    # else:
    #     Gui(root, port, socket.gethostbyname(socket.gethostname()))
    #     root.title("Client")
    root.mainloop()
