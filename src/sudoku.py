from math import sqrt
from graph_coloring import GraphColoring

"""
Sudoku class
the board is an N x N list of ints, representing the colors(0-indexed)
or None if no color is set. N must be s square number
"""


class Sudoku:
    def __init__(self, board: list[list[int | None]]) -> None:
        self.board = board
        self.board_size: int = len(board)
        self.square_size: int = int(
            sqrt(self.board_size)
        )  # size of the squares of the sudoku

    # returns a board with numbers representing a valid solution, or None if none exist
    def solve(self) -> list[list[int]] | None:
        graph_reduction: GraphColoring = self.reduceToGraphColoring()
        solution: list[int] | None = graph_reduction.solve()
        if solution is None:
            return None
        return self.reconstructSolutionFromReduction(solution)

    @classmethod
    # creates a new Sudoku object from input
    def initializeFromInput(self):
        board_size = int(
            input("Please input the size of the board (must be a square number): ")
        )
        board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        print(
            f"Please now input the board in {board_size} seperate lines, each containing {board_size} numbers\
                the numbers should be from 1 to {board_size}, or 0 if the cell is empty"
        )
        for i in range(board_size):
            for j in range(board_size):
                board[i][j] = int(input())
        return Sudoku(board)

    # returns a new GraphColoring object with a reduction from the sudoku board
    def reduceToGraphColoring(self) -> GraphColoring:
        edges: list[list[int]] = []
        colors: list[int] = []

        for id in range(self.board_size**2):
            i, j = self.idToCoordinate(id)
            colors.append(self.board[i][j])  # initializing colors

        for row in range(self.board_size):
            for i in range(self.board_size):
                for j in range(i + 1, self.board_size):
                    id1: int = self.coordinateToId(row, i)
                    id2: int = self.coordinateToId(row, j)
                    edges.append([id1, id2])
                    # elements in the same row must be unique

        for column in range(self.board_size):
            for i in range(self.board_size):
                for j in range(i + 1, self.board_size):
                    id1: int = self.coordinateToId(i, column)
                    id2: int = self.coordinateToId(j, column)
                    edges.append([id1, id2])
                    # elements in the same column must be unique

        for square_row in range(
            0, self.board_size, self.square_size
        ):  # iterating over squares
            for square_column in range(self.board_size, self.square_size):
                for row1 in range(
                    0, square_row, square_row + self.square_size
                ):  # iterating over first element in the square
                    for column1 in range(
                        square_column, square_column + self.square_size
                    ):
                        for row2 in range(
                            row1 + 1, square_row + self.square_size
                        ):  # iterating over second element in the square
                            for column2 in range(
                                column1 + 1, square_row + self.square_size
                            ):
                                id1: int = self.coordinateToId(row1, column1)
                                id2: int = self.coordinateToId(row2, column2)
                                edges.append([id1, id2])
                                # elements in the same square nums be unique

        for edge in edges:
            edge = sorted(edge)  # making sure edges are sorted for uniqueness
        edges = list(set(edges))  # getting rid of duplicate edges

        return GraphColoring(
            num_nodes=self.board_size**2,
            edges=edges,
            colors=colors,
            max_colors=self.board_size,
        )

    # takes a valid solution of the reduction graph as a list of ints representing colors,
    # and returns a solution for the sudoku as an N x N list of ints
    def reconstructSolutionFromReduction(self, solution: list[int]) -> list[list[int]]:
        solved_board: list[list[int]] = [
            [0 for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        for id, color in enumerate(solution):
            i, j = self.idToCoordinate(id)
            solved_board[i][j] = color
        return solved_board

    # takes a coordinate in the sudoku board and returns the id of the node in the reduction graph
    def coordinateToId(self, i: int, j: int) -> int:
        return i * self.board_size + j

    # takes an id of a node in the reduction graph and returns the coordinates in the sudoku board
    def idToCoordinate(self, id: int) -> tuple[int, int]:
        return id // self.board_size, id % self.board_size
