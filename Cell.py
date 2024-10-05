from dataclasses import dataclass, field

# from collections import namedtuple
import pygame as py


@dataclass
class Cell:
    x: int
    y: int
    ind: int
    size: int = 20
    side: int = -1
    b_offset_x: int = 0
    b_offset_y: int = 0
    is_visited: bool = False
    re_visited: bool = False
    _selected: bool = False
    colors: list[str] = field(default_factory=list)
    neighbors: list = field(default_factory=list)
    borders: list[bool] = field(default_factory=list)
    boeder_thickness: int = 2

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        # if self.is_visited:
        #     self.re_visited = True
        if self._selected and not self.is_visited:
            self.is_visited = True
        # self.neighbors = get_valid_neighbors()

    def __post_init__(self):
        self.borders = [True, True, True, True]
        self.colors = ["red", "brown", "green"]

    def draw(self, app):
        if self.selected or self.is_visited or self.re_visited:
            pattern = [self.selected, self.re_visited, self.is_visited]
            py.draw.rect(
                app,
                self.colors[pattern.index(1)],
                (
                    self.x,  # + #(self.boeder_thickness * 2),
                    self.y,  # + (self.boeder_thickness * 2),
                    self.size,  # - (self.boeder_thickness * 3),
                    self.size,  # - (self.boeder_thickness * 3),
                ),
            )

        for ind, border in enumerate(self.borders):
            # ind = 0
            if border and ind == 0:
                py.draw.line(
                    app,
                    "black",
                    (self.x, self.y),
                    (self.x, self.y + self.size - 1),
                    self.boeder_thickness,
                )
            if border and ind == 1:
                py.draw.line(
                    app,
                    "black",
                    (self.x + self.size, self.y),
                    (self.x + self.size, self.y + self.size),
                    self.boeder_thickness,
                )
            if border and ind == 2:
                py.draw.line(
                    app,
                    "black",
                    (self.x, self.y),
                    (self.x + self.size, self.y),
                    self.boeder_thickness,
                )
            if border and ind == 3:
                py.draw.line(
                    app,
                    "black",
                    (self.x, self.y + self.size),
                    (self.x + self.size, self.y + self.size),
                    self.boeder_thickness,
                )


def remove_border(side: int, cell_a: Cell, cell_b: Cell = None):
    r_side = 0

    if side == 0:
        r_side = 1
    if side == 1:
        r_side = 0
    if side == 2:
        r_side = 3
    if side == 3:
        r_side = 2

    cell_a.borders[side] = False
    if cell_b:
        cell_b.borders[r_side] = False


def get_row_col(cell: Cell):
    row = (cell.x - cell.b_offset_x) / cell.size
    col = (cell.y - cell.b_offset_y) / cell.size

    return row, col


def get_valid_cell(ind, parent: Cell, board: list[Cell]):
    nab = None
    for cell in board:
        if cell.ind == ind:
            nab = cell
            break

    if not nab:
        return None

    p_row, p_col = get_row_col(parent)
    n_row, n_col = get_row_col(nab)

    if p_col == n_col:
        return nab
    elif abs(p_col - n_col) == 1:
        if p_row == n_row:
            return nab

    return None


def get_valid_neighbors(cell: Cell, board: list[Cell], rows: int):
    neighbors = []

    # valid_cells = list(map(lambda x: x.ind, board))

    for i in [-1, 1]:
        ind = cell.ind + i

        # if ind in valid_cells:
        neighbors.append(get_valid_cell(ind, cell, board))

    for j in [-1, 1]:
        ind = cell.ind + j * rows

        # if ind in valid_cells:
        neighbors.append(get_valid_cell(ind, cell, board))

    # print(len(neighbors))

    for ind, neb in enumerate(neighbors):
        if neb:
            neb.side = ind

    neighbors = list(
        filter(lambda neb: neb != None and neb.is_visited == False, neighbors)
    )
    cell.neighbors = neighbors
    return neighbors
