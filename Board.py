from dataclasses import dataclass, field
from random import choice, randint
from Cell import *


@dataclass
class Board:
    rows: int
    cols: int
    size: int
    offset_x: int = 0
    offset_y: int = 0
    reverse: bool = False
    current: Cell = None
    history: list[int] = field(default_factory=list)
    board: list[Cell] = field(default_factory=list)

    def __post_init__(self):
        for j in range(self.cols):
            for i in range(self.rows):
                x = i * self.size + self.offset_x
                y = j * self.size + self.offset_y
                ind = i + j * self.rows
                self.board.append(
                    Cell(
                        x,
                        y,
                        ind,
                        size=self.size,
                        b_offset_x=self.offset_x,
                        b_offset_y=self.offset_y,
                    )
                )

        # -- initialize the current cell
        # self.current = self.get_cell(3)
        self.current = self.get_cell()
        self.current.selected = True

        # print(get_row_col(self.board[-1]))

    def reset(self):
        self.board.clear()
        self.history.clear()
        self.current = None
        self.reverse = False
        self.__post_init__()

    def get_cell(self, n=None):
        if not self.current:
            cell = choice(self.board)
            if n:
                cell = self.board[n]
            get_valid_neighbors(cell, self.board, self.rows)
            self.history.append(cell.ind)
            return cell

        if len(self.current.neighbors):
            cell = choice(self.current.neighbors)
            get_valid_neighbors(cell, self.board, self.rows)
            if self.reverse:
                self.history.append(self.current.ind)
                self.reverse = False
            return cell

        cell = self.board[self.history.pop()]
        self.reverse = True
        if cell.is_visited:
            cell.re_visited = True
        get_valid_neighbors(cell, self.board, self.rows)
        return cell

    def next_step(self):
        next = self.get_cell()
        if next.ind not in self.history and not self.reverse:
            remove_border(next.side, self.current, next)
            self.history.append(next.ind)
        self.current.selected = False
        next.selected = True
        self.current = next

    def generate(self):
        if self.reverse and len(self.history) == 0:
            self.current.selected = False
            return

        self.next_step()

    def draw(self, app):
        for cell in self.board:
            cell.draw(app)
