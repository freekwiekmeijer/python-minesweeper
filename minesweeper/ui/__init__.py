from functools import partial
import tkinter

import numpy as np  # TODO abstract


class GameUI:
    def __init__(self, game, shape):
        self._game = game
        self._shape = shape
        self._buttons = [None] * shape[0] * shape[1]
        self._initialize_window(shape)

    @property
    def game(self):
        return self._game

    @staticmethod
    def _on_click(ui, x, y):
        result, field_statuses = ui.game.handle_click(x, y)
        if not result:
            ui.show_game_over_modal()
        nr_rows, nr_cols = field_statuses.shape
        for col in range(nr_cols):
            for row in range(nr_rows):
                field_status = field_statuses[row, col]
                btn = ui.get_button(x=col, y=row)
                if field_status == -1:
                    btn.configure(text="")
                elif field_status == 0:
                    btn.configure(text="0")
                elif field_status == np.inf:
                    btn.configure(text="*")
                else:
                    btn.configure(text=str(int(field_status)))

    def _get_button_index(self, x, y):
        # Buttons are indexed with row by row, i.e. [r1c1, r1c2, ... r1cN, r1c1, ...]
        row_size = self._shape[1]
        return row_size * y + x

    def _initialize_window(self, shape):
        self._window = tkinter.Tk()
        self._window.title("Minesweeper")
        for y in range(shape[0]):
            for x in range(shape[1]):
                btn = tkinter.Button(self._window, text=" ", command=partial(self._on_click, self, x, y))
                btn.grid(row=y, column=x)
                idx = self._get_button_index(x, y)
                self._buttons[idx] = btn

    def get_button(self, x, y):
        return self._buttons[self._get_button_index(x, y)]

    def start(self):
        self._window.mainloop()

    def reset_buttons(self):
        for btn in self._buttons:
            btn.configure(text=" ")

    def show_game_over_modal(self):
        popup = tkinter.Toplevel(self._window)

        def _restart_game():
            popup.destroy()
            self.game.restart()

        label = tkinter.Label(popup, text="Game over")
        label.grid(row=0, column=0)
        btn = tkinter.Button(popup, text="OK", command=_restart_game)
        btn.grid(row=0, column=1)
