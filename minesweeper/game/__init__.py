import numpy as np

from minesweeper.models import GameModel
from minesweeper.ui import GameUI


class MineSweeperGame:
    _shape = (10, 10)
    _nr_mines = 15

    def __init__(self):
        self._model = GameModel(self._shape, self._nr_mines)
        self._ui = GameUI(self, self._shape)

    def start(self):
        self._ui.start()

    def restart(self):
        self._model = GameModel(self._shape, self._nr_mines)
        self._ui.reset_buttons()

    def handle_click(self, x, y) -> np.ndarray:
        result = self._model.reveal_field(row=y, col=x)
        return result, self._model.field_statuses
