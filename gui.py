import tkinter as tk
from communicator import Communicator
import numpy as np
from tkinter import messagebox
import time




#resizeable


class Gui:
    num_col = 7
    num_row = 6
    INIT_Y0 = 3
    INIT_Y1 = 73
    INIT_X0 = 3
    INIT_X1 = 83
    OVAL_WIDTH = 80
    PLAYER_ONE = 0
    PLAYER_ONE_COLOR = "indian red1"
    PLAYER_TWO_COLOR = "lightgoldenrod1"
    PLAYER_TWO = 1
    COL_WIDTH = 100

    def __init__(self):
        # super(TkinterGui, self).__init__()
        self._parent = tk.Tk()
        # self._canvas = tk.Canvas(self._parent,width = 2000, height = 2000, bg = "white")
        # self._canvas.pack()
        # self.__communicator = Communicator(parent, port, ip)
        # self.__communicator.connect()
        # self.__communicator.bind_action_to_message(self.__handle_message)
        self.__place_widgets()

    def __place_widgets(self):
        ## create config for MN

        self._title = tk.Canvas(self._parent, width = 690, height = 60,bg="grey")
        self._title.pack(side = "top")
        self._title.create_text(710 / 2,60 / 2,text="Four In A Row", fill="brown4",font=("Comic Sans MS", 30,"bold"))
        self._columns_list = []
        self._upper_frame = tk.Canvas(self._parent, width=700, height=20,
          highlightbackground= "black",bd=2,highlightthickness=1, bg="NavajoWhite4")
        self._upper_frame.pack()
        for col in reversed(list(range(self.num_col))):
            button = tk.Button(self._upper_frame, command =lambda c=col: self.__set_collumn_choice_handler(c))
            button.configure(width=13, activebackground="grey", bg = "NavajoWhite4", borderwidth=1)
            button.pack(side="right",  fill ="both")
        for col in range(self.num_col):
            self._columns_list.append(tk.Canvas(self._parent, width=91, height=480,
             highlightbackground="NavajoWhite4" ,bd=2,highlightthickness=2, bg="NavajoWhite4"))
            self._columns_list[-1].pack(side = "left")
            for row in range(self.num_row):
                self._columns_list[-1].create_oval(self.INIT_X0, self.INIT_X0+row*self.OVAL_WIDTH,
                self.INIT_X1, self.INIT_Y1+row*self.OVAL_WIDTH, width=0, fill='grey')

    def __set_collumn_choice_handler(self, column):
        self.__game_handler(column)
        # self._communicator.send_message(column)

    def run(self):
        self._parent.mainloop()

    def set_collumn_choice_handler(self, handler):
        self.__game_handler = handler


    def show_winning(self,board,list_coord, winner):
        self.output_board(board)
        if winner == self.PLAYER_ONE:
            winner_color = self.PLAYER_ONE_COLOR
        else:
            winner_color = self.PLAYER_TWO_COLOR
        for coord in list_coord:
            self._columns_list[coord[1]].create_oval(self.INIT_X0,self.INIT_X0
                + coord[0] * self.OVAL_WIDTH,self.INIT_X1,self.INIT_Y1 +
                coord[0] * self.OVAL_WIDTH, width=3,fill=winner_color)
        self._columns_list[coord[1]].pack()
        self._output_winner(winner)


    def _output_winner(self, winner):
        messagebox.showinfo("We Have A winner!",
                            "and the winner is....   %s" % winner)
        self.shutdown()


    def shutdown(self):
        self._parent.destroy()

    def output_board(self, board):
        for col in range(board.shape[1]):
            cur_col = board[:,col]
            for row in range(len(cur_col)):
                if cur_col[row] == self.PLAYER_ONE:
                    color = self.PLAYER_ONE_COLOR
                elif cur_col[row] == self.PLAYER_TWO:
                    color = self.PLAYER_TWO_COLOR
                else:
                    continue
                self._columns_list[col].create_oval(self.INIT_X0, self.INIT_X0+row*self.OVAL_WIDTH,
                self.INIT_X1, self.INIT_Y1+row*self.OVAL_WIDTH, width=0, fill=color)


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
