from typing import List, Tuple

import numpy as np


class GameModel:
    _max_recursion_depth = 10

    def __init__(self, shape, nr_mines):
        self._mine_locations = np.zeros(shape)  # 0=no mine, 1=mine
        self._field_statuses = np.zeros(shape) -1  # -1=not revealed, 0=blank, >0=nr of mines in adjacent cells, np.inf: contains mine
        nr_mines_placed = 0
        while nr_mines_placed < nr_mines:
            row, col = self._random_location()
            if self._mine_locations[row][col] == 0:
                self._mine_locations[row][col] = 1
                nr_mines_placed += 1

    @property
    def field_statuses(self):
        return self._field_statuses

    def reveal_field(self, row, col) -> bool:
        if self._mine_locations[row][col]:
            # Hit a mine!
            self._field_statuses[row][col] = np.inf
            return False
        else:
            # No mine here -> update field status to "revealed" and look around of we can uncover more
            self._field_statuses[row][col] = self._look_around(row, col)
            self._reveal_adjacent_fields(row, col)
            return True

    def _random_location(self) -> Tuple[int, int]:
        return tuple([
            np.random.randint(0, self._mine_locations.shape[i])
            for i in [0, 1]
        ])

    def _get_adjacent_coordinates(self, row, col) -> List[Tuple[int, int]]:
        # returns a list of all valid coordinates (row, col) in a 3 by 3 square around the specified point
        coordinates = [
            (row-1, col-1), (row, col-1), (row+1, col-1),
            (row-1, col), (row+1, col),
            (row-1, col+1), (row, col+1), (row+1, col+1),
        ]
        return [
            (row, col)
            for row, col in coordinates
            if row >= 0 and row < self._mine_locations.shape[0]
            and col >= 0 and col < self._mine_locations.shape[1]
        ]

    def _look_around(self, row, col) -> int:
        # returns the number of mines in the 3 by 3 square around (row, col)
        coordinates = self._get_adjacent_coordinates(row, col)
        return sum([self._mine_locations[row][col] for (row, col) in coordinates])

    def _reveal_adjacent_fields(self, row, col, recursion_depth=0):
        # Reveal all fields around (row, col) until it encounters a mine in the perimeter
        coordinates = [
            (row, col)
            for row, col in self._get_adjacent_coordinates(row, col)
            if self.field_statuses[row, col] == -1
        ]
        for row, col in coordinates:
            nr_mines_adjacent = self._look_around(row, col)
            self._field_statuses[row, col] = nr_mines_adjacent
            if nr_mines_adjacent == 0 and recursion_depth < self._max_recursion_depth:
                self._reveal_adjacent_fields(row, col, recursion_depth+1)
