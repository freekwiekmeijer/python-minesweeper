from typing import List, Tuple

import numpy as np


class GameModel:
    def __init__(self, shape, nr_mines):
        self._mine_locations = np.zeros(shape)  # 0=no mine, 1=mine
        self._field_statuses = np.zeros(shape) -1  # -1=not revealed, 0=blank, >0=nr of mines in adjacent cells

    def reveal_field(self, x, y) -> bool:
        if self._mine_locations[x][y]:
            # Hit a mine!
            return False
        else:
            # No mine here -> update field status to "revealed" and look around of we can uncover more
            self._field_statuses[x][y] = self._look_around(x, y)
            self._reveal_adjacent_fields(x, y)
            return True

    def _get_adjacent_coordinates(self, x, y) -> List[Tuple[int, int]]:
        # returns a list of all valid coordinates (x, y) in a 3 by 3 square around the specified point
        coordinates = [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1),
        ]
        return [
            (x, y)
            for (x, y) in coordinates
            if x >= 0 and x < self._mine_locations.shape[0]
            and y >= 0 and y < self._mine_locations.shape[1]
        ]

    def _look_around(self, x, y) -> int:
        # returns the number of mines in the 3 by 3 square around (x, y)
        coordinates = self._get_adjacent_coordinates(x, y)
        return sum([self._mine_locations[x][y] for (x, y) in coordinates])

    def _reveal_adjacent_fields(self, x, y) -> bool:
        # Reveal all fields around (x, y) until it encounters a mine in the perimeter
        coordinates = self._get_adjacent_coordinates(x, y)
        for c in coordinates:
            if self._look_around(c[0], c[1]) == 0:
                self._reveal_adjacent_fields(c[0], c[1])
