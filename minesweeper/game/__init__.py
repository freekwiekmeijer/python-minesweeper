import numpy as np

from minesweeper.models import GameModel
from minesweeper.ui import GameUI


class MineSweeperGame:
    def __init__(self):
        shape = (10, 10)
        nr_mines = 15
        self._model = GameModel(shape, nr_mines)
        self._ui = GameUI(self, shape)

    def start(self):
        self._ui.start()

    def handle_click(self, x, y) -> np.ndarray:
        result = self._model.reveal_field(row=y, col=x)
        return result, self._model.field_statuses
