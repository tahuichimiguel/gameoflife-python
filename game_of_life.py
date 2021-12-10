from collections import namedtuple, defaultdict
import time
import typing

Cell = namedtuple("Cell", ["x", "y"])


class BoardRule:
    def populateNext(self, board: set) -> dict:
        pass


class ClassicalRule(BoardRule):
    def populateNext(self,  board: set) -> set:
        """Returns a set of cells active in the next board update"""
        new_board: set = set()
        for cell, count in self.getNeighborCount(board).items():
            if count == 3 or (cell in board and count == 2):
                new_board.add(cell)
        return new_board

    def getNeighbors(self, cell: Cell):
        """Create generator for all neighbors of a cell"""
        for x in range(cell.x - 1, cell.x + 2):
            for y in range(cell.y - 1, cell.y + 2):
                if (x, y) != (cell.x, cell.y):
                    yield Cell(x, y)

    def getNeighborCount(self, board: set) -> int:
        """Get the number of neighbors"""
        neighbor_counts = defaultdict(int)
        for cell in board:
            for neighbor in self.getNeighbors(cell):
                neighbor_counts[neighbor] += 1
        return neighbor_counts


class LateralNeighborRule(BoardRule):
    def populateNext(self,  board: set) -> set:
        """Returns a set of cells active in the next board update"""
        new_board: set = set()
        for cell, count in self.getLateralNeighborCount(board).items():
            if count == 2 or (cell in board and count == 1):
                new_board.add(cell)
        return new_board

    def getLateralNeighbors(self, cell: Cell):
        for x in range(cell.x - 1, cell.x + 2):
            if x == cell.x - 1 or x == cell.x + 1:
                yield Cell(x, cell.y)

    def getLateralNeighborCount(self, board: set) -> int:
        """Get the number of neighbors"""
        neighbor_counts = defaultdict(int)
        for cell in board:
            for neighbor in self.getLateralNeighbors(cell):
                neighbor_counts[neighbor] += 1
        return neighbor_counts


def advanceBoard(board: set, rule: BoardRule) -> set:
    """Generate a new board using the advancing rule """
    new_board: set = rule.populateNext(board)
    return new_board


def generateBoard(start_state: str):
    """Generate a board as defined by a starting state"""
    board: set = set()
    for row, line in enumerate(start_state.split("\n")):
        for col, elem in enumerate(line):
            if elem == "X":
                board.add(Cell(int(col), int(row)))
    return board


def boardToString(board: set, pad: int = 0):
    """Generate a printable representation of the board"""
    if not board:
        return "empty"
    board_str = ""
    xs = [x for (x, _) in board]
    ys = [y for (_, y) in board]
    for y in range(min(ys) - pad, max(ys) + 1 + pad):
        for x in range(min(xs) - pad, max(xs) + 1 + pad):
            board_str += "X" if Cell(x, y) in board else "."
        board_str += "\n"
    return board_str.strip()


if __name__ == "__main__":
    f = generateBoard("......X.\nXX......\n.X...XXX")
    rule1 = ClassicalRule()
    rule2 = LateralNeighborRule()
    for _ in range(100):
        print("\033[2J\033[1;1H" + boardToString(f))
        print('')
        f1 = advanceBoard(f, rule1)
        f2 = advanceBoard(f, rule2)
        f = set.union(f1, f2)
        time.sleep(0.1)
