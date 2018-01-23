import tkinter as tk
from tkinter import messagebox
from gui_config import *

class Gui:
    PLAYER_ONE = 0
    PLAYER_ONE_COLOR = "blue"
    PLAYER_TWO_COLOR = "lightgoldenrod1"
    PLAYER_TWO = 1

    YOU_WON = 1
    YOU_LOST = -1
    DRAW = 0

    def __init__(self, row_num, col_num, player_color, is_ai):
        self.num_row = row_num
        self.num_col = col_num
        self.__player_color = player_color
        if is_ai:
            self.__buttons_state = tk.DISABLED
        else:
            self.__buttons_state = tk.NORMAL
        self.__game_handler = None

        self._parent = tk.Tk()
        self._parent.resizable(width=False, height=False)
        self.__place_widgets()

    @property
    def tk_root(self):
        return self._parent

    def run(self):
        self._parent.mainloop()

    def show_winning(self, board, list_coord, winner_color):
        self.output_board(board)
        if winner_color is not None:
            for coord in list_coord:
                # creating the winning ovals on the board with perimeter
                self._marking_winning_oval(coord, winner_color)
            self._output_winner(winner_color)
        else:
            self.output_draw()
            return

    def shutdown(self):
        self._parent.destroy()

    def output_board(self, board):
        for column in range(board.shape[1]):
            current_column = board[:, column]
            for row in range(len(current_column)):
                if current_column[row] == self.PLAYER_ONE:
                    color = self.PLAYER_ONE_COLOR
                elif current_column[row] == self.PLAYER_TWO:
                    color = self.PLAYER_TWO_COLOR
                else:
                    continue
                self.__color_oval(row, column, color)
                # self._columns_list[column].create_oval(
                #     INIT_X0,
                #     INIT_X0 + row * OVAL_WIDTH,
                #     INIT_X1,
                #     INIT_Y1+row*OVAL_WIDTH,
                #     width=0,
                #     fill=color
                # )

    @staticmethod
    def output_error(error_text):
        messagebox.showinfo(ERROR_TITLE, error_text)

    @staticmethod
    def output_draw():
        messagebox.showinfo(DREW_TITLE, DREW_TEXT)

    def set_column_choice_handler(self, handler):
        self.__game_handler = handler

    def press_column(self, column):
        self.__buttons[column].invoke()

    def disable_button(self, column):
        self.__buttons[column].config(state=tk.DISABLED)

    def enable_button(self, column):
        self.__buttons[column].config(state=tk.NORMAL)

    def __place_widgets(self):
        title_canvas = self.__create_title_canvas()
        upper_frame_canvas = self.__create_upper_frame_canvas()

        title_canvas.pack(side=TITLE_SIDE)
        upper_frame_canvas.pack()

        self.__place_column_choosing_buttons(upper_frame_canvas)
        self.__place_board_ovals()

    def __create_title_canvas(self):
        canvas = tk.Canvas(
            self._parent,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=TITLE_BACKGROUND_COLOR
        )

        canvas.create_text(
            WIN_W / 2,
            TITLE_H / 2,
            text=TEXT_TITLE,
            fill=TEXT_FILL,
            font=(FONT, FONT_SIZE, BOLD_FONT)
        )
        return canvas

    def __create_upper_frame_canvas(self):
        upper_frame = tk.Canvas(
            self._parent,
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            highlightbackground=U_FRAME,
            bd=FRAME_BD,
            highlightthickness=TK,
            bg=BG_COLOR
        )
        return upper_frame

    def __place_column_choosing_buttons(self, upper_frame):
        self.__buttons = []
        for col in reversed(list(range(self.num_col))):
            button = tk.Button(upper_frame, command=lambda c=col: self.__call_game_handler(c))
            button.configure(
                width=BT_W,
                activebackground=TITLE_BACKGROUND_COLOR,
                bg=BG_COLOR,
                borderwidth=TK,
                state=self.__buttons_state
            )
            button.pack(side=BUTTONS_SIDE, fill=FILL_BOTH)
            self.__buttons.append(button)

    def __color_oval(self, row, column, color):
        self._columns_list[column].create_oval(
            INIT_X0,
            INIT_X0 + row * OVAL_WIDTH,
            INIT_X1,
            INIT_Y1 + row * OVAL_WIDTH,
            width=0,
            fill=color
        )

    def __place_board_ovals(self):
        self._columns_list = []

        for column in range(self.num_col):
            self._columns_list.append(tk.Canvas(
                self._parent,
                width=COL_W,
                height=COL_H,
                highlightbackground=BG_COLOR,
                bd=FRAME_BD,
                highlightthickness=FRAME_BD,
                bg=BG_COLOR
            ))
            self._columns_list[-1].pack(side=COLUMNS_SIDE)
            for row in range(self.num_row):
                self.__color_oval(row=row, column=-1, color=TITLE_BACKGROUND_COLOR)
                # self._columns_list[-1].create_oval(
                #     INIT_X0,
                #     INIT_X0 + row * OVAL_WIDTH,
                #     INIT_X1,
                #     INIT_Y1 + row * OVAL_WIDTH,
                #     width=0,
                #     fill=TITLE_BACKGROUND_COLOR
                # )

    def __call_game_handler(self, column):
        self.__game_handler(column)

    def _marking_winning_oval(self, coord, color):
        self._columns_list[coord[1]].create_oval(INIT_X0, INIT_X0
                                                 + coord[0] * OVAL_WIDTH,
                                                 INIT_X1, INIT_Y1 +
                                                 coord[0] * OVAL_WIDTH,
                                                 width=WIN_WIDTH,
                                                 fill=color)
        self._columns_list[coord[1]].pack()

    def _output_winner(self, winner_color):
        if winner_color == self.__player_color:
            text = WINNER_TEXT
        else:
            text = LOSER_TEXT
        messagebox.showinfo(WINNER_TITLE, text)


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
